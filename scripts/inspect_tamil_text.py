from pathlib import Path
import json
import unicodedata
from collections import Counter


BASE_DIR = Path(__file__).resolve().parent.parent

DATASETS = {
    "Thirukkural": (
        BASE_DIR
        / "data"
        / "processed"
        / "thirukkural"
        / "thirukkural_raw.json"
    ),
    "Thiruvarutpa": (
        BASE_DIR
        / "data"
        / "processed"
        / "thiruvarutpa"
        / "thiruvarutpa_raw.json"
    ),
}


def get_records(data):
    if isinstance(data, dict) and "records" in data:
        return data["records"]

    if isinstance(data, list):
        return data

    raise ValueError("Unsupported dataset structure")


def inspect_text(text):
    counters = {
        "zero_width": 0,
        "non_breaking_space": 0,
        "control": 0,
        "unusual_whitespace": 0,
        "tamil_characters": 0,
    }

    unusual_chars = Counter()

    for char in text:
        code = ord(char)

        if char in {"\u200b", "\u200c", "\u200d", "\ufeff"}:
            counters["zero_width"] += 1
            unusual_chars[char] += 1

        elif char == "\u00a0":
            counters["non_breaking_space"] += 1
            unusual_chars[char] += 1

        elif unicodedata.category(char) == "Cc":
            counters["control"] += 1
            unusual_chars[char] += 1

        elif char.isspace() and char not in {" ", "\n", "\t"}:
            counters["unusual_whitespace"] += 1
            unusual_chars[char] += 1

        if 0x0B80 <= code <= 0x0BFF:
            counters["tamil_characters"] += 1

    return counters, unusual_chars


def main():
    for dataset_name, path in DATASETS.items():
        print("=" * 60)
        print(dataset_name)
        print("=" * 60)

        data = json.loads(path.read_text(encoding="utf-8"))
        records = get_records(data)

        combined_text = "\n".join(
            record["tamil_text"]
            for record in records
            if record.get("tamil_text")
        )

        print("Records:", len(records))
        print("Characters:", len(combined_text))

        for form in ["NFC", "NFD", "NFKC", "NFKD"]:
            normalized = unicodedata.normalize(form, combined_text)
            print(
                f"{form} identical:",
                normalized == combined_text,
            )

        counters, unusual_chars = inspect_text(combined_text)

        print("\nCharacter inspection:")
        for key, value in counters.items():
            print(f"{key}: {value}")

        print("\nUnusual characters:")

        if unusual_chars:
            for char, count in unusual_chars.most_common():
                print(
                    repr(char),
                    f"U+{ord(char):04X}",
                    unicodedata.name(char, "UNKNOWN"),
                    "count=",
                    count,
                )
        else:
            print("None")

        print()


if __name__ == "__main__":
    main()