from scientific.query.processor import ScientificQueryProcessor
from scientific.wormhole.router import WormholeRouter
from scientific.wormhole.tamil_bridge import ScientificToTamilBridge

from processing.dimensions.one_d.processor import OneDProcessor
from processing.dimensions.two_d.processor import TwoDProcessor
from processing.dimensions.three_d.processor import ThreeDProcessor
from processing.dimensions.four_d.processor import FourDProcessor

from tamil_rag_mock.mock_retrieval import MockTamilRetrieval


KNOWLEDGE_BASE = "data/scientific/scientific_knowledge.json"


def test_full_scientific_pipeline():

    # 1. Scientific query processing
    query = ScientificQueryProcessor(
        KNOWLEDGE_BASE
    ).process(
        "What is time dilation?"
    )

    assert "Time Dilation" in query.concepts

    # 2. Wormhole routing
    wormhole = WormholeRouter().route(
        query
    )

    assert (
        wormhole["input_query"]["original_query"]
        == query.original_query
    )

    assert wormhole["concept_mapping"]["primary_concepts"]

    assert (
        "Time Dilation"
        in wormhole["concept_mapping"]["primary_concepts"]
    )

    assert wormhole["context_mapping"]["domains"]

    assert (
        wormhole["model_route"]["status"]
        == "resolved"
    )

    # 3. Scientific -> Tamil retrieval bridge
    retrieval_request = ScientificToTamilBridge().build_request(
        query.__dict__,
        wormhole
    )

    assert "Time Dilation" in (
        retrieval_request.scientific_concepts
    )

    # 4. Mock Tamil RAG
    # Used on the scientific branch only to validate
    # the retrieval integration contract.
    rag = MockTamilRetrieval()

    tamil_results = rag.retrieve(
        retrieval_request
    )

    assert isinstance(
        tamil_results,
        list,
    )

    # 5. Convert retrieved evidence into
    # the dimensional analysis context.
    tamil_evidence = [
        {
            "source_id": result.source_id,
            "source_type": result.source_type,
            "text": result.text,
            "retrieval_score": result.retrieval_score,
            "metadata": result.metadata,
        }
        for result in tamil_results
    ]

    analysis_context = {
        "query": query.original_query,
        "scientific_concepts": query.concepts,
        "scientific_domains": query.domains,
        "context_terms": query.context_terms,
        "tamil_evidence": tamil_evidence,
    }

    # 6. 1D -> 4D analysis
    one_d = OneDProcessor().process(
        analysis_context
    )

    two_d = TwoDProcessor().process(
        analysis_context
    )

    three_d = ThreeDProcessor().process(
        analysis_context
    )

    four_d = FourDProcessor().process(
        analysis_context
    )

    # 7. Validate dimensional analysis
    assert one_d["dimension"] == "1D"
    assert one_d["analysis_type"] == "TEXT_LITERAL"

    assert two_d["dimension"] == "2D"
    assert two_d["analysis_type"] == "INTERPRETATION_CONTEXT"

    assert three_d["dimension"] == "3D"
    assert three_d["analysis_type"] == "SYMBOL_CONCEPT"

    assert four_d["dimension"] == "4D"
    assert four_d["analysis_type"] == "FUTURE_HYPOTHETICAL"

    # 8. 3D does not automatically claim
    # a scientific-literary relationship.
    assert three_d["relationship_claim"] is None

    # 9. 4D does not automatically generate
    # a hypothesis.
    assert (
        four_d["properties"]["hypothesis_generated"]
        is False
    )