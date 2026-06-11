from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.orm import Session
from core.exceptions import NotFoundError
from core.revision_scheduler import (
    calculate_next_revision_date,
)
from models.revision import Revision

class RevisionService:
    def schedule_first_revision(
        self,
        db: Session,
        user_id: UUID,
        topic_id: UUID,
    ):
        existing_revision = (
            db.query(Revision)
            .filter(
                Revision.user_id == user_id,
                Revision.topic_id == topic_id,
            )
            .first()
        )

        if existing_revision:
            return existing_revision

        now = datetime.now(
            timezone.utc,
        )

        revision = Revision(
            user_id=user_id,
            topic_id=topic_id,
            due_at=calculate_next_revision_date(
                0,
                now,
            ),
            revision_count=0,
        )
        db.add(revision)

        return revision

    def get_due_revisions(
        self,
        db: Session,
        user_id: UUID,
    ):
        now = datetime.now(
            timezone.utc,
        )
        return (
            db.query(Revision)
            .filter(
                Revision.user_id == user_id,
                Revision.due_at <= now,
            )
            .order_by(
                Revision.due_at.asc(),
            )
            .all()
        )

    def complete_revision(
        self,
        db: Session,
        revision_id: UUID,
        user_id: UUID,
    ):
        revision = (
            db.query(Revision)
            .filter(
                Revision.id == revision_id,
                Revision.user_id == user_id,
            )
            .first()
        )

        if not revision:
            raise NotFoundError(
                "Revision not found",
            )

        revision.revision_count += 1

        revision.due_at = calculate_next_revision_date(
            revision.revision_count,
            datetime.now(timezone.utc),
        )
        db.commit()
        db.refresh(revision)

        return revision
