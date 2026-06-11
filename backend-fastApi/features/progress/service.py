from uuid import UUID
from sqlalchemy.orm import Session
from core.exceptions import NotFoundError
from features.revisions.service import RevisionService
from models.enums import (
    TopicProgressStatus,
)
from models.topic import Topic
from models.topic_progress import (
    TopicProgress,
)


class ProgressService:

    def __init__(self):
        self.revision_service = RevisionService()

    def update_progress(
        self,
        db: Session,
        user_id: UUID,
        topic_id: UUID,
        status: TopicProgressStatus,
    ):
        topic = db.get(
            Topic,
            topic_id,
        )

        if not topic:
            raise NotFoundError(
                "Topic not found"
            )

        progress = (
            db.query(TopicProgress)
            .filter(
                TopicProgress.user_id == user_id,
                TopicProgress.topic_id == topic_id,
            )
            .first()
        )

        previous_status = None

        if not progress:
            progress = TopicProgress(
                user_id=user_id,
                topic_id=topic_id,
                status=status,
            )

            db.add(progress)

        else:
            previous_status = progress.status
            progress.status = status

        if (
            status == TopicProgressStatus.COMPLETED
            and previous_status
            != TopicProgressStatus.COMPLETED
        ):
            self.revision_service.schedule_first_revision(
                db,
                user_id,
                topic_id,
            )
        db.commit()
        db.refresh(progress)

        return progress
