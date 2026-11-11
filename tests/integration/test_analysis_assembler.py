from integration.analysis_assembler import AnalysisAssembler


def test_analysis_assembler():

    scientific_query = {
        "concepts": ["Time Dilation"],
    }

    wormhole_result = {
        "concept_mapping": {
            "all_concepts": [
                "Time Dilation",
                "Special Relativity",
            ],
        },
        "context_mapping": {
            "domains": [
                "Physics",
                "Relativity",
            ],
        },
        "dimension_route": {
            "dimensional_analysis": [
                {
                    "dimension": "4D",
                    "representation_type": "spatiotemporal_structure",
                }
            ],
        },
    }

    tamil_results = [
        {
            "source_id": "synthetic-001",
            "source_type": "synthetic_test",
            "text": "Synthetic Tamil retrieval record.",
            "retrieval_score": 0.42,
        }
    ]

    relationship_result = {
        "relationship_type": "INTERPRETATION",
        "relationship_confidence": 0.5,
        "reason": "Conceptual interpretation only.",
    }

    result = AnalysisAssembler().assemble(
        scientific_query,
        wormhole_result,
        tamil_results,
        relationship_result,
    )

    assert result.scientific_concepts == [
        "Time Dilation",
        "Special Relativity",
    ]

    assert result.scientific_domains == [
        "Physics",
        "Relativity",
    ]

    assert result.dimensional_analysis[0]["dimension"] == "4D"

    assert result.tamil_evidence == tamil_results

    assert result.relationship_type == "INTERPRETATION"

    assert result.relationship_confidence == 0.5

    assert result.uncertainty is True