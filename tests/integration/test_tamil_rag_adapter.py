from scientific.query.tamil_retrieval_adapter import (
    TamilRAGAdapter,
)
from shared.schemas.tamil_retrieval import TamilRetrievalResult


class FakeTamilRAG:
    def retrieve(self, request):
        assert "Time Dilation" in request.scientific_concepts
        assert "Physics" in request.scientific_domains

        return [
            TamilRetrievalResult(
                source_id="test_tamil_001",
                source_type="tamil_text",
                text="Synthetic Tamil retrieval evidence.",
                matched_terms=["time"],
                retrieval_score=0.75,
                metadata={
                    "synthetic": True,
                },
            )
        ]


def test_tamil_rag_adapter():
    adapter = TamilRAGAdapter(FakeTamilRAG())

    results = adapter.retrieve(
        scientific_concepts=["Time Dilation"],
        scientific_domains=["Physics"],
        context_terms=["relativity"],
        query_terms=["time"],
    )

    assert len(results) == 1

    evidence = results[0]

    assert evidence.source_id == "test_tamil_001"
    assert evidence.source_type == "tamil_rag"
    assert evidence.retrieval_score == 0.75
    assert evidence.matched_terms == ["time"]
    assert evidence.provenance["synthetic"] is True