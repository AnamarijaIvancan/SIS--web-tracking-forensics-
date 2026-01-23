import sqlite3
import json
from datetime import datetime

DB_PATH = "cookies.db"

FACEBOOK_DOMAINS = [
    "facebook.com",
    "connect.facebook.net",
    "fbcdn.net",
    "meta.com"
]

KEYWORD_TO_DATA = {
    "canvas": "Grafički fingerprint (canvas rendering)",
    "webgl": "GPU / grafički driver",
    "audiocontext": "Audio fingerprint",
    "navigator.language": "Jezik korisnika",
    "navigator.languages": "Jezici sustava",
    "screen.width": "Rezolucija ekrana",
    "screen.height": "Rezolucija ekrana",
    "devicepixelratio": "Gustoća piksela (DPI)",
    "navigator.hardwareconcurrency": "Broj CPU jezgri",
    "navigator.devicememory": "Količina RAM memorije",
    "enumeratedevices": "Popis audio/video uređaja"
}

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT domain, fp_keywords, fp_third_parties
        FROM pages
        WHERE fingerprinting = 1
    """)

    findings = []

    for domain, keywords, third_parties in cur.fetchall():
        if not third_parties:
            continue

        if any(fb in third_parties for fb in FACEBOOK_DOMAINS):
            data_access = set()
            for k, v in KEYWORD_TO_DATA.items():
                if keywords and k in keywords:
                    data_access.add(v)

            findings.append({
                "page": domain,
                "facebook_third_parties": third_parties,
                "fingerprinting_keywords": keywords,
                "facebook_can_access": list(data_access)
            })

    conn.close()

    report = {
        "generated": datetime.utcnow().isoformat(),
        "facebook_fingerprinting_pages": len(findings),
        "findings": findings
    }

    with open("facebook_fingerprinting_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"[OK] Facebook fingerprinting pages: {len(findings)}")

if __name__ == "__main__":
    main()
