from pathlib import Path
import json
import re

from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "thiruvarutpa"
    / "projectmadurai_thiruvarutpa_thirumurai1.html"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "thiruvarutpa"
    / "thiruvarutpa_raw.json"
)


# Known section numbers appearing in this source.
# These are headings, not verse numbers.
SECTION_NUMBERS = set(range(1, 46))


def load_lines():
    html = SOURCE_FILE.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text("\n").splitlines()


def is_section_heading(line):
    """
    Detect headings such as:
        1. சென்னைக் கந்தகோட்டம்
        30. புண்ணியநீற்று மான்மியம்
        45. செவி அறிவுறுத்தல்
    """
    match = re.match(r"^\s*(\d+)\.\s+\S", line)

    if not match:
        return False

    number = int(match.group(1))

    return number in SECTION_NUMBERS


def extract_verse_marker(line):
    # Format 1:
    # 46.
    # 505. Tamil text
    match = re.match(r"^\s*(\d+)\.\s*(.*)$", line)
    if match:
        number = int(match.group(1))
        text = match.group(2).strip()

        # A numbered line with text is a section heading
        # only when it is one of the known section-heading numbers.
        # Actual verses such as 46. can have no text on the marker line.
        if number <= 52 and text:
            return None

        return number, text

    # Format 2:
    # 493 Tamil text
    # 494 Tamil text
    # Used by part of the source around verses 493-504.
    match = re.match(r"^\s*(\d+)\s+(\S.*)$", line)
    if match:
        number = int(match.group(1))
        text = match.group(2).strip()

        # Section headings have a period after the number,
        # so this no-period format is treated as a verse.
        return number, text

    return None


def extract_entries(lines):
    entries = []
    current = None

    for line in lines:
        stripped = line.strip()

        # Stop before webpage footer.
        if stripped.startswith("This webpage was revised"):
            break

        marker = extract_verse_marker(line)

        if marker is not None:
            verse_number, first_text = marker

            # Save previous verse.
            if current is not None:
                current["tamil_text"] = "\n".join(
                    current["text_lines"]
                ).strip()

                del current["text_lines"]

                if current["tamil_text"]:
                    entries.append(current)

            current = {
                "work": "Thiruvarutpa",
                "tirmurai": "I",
                "verse_number": verse_number,
                "text_lines": [],
            }

            if first_text:
                current["text_lines"].append(first_text)

            continue

        # Ignore everything before the first actual verse.
        if current is None:
            continue

               # Skip obvious section metadata and separators.
        if (
            stripped == ""
            or stripped == "திருச்சிற்றம்பலம்"
            or re.fullmatch(r"-{3,}", stripped)
        ):
            continue

        current["text_lines"].append(stripped)

    # Save final verse.
    if current is not None:
        current["tamil_text"] = "\n".join(
            current["text_lines"]
        ).strip()

        del current["text_lines"]

        if current["tamil_text"]:
            entries.append(current)

    return entries


def main():
    lines = load_lines()
    entries = extract_entries(lines)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_FILE.write_text(
        json.dumps(
            entries,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Extracted records: {len(entries)}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()