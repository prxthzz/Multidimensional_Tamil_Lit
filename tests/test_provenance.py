from shared.schemas.tamil_retrieval import TamilRetrievalRequest
from src.tamil_rag.retrieval.semantic_retriever import SemanticTamilRetriever


def main():
    retriever = SemanticTamilRetriever(top_k=3)

    request = TamilRetrievalRequest(
        query_terms=["அறிவு"],
        retrieval_reason="Provenance test",
    )

    results = retriever.retrieve(request)

    for result in results:
        print("\nSource ID:", result.source_id)
        print("Source Type:", result.source_type)
        print("Text:", result.text)
        print("Score:", result.retrieval_score)
        print("Metadata:", result.metadata)


if __name__ == "__main__":
    main()