from processing.dimensions.pipeline import DimensionPipeline


def test_dimension_pipeline_runs_all_levels():
    pipeline = DimensionPipeline()

    context = {
        "query": "What is time dilation?",
        "scientific_concepts": [
            "Time Dilation",
        ],
        "tamil_evidence": [
            {
                "source_id": "test_tamil",
                "text": "Synthetic Tamil evidence",
                "retrieval_score": 0.8,
            }
        ],
    }

    result = pipeline.process(context)

    assert result["analysis_model"] == "interpretive_levels"

    assert set(result["dimensions"].keys()) == {
        "1D",
        "2D",
        "3D",
        "4D",
    }


def test_dimension_pipeline_does_not_create_relationship():
    pipeline = DimensionPipeline()

    context = {
        "query": "What is time dilation?",
        "scientific_concepts": [
            "Time Dilation",
        ],
        "tamil_evidence": [],
    }

    result = pipeline.process(context)

    assert (
        result["dimensions"]["3D"]["properties"][
            "relationship_determined"
        ]
        is False
    )

    assert (
        result["dimensions"]["4D"]["properties"][
            "hypothesis_generated"
        ]
        is False
    )