from scientific.query.processor import ScientificQueryProcessor
from scientific.wormhole.router import WormholeRouter
from scientific.wormhole.tamil_bridge import ScientificToTamilBridge
from tamil_rag_mock.mock_retrieval import MockTamilRetrieval

KNOWLEDGE_BASE = "data/scientific/scientific_knowledge.json"


def test_scientific_to_mock_tamil_rag_pipeline():
    processor = ScientificQueryProcessor(KNOWLEDGE_BASE)

    query = processor.process(
        "What is time dilation?"
    )

    wormhole_result = WormholeRouter().route(query)

    retrieval_request = ScientificToTamilBridge().build_request(
        query.__dict__,
        wormhole_result,
    )

    results = MockTamilRetrieval().retrieve(
        retrieval_request
    )

    assert retrieval_request.scientific_concepts == [
        "Time Dilation",
        "Special Relativity",
        "General Relativity",
    ]

    assert retrieval_request.scientific_domains == [
        "Physics",
        "Relativity",
    ]

    assert len(results) == 2

    for result in results:
        assert result.source_type == "synthetic_test"
        assert result.metadata["purpose"] == "integration_test"
        assert 0.0 <= result.retrieval_score <= 1.0