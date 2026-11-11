from pathlib import Path

import json
import re
from html import unescape

from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "thirukkural"
    / "projectmadurai_thirukkural.html"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "processed"
    / "thirukkural"
)

OUTPUT_FILE = OUTPUT_DIR / "thirukkural_raw.json"


def clean_text(text: str) -> str:
    """Clean HTML entities and whitespace."""
    text = unescape(text)
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_kurals(html: str):
    soup = BeautifulSoup(html, "html.parser")

    # Convert every <br> into a real newline.
    for br in soup.find_all("br"):
        br.replace_with("\n")

    # Get the logical text lines from the HTML.
    text = soup.get_text("\n")

    lines = []

    for line in text.splitlines():
        line = clean_text(line)

        if line:
            lines.append(line)

    records = []
    seen_numbers = set()

    for index, line in enumerate(lines):

        # A Kural number normally appears at the end
        # of its second line.
        match = re.search(r"(\d{1,5})$", line)

        kural_number = None

        if match:
            kural_number = int(match.group(1))

        # We need a previous line for the first line
        # of the Kural.
        if index < 1:
            continue

        line1 = lines[index - 1]

        # Avoid headings / chapter identifiers.
        if re.search(r"\d+\.\d+(?:\.\d+)?$", line1):
            continue

        # ---------------------------------------------------------
        # Known Project Madurai source-numbering corrections
        # ---------------------------------------------------------

        # Kural 72
        if line1.startswith("அன்பிலார் எல்லாம் தமக்குரியர்"):
            kural_number = 72

        # Kural 753
        elif line1.startswith("பொருளென்னும் பொய்யா விளக்கம்"):
            kural_number = 753

        # Kural 781
        elif line1.startswith("செயற்கரிய யாவுள நட்பின்"):
            kural_number = 781

        # Kural 1293
        elif line1.startswith("கெட்டார்க்கு நட்டார்இல்"):
            kural_number = 1293

        # No usable Kural number.
        if kural_number is None:
            continue

        # Only accept valid Kural numbers.
        if not 1 <= kural_number <= 1330:
            continue

        # Remove the source number from the second line.
        if match:
            line2 = line[:match.start()].strip()
        else:
            line2 = line

        if not line1 or not line2:
            continue

        # Avoid duplicate corrected numbers.
        if kural_number in seen_numbers:
            continue

        # Derive chapter number from Kural number.
        chapter_number = (kural_number - 1) // 10 + 1

        record = {
            "work": "Thirukkural",
            "kural_number": kural_number,
            "chapter_number": chapter_number,
            "tamil_text": f"{line1}\n{line2}",
            "source": "Project Madurai",
        }

        records.append(record)
        seen_numbers.add(kural_number)

    records.sort(key=lambda record: record["kural_number"])

    return records


def main():

    if not SOURCE_FILE.exists():
        raise FileNotFoundError(
            f"Source file not found: {SOURCE_FILE}"
        )

    html = SOURCE_FILE.read_text(encoding="utf-8")

    records = extract_kurals(html)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    data = {
        "work": "Thirukkural",
        "source": "Project Madurai",
        "source_file": "projectmadurai_thirukkural.html",
        "encoding": "UTF-8",
        "records": records,
    }

    OUTPUT_FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    numbers = {
        record["kural_number"]
        for record in records
    }

    missing = [
        number
        for number in range(1, 1331)
        if number not in numbers
    ]

    duplicates = len(records) - len(numbers)

    print(f"Extracted records: {len(records)}")
    print(f"Unique Kural numbers: {len(numbers)}")
    print(f"Duplicates: {duplicates}")
    print(f"Missing Kurals: {missing}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()