from processing.relationship.analyzer import RelationshipAnalyzer


def test_no_evidence_is_unsupported():
    analyzer = RelationshipAnalyzer()

    result = analyzer.analyze(
        scientific_concepts=["Time Dilation"],
        retrieved_results=[],
    )

    assert result["relationship_type"] == "UNSUPPORTED"
    assert result["relationship_confidence"] == 0.0


def test_existing_literary_evidence_returns_interpretation():
    analyzer = RelationshipAnalyzer()

    results = [
        {
            "source_id": "tamil_001",
            "source_type": "tamil_rag",
            "text": "Tamil literary evidence.",
            "retrieval_score": 0.82,
        }
    ]

    result = analyzer.analyze(
        scientific_concepts=["Time Dilation"],
        retrieved_results=results,
    )

    assert result["relationship_type"] == "INTERPRETATION"
    assert result["relationship_confidence"] == 0.5


def test_retrieval_score_is_not_relationship_confidence():
    analyzer = RelationshipAnalyzer()

    results = [
        {
            "source_id": "tamil_001",
            "source_type": "tamil_rag",
            "text": "Highly retrieved evidence.",
            "retrieval_score": 0.99,
        }
    ]

    result = analyzer.analyze(
        scientific_concepts=["Time Dilation"],
        retrieved_results=results,
    )

    assert result["evidence"][0]["retrieval_score"] == 0.99
    assert result["relationship_confidence"] == 0.5


def test_synthetic_test_evidence_does_not_become_fact():
    analyzer = RelationshipAnalyzer()

    results = [
        {
            "source_id": "synthetic_001",
            "source_type": "synthetic_test",
            "text": "Synthetic test evidence.",
            "retrieval_score": 1.0,
        }
    ]

    result = analyzer.analyze(
        scientific_concepts=["Time Dilation"],
        retrieved_results=results,
    )

    assert result["relationship_type"] == "INTERPRETATION"

def test_no_tamil_evidence_is_unsupported():
    analyzer = RelationshipAnalyzer()

    results = [
        {
            "source_id": "physics_001",
            "source_type": "scientific_kb",
            "text": "Scientific evidence.",
            "retrieval_score": 0.95,
        }
    ]

    result = analyzer.analyze(
        scientific_concepts=["Time Dilation"],
        retrieved_results=results,
    )

    assert result["relationship_type"] == "UNSUPPORTED"
    assert result["relationship_confidence"] == 0.0


def test_explicit_analogy_metadata_is_respected():
    analyzer = RelationshipAnalyzer()

    results = [
        {
            "source_id": "tamil_001",
            "source_type": "tamil_rag",
            "text": "Tamil literary evidence.",
            "retrieval_score": 0.82,
            "metadata": {
                "relationship_type": "ANALOGY",
            },
        }
    ]

    result = analyzer.analyze(
        scientific_concepts=["Time Dilation"],
        retrieved_results=results,
    )

    assert result["relationship_type"] == "ANALOGY"


def test_explicit_hypothesis_metadata_is_respected():
    analyzer = RelationshipAnalyzer()

    results = [
        {
            "source_id": "tamil_001",
            "source_type": "tamil_rag",
            "text": "Tamil literary evidence.",
            "retrieval_score": 0.82,
            "metadata": {
                "relationship_type": "HYPOTHESIS",
            },
        }
    ]

    result = analyzer.analyze(
        scientific_concepts=["Time Dilation"],
        retrieved_results=results,
    )

    assert result["relationship_type"] == "HYPOTHESIS"


def test_retrieval_similarity_cannot_create_fact():
    analyzer = RelationshipAnalyzer()

    results = [
        {
            "source_id": "tamil_001",
            "source_type": "tamil_rag",
            "text": "Highly similar literary text.",
            "retrieval_score": 0.999,
        }
    ]

    result = analyzer.analyze(
        scientific_concepts=["Time Dilation"],
        retrieved_results=results,
    )

    assert result["relationship_type"] == "INTERPRETATION"
    assert result["relationship_confidence"] == 0.5