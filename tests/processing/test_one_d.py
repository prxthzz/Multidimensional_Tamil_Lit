from processing.dimensions.one_d.processor import OneDProcessor


def test_one_d_processing():

    context = {
        "query": "What is time dilation?",
        "scientific_concepts": [
            "Time Dilation",
        ],
        "tamil_evidence": [
            {
                "source_id": "test_1",
                "source_type": "synthetic_test",
                "text": "Synthetic textual evidence.",
                "retrieval_score": 0.7,
                "metadata": {},
            }
        ],
    }

    result = OneDProcessor().process(context)

    assert result["dimension"] == "1D"
    assert result["analysis_type"] == "TEXT_LITERAL"
    assert result["status"] == "resolved"
    assert result["properties"]["evidence_count"] == 1
    assert result["properties"]["contains_interpretation"] is False
    assert result["properties"]["contains_relationship_claim"] is False