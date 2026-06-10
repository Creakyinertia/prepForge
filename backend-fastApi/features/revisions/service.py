from datetime import datetime
from datetime import timezone

from sqlalchemy.orm import Session

from models.revision import Revision

from core.revision_scheduler import (
    calculate_next_due_date,
)

class RevisionService:
    def create_revision(
        self,
        db: Session,
        user_id,
        topic_id,
    ):
        existing = (
            db.query(Revision)
            .filter(
                Revision.user_id == user_id,
                Revision.topic_id == topic_id,
            )
            .first()
        )
        if existing:
            return existing
        revision = Revision(
            user_id=user_id,
            topic_id=topic_id,
            due_at=calculate_next_due_date(
                0,
                datetime.now(timezone.utc),
            ),
            revision_count=0,
        )
        db.add(revision)

        db.commit()

        db.refresh(revision)

        return revision

    def get_due_revisions(
        self,
        db: Session,
        user_id,
    ):
        return (
            db.query(Revision)
            .filter(
                Revision.user_id == user_id,
                Revision.due_at
                <= datetime.now(timezone.utc),
            )
            .order_by(
                Revision.due_at.asc()
            )
            .all()
        )

    def complete_revision(
        self,
        db: Session,
        revision_id,
    ):
        revision = db.get(
            Revision,
            revision_id,
        )
        if not revision:
            raise ValueError(
                "Revision not found"
            )
            revision.revision_count += 1
            revision.due_at = (
            calculate_next_due_date(
                revision.revision_count,
                datetime.now(timezone.utc),
            )
        )
        db.commit()
        
        db.refresh(revision)
        
        return revision