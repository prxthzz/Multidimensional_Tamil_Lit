from shared.schemas.tamil_retrieval import TamilRetrievalRequest
from src.tamil_rag.retrieval.semantic_retriever import SemanticTamilRetriever
from src.tamil_rag.reranking.reranker import TamilReranker


QUERIES = [
    "அறிவு",
    "அன்பு",
    "முயற்சி",
]


def main():
    retriever = SemanticTamilRetriever(top_k=10)
    reranker = TamilReranker(top_k=5)

    for query in QUERIES:
        request = TamilRetrievalRequest(
            query_terms=[query],
            retrieval_reason="Re-ranking evaluation",
        )

        candidates = retriever.retrieve(request)
        reranked = reranker.rerank(query, candidates)

        print("\n" + "=" * 60)
        print("QUERY:", query)
        print("=" * 60)

        print("\nFinal ranked results:")

        for rank, result in enumerate(reranked, start=1):
            print(
                f"{rank}. {result.source_id} "
                f"| score={result.retrieval_score:.4f}"
            )
            print("   ", result.text)


if __name__ == "__main__":
    main()