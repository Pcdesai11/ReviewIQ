import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.session import AuditLog


def write_audit(
    db: Session,
    *,
    analysis_type: str,
    subject_id: str,
    model_provider: str,
    model_name: str,
    prompt: str,
    output: str,
    action_taken: str,
) -> AuditLog:
    row = AuditLog(
        id=str(uuid.uuid4()),
        analysis_type=analysis_type,
        subject_id=subject_id,
        model_provider=model_provider,
        model_name=model_name,
        prompt=prompt,
        output=output,
        action_taken=action_taken,
        created_at=datetime.now(timezone.utc),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
