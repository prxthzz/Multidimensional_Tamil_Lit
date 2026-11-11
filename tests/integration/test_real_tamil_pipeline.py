from integration.application import ScientificApplication


def test_real_tamil_rag_pipeline():
    application = ScientificApplication()

    result = application.analyze(
        "What is time dilation in Tamil literature?"
    )

    assert "Time Dilation" in result.scientific_concepts

    assert result.tamil_evidence

    assert all(
        item["source_type"] == "tamil_rag"
        for item in result.tamil_evidence
    )

    assert len(result.dimensional_analysis) == 4

    assert result.relationship_type in {
        "UNSUPPORTED",
        "INTERPRETATION",
        "ANALOGY",
        "HYPOTHESIS",
        "FACT",
    }