from src.database.connection import SessionLocal, init_db
from src.database.models import User, RoleEnum, EvidenceRecord, AuditLog, ScientificConcept

def test_database_creation_and_seeding():
    init_db()
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        concept_count = db.query(ScientificConcept).count()
        assert user_count > 0
        assert concept_count >= 50
    finally:
        db.close()

def test_evidence_record_persistence():
    db = SessionLocal()
    try:
        ev = EvidenceRecord(
            evidence_id="TEST-EV-001",
            scientific_concept_id="water_cycle",
            scientific_concept_name="Water Cycle",
            literary_source_id="thirukkural_11",
            verse_id="thirukkural_11",
            relationship_type="THEMATIC",
            retrieval_relevance=0.88,
            evidence_strength="MEDIUM",
            interpretation_confidence=0.75,
            supporting_text="துப்பார்க்குத் துப்பாய..."
        )
        db.add(ev)
        db.commit()

        fetched = db.query(EvidenceRecord).filter(EvidenceRecord.evidence_id == "TEST-EV-001").first()
        assert fetched is not None
        assert fetched.relationship_type == "THEMATIC"
        assert fetched.evidence_strength == "MEDIUM"

        db.delete(fetched)
        db.commit()
    finally:
        db.close()
