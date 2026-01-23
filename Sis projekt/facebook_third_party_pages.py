import sqlite3
import json
from datetime import datetime, timezone

DB_PATH = "cookies.db"

# Facebook/Meta infrastruktura koja se učitava na drugim stranicama
FB_MARKERS = [
    "facebook.com",
    "connect.facebook.net",
    "static.xx.fbcdn.net",
    "fbcdn.net",
    "facebook.com/tr",          
    "graph.facebook.com",
    "www.facebook.com/tr"
]

# Domene koje NE želimo brojati kao "third-party site"
EXCLUDE_PAGES = [
    "facebook.com",
    "fbsbx.com",
    "fb.com",
    "messenger.com"
]

def is_excluded(page_domain: str) -> bool:
    return any(page_domain == d or page_domain.endswith("." + d) for d in EXCLUDE_PAGES)

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Pretpostavka: pages ima fp_third_parties i fingerprinting flag/keywords
    cur.execute("""
        SELECT domain, fingerprinting, fp_third_parties, fp_keywords
        FROM pages
        WHERE fp_third_parties IS NOT NULL AND fp_third_parties != ''
    """)

    rows = cur.fetchall()
    conn.close()

    hits = []
    for domain, fingerprinting, third_parties, keywords in rows:
        if not domain:
            continue
        if is_excluded(domain):
            continue

        tp = third_parties.lower()
        if any(marker in tp for marker in FB_MARKERS):
            hits.append({
                "page": domain,
                "fingerprinting": int(fingerprinting) if fingerprinting is not None else 0,
                "facebook_markers_found": [m for m in FB_MARKERS if m in tp],
                "fp_third_parties": third_parties,
                "fp_keywords": keywords or ""
            })

    # Sort: prvo fingerprinting=1 pa po domeni
    hits.sort(key=lambda x: (-x["fingerprinting"], x["page"]))

    report = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "total_pages_with_facebook_third_party": len(hits),
        "hits": hits
    }

    out_path = "facebook_third_party_pages.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"[OK] Pages where Facebook appears as 3rd-party: {len(hits)}")
    if hits:
        print("Top examples:")
        for h in hits[:10]:
            print(f" - {h['page']}  (fingerprinting={h['fingerprinting']})")

if __name__ == "__main__":
    main()
