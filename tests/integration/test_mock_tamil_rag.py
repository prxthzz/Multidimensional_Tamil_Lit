from tamil_rag_mock.mock_retrieval import MockTamilRetrieval
from shared.schemas.tamil_retrieval import TamilRetrievalRequest


def test_mock_tamil_retrieval_contract():
    request = TamilRetrievalRequest(
        scientific_concepts=[
            "Time Dilation",
            "Special Relativity",
        ],
        scientific_domains=[
            "Physics",
            "Relativity",
        ],
        context_terms=[
            "time",
            "clock",
        ],
        query_terms=[
            "Time Dilation",
            "relativity",
        ],
        retrieval_reason=(
            "Integration test request."
        ),
    )

    results = MockTamilRetrieval().retrieve(request)

    assert len(results) == 2

    for result in results:
        assert result.source_type == "synthetic_test"
        assert result.metadata["purpose"] == "integration_test"
        assert 0.0 <= result.retrieval_score <= 1.0
        assert result.text != ""
        assert result.source_id != ""


def test_mock_tamil_retrieval_empty_request():
    request = TamilRetrievalRequest()

    results = MockTamilRetrieval().retrieve(request)

    assert results == []