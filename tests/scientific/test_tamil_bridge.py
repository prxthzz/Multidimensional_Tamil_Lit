from scientific.query.processor import ScientificQueryProcessor
from scientific.wormhole.router import WormholeRouter
from scientific.wormhole.tamil_bridge import ScientificToTamilBridge


KNOWLEDGE_BASE = "data/scientific/scientific_knowledge.json"


def test_scientific_to_tamil_bridge():
    processor = ScientificQueryProcessor(KNOWLEDGE_BASE)

    query = processor.process(
        "What is time dilation?"
    )

    wormhole_result = WormholeRouter().route(query)

    request = ScientificToTamilBridge().build_request(
        query.__dict__,
        wormhole_result,
    )

    assert request.scientific_concepts == [
        "Time Dilation",
        "Special Relativity",
        "General Relativity",
    ]

    assert request.scientific_domains == [
        "Physics",
        "Relativity",
    ]

    assert "time dilation" in request.context_terms
    assert "clock" in request.context_terms

    assert "Time Dilation" in request.query_terms
    assert "Special Relativity" in request.query_terms

    assert request.retrieval_reason != ""


def test_bridge_does_not_create_literary_claims():
    processor = ScientificQueryProcessor(KNOWLEDGE_BASE)

    query = processor.process(
        "What is time dilation?"
    )

    wormhole_result = WormholeRouter().route(query)

    request = ScientificToTamilBridge().build_request(
        query.__dict__,
        wormhole_result,
    )

    assert not hasattr(request, "literary_evidence")
    assert not hasattr(request, "relationship_confidence")