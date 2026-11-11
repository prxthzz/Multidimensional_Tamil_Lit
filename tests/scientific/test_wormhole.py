from scientific.query.processor import ScientificQueryProcessor
from scientific.wormhole.router import WormholeRouter


KNOWLEDGE_BASE = "data/scientific/scientific_knowledge.json"


def test_wormhole_routes_time_dilation():
    processor = ScientificQueryProcessor(KNOWLEDGE_BASE)

    query = processor.process(
        "What is time dilation?"
    )

    result = WormholeRouter().route(query)

    assert result["concept_mapping"]["primary_concepts"] == [
        "Time Dilation"
    ]

    assert "Special Relativity" in (
        result["concept_mapping"]["expanded_concepts"]
    )

    assert "General Relativity" in (
        result["concept_mapping"]["expanded_concepts"]
    )

    assert result["model_route"]["status"] == "resolved"

    assert result["model_route"]["model_type"] == "tiny_llm"


def test_wormhole_handles_unknown_query():
    processor = ScientificQueryProcessor(KNOWLEDGE_BASE)

    query = processor.process(
        "Tell me something completely unrelated."
    )

    result = WormholeRouter().route(query)

    assert result["concept_mapping"]["primary_concepts"] == []

    assert result["model_route"]["status"] == "unresolved"