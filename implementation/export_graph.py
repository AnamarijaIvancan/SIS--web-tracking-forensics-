import json, os
from datetime import datetime, timezone

FB_JSON = "facebook_third_party_pages.json"
OUT_DIR = os.path.join("results", "visualization")
OUT_PATH = os.path.join(OUT_DIR, "graph.json")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    with open(FB_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    nodes = {}
    links = []

    def add_node(node_id, label, node_type):
        if node_id not in nodes:
            nodes[node_id] = {"id": node_id, "label": label, "type": node_type}

    for hit in data.get("hits", []):
        page = hit.get("page")
        markers = hit.get("facebook_markers_found", [])
        if not page or not markers:
            continue

        site_id = f"site:{page}"
        add_node(site_id, page, "site")

        for m in markers:
            tr_id = f"tracker:{m}"
            add_node(tr_id, m, "tracker")
            links.append({"source": site_id, "target": tr_id, "weight": 1})

    out = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "total_pages_with_facebook_third_party": data.get("total_pages_with_facebook_third_party", 0),
        "nodes": list(nodes.values()),
        "links": links
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"[OK] Written {OUT_PATH}")
    print(f"Nodes: {len(out['nodes'])}, Links: {len(out['links'])}")

if __name__ == "__main__":
    main()
