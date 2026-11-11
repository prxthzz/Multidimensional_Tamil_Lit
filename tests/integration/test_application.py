from integration.application import ScientificApplication


def test_raw_query_reaches_analysis_pipeline():
    application = ScientificApplication()

    result = application.analyze(
        "What is time dilation?"
    )

    assert "Time Dilation" in result.scientific_concepts

    assert "Physics" in result.scientific_domains

    assert len(result.dimensional_analysis) == 4

    assert result.relationship_type == "UNSUPPORTED"

    assert result.relationship_confidence == 0.0

    assert result.uncertainty is True