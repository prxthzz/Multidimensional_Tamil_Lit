from pathlib import Path
import json

from src.tamil_rag.preprocessing.normalizer import normalize_tamil_text


BASE_DIR = Path(__file__).resolve().parent.parent

DATASETS = {
    "thirukkural": {
        "input": (
            BASE_DIR
            / "data"
            / "processed"
            / "thirukkural"
            / "thirukkural_raw.json"
        ),
        "output": (
            BASE_DIR
            / "data"
            / "processed"
            / "thirukkural"
            / "thirukkural_normalized.json"
        ),
    },
    "thiruvarutpa": {
        "input": (
            BASE_DIR
            / "data"
            / "processed"
            / "thiruvarutpa"
            / "thiruvarutpa_raw.json"
        ),
        "output": (
            BASE_DIR
            / "data"
            / "processed"
            / "thiruvarutpa"
            / "thiruvarutpa_normalized.json"
        ),
    },
}


def load_records(data):
    if isinstance(data, dict) and "records" in data:
        return data["records"]

    if isinstance(data, list):
        return data

    raise ValueError("Unsupported dataset structure")


def normalize_records(records):
    normalized_records = []

    for record in records:
        new_record = dict(record)

        original_text = record.get("tamil_text", "")

        new_record["normalized_text"] = normalize_tamil_text(
            original_text
        )

        normalized_records.append(new_record)

    return normalized_records


def main():
    for dataset_name, config in DATASETS.items():
        data = json.loads(
            config["input"].read_text(encoding="utf-8")
        )

        records = load_records(data)
        normalized_records = normalize_records(records)

        if isinstance(data, dict):
            output_data = dict(data)
            output_data["records"] = normalized_records
        else:
            output_data = normalized_records

        config["output"].parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        config["output"].write_text(
            json.dumps(
                output_data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        print(
            f"{dataset_name}: "
            f"{len(normalized_records)} records"
        )
        print(f"Output: {config['output']}")


if __name__ == "__main__":
    main()