from processing.dimensions.one_d.processor import OneDProcessor
from processing.dimensions.two_d.processor import TwoDProcessor
from processing.dimensions.three_d.processor import ThreeDProcessor
from processing.dimensions.four_d.processor import FourDProcessor


TAMIL_EVIDENCE = [
    {
        "source_id": "test_kural_1",
        "source_type": "synthetic_test",
        "text": "Synthetic literary evidence for integration testing.",
        "retrieval_score": 0.8,
        "metadata": {
            "purpose": "integration_test",
        },
    }
]


CONTEXT = {
    "query": "What is time dilation?",
    "scientific_concepts": [
        "Time Dilation",
    ],
    "scientific_domains": [
        "Physics",
        "Relativity",
    ],
    "context_terms": [
        "time",
        "clock",
    ],
    "tamil_evidence": TAMIL_EVIDENCE,
}


def test_all_dimension_processors():

    processors = [
        OneDProcessor(),
        TwoDProcessor(),
        ThreeDProcessor(),
        FourDProcessor(),
    ]

    results = [
        processor.process(CONTEXT)
        for processor in processors
    ]

    assert [result["dimension"] for result in results] == [
        "1D",
        "2D",
        "3D",
        "4D",
    ]

    assert results[0]["analysis_type"] == "TEXT_LITERAL"
    assert results[1]["analysis_type"] == "INTERPRETATION_CONTEXT"
    assert results[2]["analysis_type"] == "SYMBOL_CONCEPT"
    assert results[3]["analysis_type"] == "FUTURE_HYPOTHETICAL"

    assert results[0]["status"] == "resolved"
    assert results[1]["status"] == "resolved"
    assert results[2]["status"] == (
        "eligible_for_relationship_analysis"
    )
    assert results[3]["status"] == "not_activated"

    assert results[3]["properties"]["hypothesis_generated"] is False