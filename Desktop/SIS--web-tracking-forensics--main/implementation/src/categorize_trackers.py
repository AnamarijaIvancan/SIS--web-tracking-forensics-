import sqlite3

DB_NAME = "cookies.db"

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

categories = {
    'facebook.com': 'social',
    'connect.facebook.net': 'social',
    'static.xx.fbcdn.net': 'social',
    'google.com': 'analytics',
    'googletagmanager.com': 'analytics',
    'gstatic.com': 'analytics',
    'accounts.google.com': 'analytics',
    'pagead2.googlesyndication.com': 'advertising',
    'securepubads.g.doubleclick.net': 'advertising',
    'instagram.com': 'social',
    'platform.twitter.com': 'social',
}

for domain, cat in categories.items():
    cur.execute("UPDATE trackers SET category = ? WHERE domain LIKE ?", (cat, f'%{domain}%'))

conn.commit()
conn.close()
print("✔ Trackers kategorizirani!")
print("Provjeri: sqlite3 cookies.db 'SELECT domain, category FROM trackers LIMIT 5;'")
