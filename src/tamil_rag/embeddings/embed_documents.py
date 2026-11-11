from pathlib import Path
import json

import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parents[3]

INPUT_FILE = BASE_DIR / "data" / "processed" / "embedding_documents.json"
INDEX_DIR = BASE_DIR / "indexes" / "tamil"

EMBEDDING_FILE = INDEX_DIR / "embeddings.npy"
METADATA_FILE = INDEX_DIR / "metadata.json"

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


def load_documents():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    documents = load_documents()

    print("Documents loaded:", len(documents))

    model = SentenceTransformer(MODEL_NAME)

    texts = [document["text"] for document in documents]

    print("Generating embeddings...")

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    print("Embedding shape:", embeddings.shape)
    print("Embedding dtype:", embeddings.dtype)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    np.save(EMBEDDING_FILE, embeddings)

    metadata = [
        {
            "source_id": document["source_id"],
            "source_type": document["source_type"],
            "text": document["text"],
            "metadata": document["metadata"],
        }
        for document in documents
    ]

    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print("Embeddings saved to:", EMBEDDING_FILE)
    print("Metadata saved to:", METADATA_FILE)


if __name__ == "__main__":
    main()