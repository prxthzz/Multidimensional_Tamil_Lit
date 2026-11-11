from shared.schemas.evidence import Evidence


def test_evidence_schema():
    evidence = Evidence(
        source_id="physics_spacetime",
        source_type="scientific_kb",
        text="Spacetime combines space and time into a unified framework.",
        retrieval_score=0.92,
        matched_terms=["spacetime"],
        provenance={
            "source": "scientific_knowledge.json",
        },
    )

    assert evidence.source_id == "physics_spacetime"
    assert evidence.source_type == "scientific_kb"
    assert evidence.retrieval_score == 0.92
    assert evidence.matched_terms == ["spacetime"]
    assert evidence.provenance["source"] == "scientific_knowledge.json"


def test_evidence_defaults():
    evidence = Evidence(
        source_id="test",
        source_type="test",
        text="test evidence",
    )

    assert evidence.retrieval_score == 0.0
    assert evidence.matched_terms == []
    assert evidence.provenance == {}
    assert evidence.metadata == {}