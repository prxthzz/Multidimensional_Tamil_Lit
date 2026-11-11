from processing.relationship.analyzer import RelationshipAnalyzer


def test_relationship_without_evidence():
    analyzer = RelationshipAnalyzer()

    result = analyzer.analyze(
        scientific_concepts=["Time Dilation"],
        retrieved_results=[],
    )

    assert result["relationship_type"] == "UNSUPPORTED"
    assert result["relationship_confidence"] == 0.0


def test_synthetic_evidence_cannot_be_fact():
    analyzer = RelationshipAnalyzer()

    results = [
        {
            "source_id": "synthetic-001",
            "source_type": "synthetic_test",
            "text": "Synthetic Tamil retrieval record.",
            "retrieval_score": 0.42,
        }
    ]

    result = analyzer.analyze(
        scientific_concepts=["Time Dilation"],
        retrieved_results=results,
    )

    assert result["relationship_type"] == "INTERPRETATION"
    assert result["relationship_type"] != "FACT"
    assert 0.0 <= result["relationship_confidence"] <= 1.0
    assert len(result["evidence"]) == 1


def test_relationship_confidence_is_separate_from_retrieval_score():
    analyzer = RelationshipAnalyzer()

    results = [
        {
            "source_id": "synthetic-001",
            "source_type": "synthetic_test",
            "text": "Synthetic retrieval record.",
            "retrieval_score": 0.95,
        }
    ]

    result = analyzer.analyze(
        scientific_concepts=["Time Dilation"],
        retrieved_results=results,
    )

    assert result["evidence"][0]["retrieval_score"] == 0.95
    assert result["relationship_confidence"] == 0.5