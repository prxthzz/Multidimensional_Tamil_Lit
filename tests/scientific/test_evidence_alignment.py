from scientific.query.evidence_alignment import EvidenceAligner
from shared.schemas.evidence import Evidence


def test_evidence_alignment_groups_sources():
    evidence = [
        Evidence(
            source_id="physics_001",
            source_type="scientific_kb",
            text="Scientific evidence",
            retrieval_score=0.9,
        ),
        Evidence(
            source_id="tamil_001",
            source_type="tamil_rag",
            text="Tamil evidence",
            retrieval_score=0.7,
        ),
        Evidence(
            source_id="research_001",
            source_type="research",
            text="Research evidence",
            retrieval_score=0.8,
        ),
    ]

    aligner = EvidenceAligner()

    result = aligner.align(evidence)

    assert len(result.scientific_evidence) == 1
    assert len(result.tamil_evidence) == 1
    assert len(result.research_evidence) == 1

    assert result.evidence_count == 3

    assert set(result.sources_present) == {
        "scientific_kb",
        "tamil_rag",
        "research",
    }


def test_missing_sources_are_recorded():
    evidence = [
        Evidence(
            source_id="physics_001",
            source_type="scientific_kb",
            text="Scientific evidence",
            retrieval_score=0.9,
        )
    ]

    aligner = EvidenceAligner()

    result = aligner.align(
        evidence,
        required_sources=[
            "scientific_kb",
            "tamil_rag",
            "research",
        ],
    )

    assert result.missing_sources == [
        "tamil_rag",
        "research",
    ]


def test_empty_alignment():
    aligner = EvidenceAligner()

    result = aligner.align([])

    assert result.evidence_count == 0
    assert result.sources_present == []
    assert result.missing_sources == []