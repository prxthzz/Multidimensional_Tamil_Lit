import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from src.database.models import AuditLog

class AuditService:
    @staticmethod
    def log_action(
        db: Session,
        action: str,
        resource: str,
        user_id: Optional[str] = None,
        username: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        request_id: Optional[str] = None,
        status: str = "SUCCESS"
    ) -> AuditLog:
        audit_record = AuditLog(
            user_id=user_id or "ANONYMOUS",
            username=username or "ANONYMOUS",
            action=action,
            resource=resource,
            details=details or {},
            ip_address=ip_address or "127.0.0.1",
            request_id=request_id or "REQ-SYSTEM",
            status=status,
            timestamp=datetime.datetime.utcnow()
        )
        db.add(audit_record)
        try:
            db.commit()
            db.refresh(audit_record)
        except Exception:
            db.rollback()
        return audit_record
