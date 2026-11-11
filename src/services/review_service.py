import datetime
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from src.database.models import EvidenceRecord, ExpertReview, ReviewStatusEnum, User

class ReviewService:
    @staticmethod
    def submit_expert_review(
        db: Session,
        evidence_id: str,
        reviewer_user: User,
        status_decision: str,
        relationship_override: Optional[str] = None,
        evidence_strength_override: Optional[str] = None,
        comments: Optional[str] = None
    ) -> ExpertReview:
        record = db.query(EvidenceRecord).filter(EvidenceRecord.evidence_id == evidence_id).first()
        if not record:
            raise ValueError(f"Evidence record '{evidence_id}' not found.")

        review = ExpertReview(
            evidence_id=evidence_id,
            reviewer_id=reviewer_user.id,
            reviewer_name=reviewer_user.full_name,
            reviewer_role=reviewer_user.role,
            status_decision=status_decision,
            relationship_override=relationship_override,
            evidence_strength_override=evidence_strength_override,
            comments=comments or ""
        )
        db.add(review)

        # Update Evidence Record status
        if status_decision in [ReviewStatusEnum.APPROVED, ReviewStatusEnum.REJECTED, ReviewStatusEnum.NEEDS_REVISION]:
            record.review_status = status_decision

        if relationship_override:
            record.relationship_type = relationship_override
        if evidence_strength_override:
            record.evidence_strength = evidence_strength_override

        reviewer_list = record.reviewer_ids or []
        if reviewer_user.id not in reviewer_list:
            reviewer_list.append(reviewer_user.id)
            record.reviewer_ids = reviewer_list

        record.updated_at = datetime.datetime.utcnow()
        db.commit()
        db.refresh(review)
        return review
