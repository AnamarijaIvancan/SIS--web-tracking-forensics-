import sqlite3

conn = sqlite3.connect('cookies.db')
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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

-- Test podaci
INSERT OR IGNORE INTO pages (domain, fingerprinting) VALUES 
('vecernji.hr', 2), ('dan.co.me', 2), ('vijesti.me', 1);

INSERT OR IGNORE INTO trackers (domain) VALUES 
('connect.facebook.net'), ('googletagmanager.com'), ('doubleclick.net');

-- Mapping s 3 kolone
INSERT OR IGNORE INTO mapping (page_id, tracker_id, interaction_count) VALUES 
(1,1,3), (1,2,2), (1,3,1),  -- vecernji.hr
(2,1,2), (2,2,1);            -- dan.co.me

-- Test 3rd party cookies
INSERT INTO cookies (page_id, name, domain, is_third_party) VALUES 
(1, '_ga', 'google.com', 1);
""")

conn.commit()
conn.close()
print("✔ Test baza spremna!")
print("Pokreni: python categorize_trackers.py && python calculate_intensity.py")
