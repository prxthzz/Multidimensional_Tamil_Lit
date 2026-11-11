import uuid
import datetime
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from src.database.models import EvidenceRecord, ReviewStatusEnum

class EvidenceService:
    @staticmethod
    def create_or_update_evidence_record(
        db: Session,
        scientific_concept_id: str,
        scientific_concept_name: str,
        literary_source_id: str,
        verse_id: str,
        relationship_type: str,
        retrieval_relevance: float,
        evidence_strength: str,
        interpretation_confidence: float,
        supporting_text: str,
        translation: Optional[str] = None,
        commentary: Optional[str] = None,
        scientific_claim: Optional[str] = None,
        literary_claim: Optional[str] = None,
        comparison: Optional[str] = None,
        limitations: Optional[List[str]] = None,
        created_by: str = "SYSTEM"
    ) -> EvidenceRecord:
        evidence_id = f"EV-{scientific_concept_id}-{verse_id}".replace(" ", "_")
        
        existing = db.query(EvidenceRecord).filter(EvidenceRecord.evidence_id == evidence_id).first()
        if existing:
            # AI never overwrites human approved knowledge!
            if existing.review_status == ReviewStatusEnum.APPROVED:
                return existing

            existing.relationship_type = relationship_type
            existing.retrieval_relevance = retrieval_relevance
            existing.evidence_strength = evidence_strength
            existing.interpretation_confidence = interpretation_confidence
            existing.supporting_text = supporting_text
            existing.translation = translation or existing.translation
            existing.commentary = commentary or existing.commentary
            existing.scientific_claim = scientific_claim or existing.scientific_claim
            existing.limitations = limitations or existing.limitations
            existing.updated_at = datetime.datetime.utcnow()
            db.commit()
            db.refresh(existing)
            return existing

        record = EvidenceRecord(
            evidence_id=evidence_id,
            scientific_concept_id=scientific_concept_id,
            scientific_concept_name=scientific_concept_name,
            literary_source_id=literary_source_id,
            verse_id=verse_id,
            relationship_type=relationship_type,
            retrieval_relevance=retrieval_relevance,
            evidence_strength=evidence_strength,
            interpretation_confidence=interpretation_confidence,
            scientific_claim=scientific_claim or f"Scientific analysis of {scientific_concept_name}",
            literary_claim=literary_claim or "Classical Tamil verse expression",
            comparison=comparison or "Evidence-aware semantic alignment",
            supporting_text=supporting_text,
            translation=translation or "",
            commentary=commentary or "",
            limitations=limitations or [],
            review_status=ReviewStatusEnum.DRAFT,
            created_by=created_by
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
