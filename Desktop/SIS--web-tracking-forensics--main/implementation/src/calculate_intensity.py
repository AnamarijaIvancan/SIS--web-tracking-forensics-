import sqlite3
import json

DB_NAME = "cookies.db"

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()


cur.execute("PRAGMA table_info(pages)")
if not any(c[1] == 'intensity_score' for c in cur.fetchall()):
    cur.execute("ALTER TABLE pages ADD COLUMN intensity_score INTEGER DEFAULT 0")

cur.execute("SELECT id FROM pages")
page_ids = [row[0] for row in cur.fetchall()]

for page_id in page_ids:
    trackers = cur.execute("SELECT COUNT(DISTINCT tracker_id) FROM mapping WHERE page_id = ?", (page_id,)).fetchone()[0] or 0
    third_cookies = cur.execute("SELECT COUNT(*) FROM cookies WHERE page_id = ? AND is_third_party = 1", (page_id,)).fetchone()[0] or 0
    fp = cur.execute("SELECT fingerprinting FROM pages WHERE id = ?", (page_id,)).fetchone()[0] or 0
    score = trackers + third_cookies + (fp * 10)
    
    cur.execute("UPDATE pages SET intensity_score = ? WHERE id = ?", (score, page_id))
    domain = cur.execute("SELECT domain FROM pages WHERE id = ?", (page_id,)).fetchone()[0]
    print(f"{domain}: score={score}, trackers={trackers}, 3rd={third_cookies}, FP={fp}")

cur.execute("SELECT domain, intensity_score, fingerprinting FROM pages ORDER BY intensity_score DESC")
results = [{"domain": r[0], "score": r[1], "fp": r[2]} for r in cur.fetchall()]
with open("intensity_scores.json", "w") as f:
    json.dump(results, f, indent=2)

conn.commit()
conn.close()
print("✔ Intensity score gotov! Pogledaj intensity_scores.json")
