import json
import unicodedata
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm

INPUT_JSON = "facebook_fingerprinting_report.json"
OUTPUT_PDF = "facebook_fingerprinting_report.pdf"

def strip_diacritics(text: str) -> str:
    if not text:
        return ""
    # RUCNA MAPA ZA PROBLEMATICNA SLOVA
    replacements = {
        "đ": "d",
        "Đ": "D",
        "č": "c",
        "Č": "C",
        "ć": "c",
        "Ć": "C",
        "š": "s",
        "Š": "S",
        "ž": "z",
        "Ž": "Z",
    }

    for src, dst in replacements.items():
        text = text.replace(src, dst)

    # fallback za sve ostalo
    import unicodedata
    return "".join(
        c for c in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(c)
    )

def main():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="SectionTitle",
        fontSize=14,
        spaceBefore=12,
        spaceAfter=6,
        leading=18,
        fontName="Helvetica-Bold"
    ))

    styles.add(ParagraphStyle(
        name="Body",
        fontSize=10,
        leading=14,
        spaceAfter=6
    ))

    story = []

    findings = data.get("findings", [])

    for entry in findings:
        story.append(Paragraph(
            strip_diacritics(f"Stranica: <b>{entry.get('page')}</b>"),
            styles["SectionTitle"]
        ))

        story.append(Paragraph(
            strip_diacritics(
                "<b>Third-party resursi stranice (Facebook prisutan):</b><br/>"
                + entry.get("facebook_third_parties", "")
            ),
            styles["Body"]
        ))

        story.append(Paragraph(
            strip_diacritics(
                "<b>Detektirane fingerprinting tehnike:</b><br/>"
                + entry.get("fingerprinting_keywords", "")
            ),
            styles["Body"]
        ))

        access = entry.get("facebook_can_access", [])
        if access:
            story.append(Paragraph(
                strip_diacritics(
                    "<b>Potencijalni fingerprinting podaci dostupni Facebook skripti:</b><br/>"
                    + ", ".join(access)
                ),
                styles["Body"]
            ))

        story.append(Spacer(1, 12))

    doc.build(story)
    print(f"✔ PDF izvjestaj kreiran: {OUTPUT_PDF}")

if __name__ == "__main__":
    main()