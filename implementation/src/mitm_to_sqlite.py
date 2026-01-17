import sqlite3
import tldextract
from mitmproxy import http, io
from urllib.parse import urlparse

DB_NAME = "cookies.db"
MITM_FILE = "traffic.mitm"

def get_domain(host):
    ext = tldextract.extract(host)
    return ext.registered_domain or ""

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS pages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        domain TEXT UNIQUE,
        fingerprinting INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS cookies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        page_id INTEGER,
        name TEXT,
        domain TEXT,
        path TEXT,
        secure INTEGER,
        httponly INTEGER,
        is_third_party INTEGER,
        expires TEXT
    );

    CREATE TABLE IF NOT EXISTS trackers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        domain TEXT UNIQUE,
        category TEXT
    );

    CREATE TABLE IF NOT EXISTS mapping (
        page_id INTEGER,
        tracker_id INTEGER,
        interaction_count INTEGER DEFAULT 1,
        PRIMARY KEY (page_id, tracker_id)
    );
    """)

    conn.commit()
    return conn

def is_html_page(flow):
    content_type = flow.response.headers.get("Content-Type", "")
    return "text/html" in content_type.lower()

def normalize_page(url):
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}"

def parse_mitm():
    conn = init_db()
    cur = conn.cursor()

    with open(MITM_FILE, "rb") as f:
        reader = io.FlowReader(f)

        for flow in reader.stream():
            if not isinstance(flow, http.HTTPFlow):
                continue
            if not flow.response:
                continue

            page_url = normalize_page(flow.request.url)
            page_domain = get_domain(flow.request.host)

            # PAGE – UNIQUE PO DOMENI
            cur.execute("""
                INSERT OR IGNORE INTO pages (url, domain)
                VALUES (?, ?)
            """, (page_url, page_domain))

            cur.execute(
                "SELECT id FROM pages WHERE domain=?",
                (page_domain,)
            )
            page_id = cur.fetchone()[0]

            # COOKIES
            cookies = flow.response.headers.get_all("Set-Cookie")
            for raw in cookies:
                parts = [p.strip() for p in raw.split(";")]
                name = parts[0].split("=", 1)[0]

                cookie_domain = page_domain
                path = ""
                secure = 0
                httponly = 0
                expires = ""

                for p in parts[1:]:
                    pl = p.lower()
                    if pl.startswith("domain="):
                        cookie_domain = get_domain(p.split("=", 1)[1])
                    elif pl.startswith("path="):
                        path = p.split("=", 1)[1]
                    elif pl == "secure":
                        secure = 1
                    elif pl == "httponly":
                        httponly = 1
                    elif pl.startswith("expires="):
                        expires = p.split("=", 1)[1]

                is_third = 1 if cookie_domain != page_domain else 0

                cur.execute("""
                    INSERT INTO cookies
                    (page_id, name, domain, path, secure, httponly, is_third_party, expires)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    page_id, name, cookie_domain, path,
                    secure, httponly, is_third, expires
                ))

                # TRACKERS + MAPPING
                if is_third:
                    cur.execute(
                        "INSERT OR IGNORE INTO trackers (domain, category) VALUES (?, 'unknown')",
                        (cookie_domain,)
                    )

                    cur.execute(
                        "SELECT id FROM trackers WHERE domain=?",
                        (cookie_domain,)
                    )
                    tracker_id = cur.fetchone()[0]

                    cur.execute("""
                        INSERT INTO mapping (page_id, tracker_id, interaction_count)
                        VALUES (?, ?, 1)
                        ON CONFLICT(page_id, tracker_id)
                        DO UPDATE SET interaction_count = interaction_count + 1
                    """, (page_id, tracker_id))

            conn.commit()

    conn.close()
    print("✔ SQLite baza s filtriranim Pages tablicama uspješno kreirana")

if __name__ == "__main__":
    parse_mitm()