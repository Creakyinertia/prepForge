from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from models.enums import (
    TopicProgressStatus,
)

from models.note import Note
from models.revision import Revision
from models.topic_progress import TopicProgress

class DashboardService:

    def get_dashboard(
        self,
        db: Session,
        user_id,
    ):
        completed_topics = (
            db.query(func.count())
            .select_from(TopicProgress)
            .filter(
                TopicProgress.user_id == user_id,
                TopicProgress.status == TopicProgressStatus.COMPLETED,
            )
            .scalar()
        )

        in_progress_topics = (
            db.query(func.count())
            .select_from(TopicProgress)
            .filter(
                TopicProgress.user_id == user_id,
                TopicProgress.status == TopicProgressStatus.IN_PROGRESS,
            )
            .scalar()
        )

        notes_count = (
            db.query(func.count())
            .select_from(Note)
            .filter(
                Note.user_id == user_id,
            )
            .scalar()
        )

        due_revisions = (
            db.query(func.count())
            .select_from(Revision)
            .filter(
                Revision.user_id == user_id,
                Revision.due_at <= datetime.now(
                    timezone.utc
                ),
            )
            .scalar()
        )

        roadmaps_started = (
            db.query(func.count())
            .select_from(
                TopicProgress
            )
            .filter(
                TopicProgress.user_id == user_id,
                TopicProgress.status.in_(
                    [
                        TopicProgressStatus.IN_PROGRESS,
                        TopicProgressStatus.COMPLETED,
                    ]
                ),
            )
            .scalar()
        )

        return {
            "total_topics_completed": completed_topics,
            "total_topics_in_progress": in_progress_topics,
            "total_notes": notes_count,
            "due_revisions": due_revisions,
            "roadmaps_started": roadmaps_started,
        }