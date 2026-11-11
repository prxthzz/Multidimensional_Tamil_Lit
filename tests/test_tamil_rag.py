from shared.schemas.tamil_retrieval import TamilRetrievalRequest
from tamil_rag.interface.tamil_rag import TamilRAG


def main():
    request = TamilRetrievalRequest(
        scientific_concepts=["அறிவு"],
        scientific_domains=[],
        context_terms=[],
        query_terms=["அறிவு"],
        retrieval_reason="Test Tamil RAG interface",
    )

    rag = TamilRAG(
        retrieval_top_k=10,
        final_top_k=5,
    )

    results = rag.retrieve(request)

    print("Result count:", len(results))

    for index, result in enumerate(results, start=1):
        print()
        print(f"Result {index}")
        print("Source ID:", result.source_id)
        print("Source Type:", result.source_type)
        print("Text:", result.text)
        print("Score:", result.retrieval_score)
        print("Metadata:", result.metadata)


if __name__ == "__main__":
    main()