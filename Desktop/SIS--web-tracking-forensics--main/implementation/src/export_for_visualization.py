import json
import os
import sqlite3
from collections import defaultdict

DB_PATH = os.path.join(os.getcwd(), "cookies.db")

def norm(d: str) -> str:
    d = (d or "").strip().lower()
    if d.startswith("www."):
        d = d[4:]
    return d

def main():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Ne mogu naci bazu: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Uzmemo SAMO stvarne visited pages koje su oznacene fingerprinting=1
    cur.execute("""
        SELECT domain, fp_third_parties
        FROM pages
        WHERE fingerprinting = 1
          AND domain IS NOT NULL AND domain <> ''
    """)
    rows = cur.fetchall()

    # set svih page domena (da ih možemo razlikovati od trackera)
    page_set = {norm(r[0]) for r in rows if norm(r[0])}

    conn.close()

    nodes = {}
    links = []
    tracker_counts = defaultdict(int)
    tracker_used_on_pages = defaultdict(set)

    def add_node(node_id: str, node_type: str):
        if node_id not in nodes:
            nodes[node_id] = {"id": node_id, "type": node_type}

    for page_domain, fp_tp in rows:
        page = norm(page_domain)
        if not page:
            continue

        # page node
        add_node(page, "page")

        # third parties
        tp_list = []
        if fp_tp:
            tp_list = [norm(x) for x in fp_tp.split(",") if norm(x)]

        for tp in tp_list:
            if not tp:
                continue

            # 1) makni self-link (page -> page)
            if tp == page:
                continue

            # 2) ako se tracker domena slucajno nalazi u page_set, NE tretiraj ju kao page u grafu
            #    (u grafu ju želimo kao tracker)
            add_node(tp, "tracker")
            links.append({"source": page, "target": tp})

            tracker_counts[page] += 1
            tracker_used_on_pages[tp].add(page)

    # Bar chart: samo za PAGES (ne za trackere)
    bar = [{"page": p, "tracker_count": c} for p, c in tracker_counts.items()]
    bar.sort(key=lambda x: x["tracker_count"], reverse=True)

    stats = {
        "pages_with_fp": len(tracker_counts),
        "unique_trackers": len([n for n in nodes.values() if n["type"] == "tracker"]),
        "total_links": len(links),
    }

    # Dodaj i tracker stats (koliko stranica koristi tracker)
    tracker_stats = [
        {"tracker": t, "pages_count": len(pages)}
        for t, pages in tracker_used_on_pages.items()
    ]
    tracker_stats.sort(key=lambda x: x["pages_count"], reverse=True)

    os.makedirs("results/visualization", exist_ok=True)
    out_path = os.path.join("results", "visualization", "graph_data.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "nodes": list(nodes.values()),
                "links": links,
                "bar": bar,
                "stats": stats,
                "tracker_stats": tracker_stats
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print("OK: export završio")
    print(f"Spremio: {out_path}")
    print(f"Stats: {stats}")
    if tracker_stats:
        print("Top trackers by pages covered:")
        for x in tracker_stats[:10]:
            print(f" - {x['tracker']}: {x['pages_count']} pages")

if __name__ == "__main__":
    main()
