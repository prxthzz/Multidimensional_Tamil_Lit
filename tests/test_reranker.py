from shared.schemas.tamil_retrieval import TamilRetrievalRequest
from src.tamil_rag.retrieval.semantic_retriever import SemanticTamilRetriever
from src.tamil_rag.reranking.reranker import TamilReranker


def main():
    retriever = SemanticTamilRetriever(top_k=10)
    reranker = TamilReranker(top_k=5)

    request = TamilRetrievalRequest(
        query_terms=["முயற்சி"],
        retrieval_reason="Re-ranking prototype test",
    )

    results = retriever.retrieve(request)

    print("\nBefore re-ranking:")
    for rank, result in enumerate(results, start=1):
        print(
            f"{rank}. {result.source_id} "
            f"| {result.retrieval_score:.4f}"
        )

    query = "முயற்சி"

    reranked_results = reranker.rerank(
        query,
        results,
    )

    print("\nAfter re-ranking:")

    for rank, result in enumerate(
        reranked_results,
        start=1,
    ):
        print(
            f"{rank}. {result.source_id} "
            f"| {result.retrieval_score:.4f}"
        )
        print("   ", result.text)


if __name__ == "__main__":
    main()