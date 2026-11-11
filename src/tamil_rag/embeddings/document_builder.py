from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parents[3]

THIRUKKURAL_FILE = (
    BASE_DIR / "data" / "processed" / "thirukkural"
    / "thirukkural_normalized.json"
)

THIRUVARUTPA_FILE = (
    BASE_DIR / "data" / "processed" / "thiruvarutpa"
    / "thiruvarutpa_normalized.json"
)


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_thirukkural_documents():
    data = load_json(THIRUKKURAL_FILE)

    records = data["records"] if isinstance(data, dict) else data

    documents = []

    for record in records:
        documents.append(
            {
                "source_id": f"thirukkural_{record['kural_number']}",
                "source_type": "thirukkural",
                "text": record["normalized_text"],
                "metadata": {
                    "work": record["work"],
                    "kural_number": record["kural_number"],
                    "chapter_number": record["chapter_number"],
                    "source": record.get("source", ""),
                },
            }
        )

    return documents


def build_thiruvarutpa_documents():
    records = load_json(THIRUVARUTPA_FILE)

    documents = []

    for record in records:
        documents.append(
            {
                "source_id": f"thiruvarutpa_{record['verse_number']}",
                "source_type": "thiruvarutpa",
                "text": record["normalized_text"],
                "metadata": {
                    "work": record["work"],
                    "tirmurai": record.get("tirmurai", ""),
                    "verse_number": record["verse_number"],
                },
            }
        )

    return documents


if __name__ == "__main__":
    thirukkural = build_thirukkural_documents()
    thiruvarutpa = build_thiruvarutpa_documents()

    documents = thirukkural + thiruvarutpa

    output_file = (
        BASE_DIR / "data" / "processed" / "embedding_documents.json"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)

    print("Thirukkural documents:", len(thirukkural))
    print("Thiruvarutpa documents:", len(thiruvarutpa))
    print("Total documents:", len(documents))
    print("Saved to:", output_file)