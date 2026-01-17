import json
import os
import sqlite3
from datetime import datetime, timezone
from urllib.parse import urlparse

from mitmproxy import io
from mitmproxy.http import HTTPFlow

DB_PATH = os.path.join(os.getcwd(), "cookies.db")
MITM_PATH = os.path.join(os.getcwd(), "traffic.mitm")

FP_KEYWORDS = [
    "canvas", "todataurl", "getimagedata", "putimagedata",
    "audiocontext", "offlineaudiocontext",
    "webglrenderingcontext", "webgl_debug_renderer_info", "getparameter",
    "devicepixelratio", "screen.width", "screen.height", "screen.availwidth", "screen.availheight",
    "navigator.plugins", "navigator.mimetypes", "navigator.languages",
    "navigator.hardwareconcurrency", "navigator.devicememory",
    "navigator.webdriver",
    "enumeratedevices", "mediadevices",
    "rtcpeerconnection",
]

def netloc(url: str) -> str:
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ""

def norm_domain(d: str) -> str:
    d = (d or "").strip().lower()
    if d.startswith("www."):
        d = d[4:]
    return d

def detect_keywords(text: str) -> list[str]:
    t = text.lower()
    return [kw for kw in FP_KEYWORDS if kw in t]

def ensure_columns(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(pages)")
    cols = [c[1] for c in cur.fetchall()]

    if "fingerprinting" not in cols:
        cur.execute("ALTER TABLE pages ADD COLUMN fingerprinting INTEGER DEFAULT 0")
    if "fp_keywords" not in cols:
        cur.execute("ALTER TABLE pages ADD COLUMN fp_keywords TEXT")
    if "fp_last_seen" not in cols:
        cur.execute("ALTER TABLE pages ADD COLUMN fp_last_seen TEXT")
    if "fp_third_parties" not in cols:
        cur.execute("ALTER TABLE pages ADD COLUMN fp_third_parties TEXT")
    conn.commit()

def get_pages_domains(conn: sqlite3.Connection) -> set[str]:
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT domain FROM pages WHERE domain IS NOT NULL AND domain <> ''")
    return {norm_domain(r[0]) for r in cur.fetchall()}

def update_page(conn: sqlite3.Connection, page_domain: str, fp_third_parties: set[str], fp_keywords: set[str]):
    now_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    cur = conn.cursor()

    # Merge s postojećim vrijednostima (da se ne izgubi raniji upis)
    cur.execute("SELECT fp_keywords, fp_third_parties FROM pages WHERE domain = ? LIMIT 1", (page_domain,))
    row = cur.fetchone()

    old_kw, old_tp = set(), set()
    if row:
        if row[0]:
            old_kw = {x.strip() for x in row[0].split(",") if x.strip()}
        if row[1]:
            old_tp = {x.strip() for x in row[1].split(",") if x.strip()}

    merged_kw = sorted(old_kw.union(fp_keywords))
    merged_tp = sorted(old_tp.union(fp_third_parties))

    cur.execute(
        """
        UPDATE pages
        SET fingerprinting = 1,
            fp_keywords = ?,
            fp_third_parties = ?,
            fp_last_seen = ?
        WHERE domain = ?
        """,
        (", ".join(merged_kw), ", ".join(merged_tp), now_utc, page_domain),
    )
    conn.commit()

def main():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Ne mogu naci bazu: {DB_PATH}")
    if not os.path.exists(MITM_PATH):
        raise FileNotFoundError(f"Ne mogu naci mitm datoteku: {MITM_PATH}")

    conn = sqlite3.connect(DB_PATH)
    ensure_columns(conn)
    pages_domains = get_pages_domains(conn)

    # 1) Detektiraj FP tracker domene (gdje u HTML/JS responseu ima FP keyworda)
    fp_tracker_to_keywords: dict[str, set[str]] = {}
    total_flows = 0
    scanned_html_js = 0

    with open(MITM_PATH, "rb") as f:
        reader = io.FlowReader(f)
        for flow in reader.stream():
            if not isinstance(flow, HTTPFlow):
                continue
            total_flows += 1
            if not flow.response:
                continue

            ct = flow.response.headers.get("content-type", "").lower()
            if ("javascript" not in ct) and ("text/html" not in ct):
                continue

            try:
                body = flow.response.get_text(strict=False)
            except Exception:
                continue

            scanned_html_js += 1
            hits = detect_keywords(body)
            if hits:
                tracker = norm_domain(netloc(flow.request.pretty_url))
                if tracker:
                    fp_tracker_to_keywords.setdefault(tracker, set()).update(hits)

    fp_trackers = set(fp_tracker_to_keywords.keys())

    # 2) Mapiraj FP trackere na "pages" preko Referer ILI Origin
    page_to_fp_trackers: dict[str, set[str]] = {}
    page_to_keywords: dict[str, set[str]] = {}

    referer_present = 0
    origin_present = 0
    mapped_hits = 0

    with open(MITM_PATH, "rb") as f:
        reader = io.FlowReader(f)
        for flow in reader.stream():
            if not isinstance(flow, HTTPFlow):
                continue

            tracker = norm_domain(netloc(flow.request.pretty_url))
            if tracker not in fp_trackers:
                continue

            ref = flow.request.headers.get("referer", "")
            org = flow.request.headers.get("origin", "")

            if ref:
                referer_present += 1
            if org:
                origin_present += 1

            page_dom = ""
            if ref:
                page_dom = norm_domain(netloc(ref))
            elif org:
                page_dom = norm_domain(netloc(org))

            if page_dom and page_dom in pages_domains:
                page_to_fp_trackers.setdefault(page_dom, set()).add(tracker)
                page_to_keywords.setdefault(page_dom, set()).update(fp_tracker_to_keywords.get(tracker, set()))
                mapped_hits += 1

    # 3) Fallback: ako je FP detektiran na domeni koja je sama "page", označi ju
    for tracker, kws in fp_tracker_to_keywords.items():
        if tracker in pages_domains:
            page_to_fp_trackers.setdefault(tracker, set()).add(tracker)
            page_to_keywords.setdefault(tracker, set()).update(kws)

    # 4) Upis u pages
    marked = 0
    for page_dom, trackers in page_to_fp_trackers.items():
        kws = page_to_keywords.get(page_dom, set())
        update_page(conn, page_dom, trackers, kws)
        marked += 1

    conn.close()

    # 5) Log u results/logs
    os.makedirs("results/logs", exist_ok=True)
    out_path = os.path.join("results", "logs", "fingerprinting_findings.json")
    with open(out_path, "w", encoding="utf-8") as fp:
        json.dump(
            {
                "total_flows": total_flows,
                "scanned_html_js": scanned_html_js,
                "fp_trackers_detected": [
                    {"domain": d, "keywords": sorted(list(kws))}
                    for d, kws in sorted(fp_tracker_to_keywords.items(), key=lambda x: x[0])
                ],
                "mapping_stats": {
                    "referer_present": referer_present,
                    "origin_present": origin_present,
                    "mapped_hits": mapped_hits,
                    "pages_marked": marked,
                },
                "pages_marked": [
                    {
                        "page_domain": pd,
                        "fp_third_parties": sorted(list(page_to_fp_trackers.get(pd, set()))),
                        "keywords": sorted(list(page_to_keywords.get(pd, set()))),
                    }
                    for pd in sorted(page_to_fp_trackers.keys())
                ],
            },
            fp,
            indent=2,
            ensure_ascii=False,
        )

    print("ZAVRŠENO")
    print(f"Ukupno flowova: {total_flows}")
    print(f"Skenirano (HTML/JS): {scanned_html_js}")
    print(f"FP tracker domene detektirane: {len(fp_trackers)}")
    print(f"Referer prisutan u: {referer_present} zahtjeva (prema FP trackerima)")
    print(f"Origin prisutan u: {origin_present} zahtjeva (prema FP trackerima)")
    print(f"Mapirano (pogodaka) preko Referer/Origin: {mapped_hits}")
    print(f"Pages oznacene fingerprinting=1: {marked}")
    print(f"Log spremljen u: {out_path}")

if __name__ == "__main__":
    main()
