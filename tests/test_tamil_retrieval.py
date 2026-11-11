from shared.schemas.tamil_retrieval import TamilRetrievalRequest
from src.tamil_rag.retrieval.semantic_retriever import SemanticTamilRetriever


def main():
    retriever = SemanticTamilRetriever(top_k=5)

    request = TamilRetrievalRequest(
        query_terms=["அறிவு"],
        retrieval_reason="Test Tamil semantic retrieval",
    )

    results = retriever.retrieve(request)

    print("Results:", len(results))

    for result in results:
        print("\nSource ID:", result.source_id)
        print("Source type:", result.source_type)
        print("Score:", result.retrieval_score)
        print("Text:", result.text)


if __name__ == "__main__":
    main()