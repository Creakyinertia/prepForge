from datetime import datetime
from datetime import timezone
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from models.bookmarked_topic import (
    BookmarkedTopic,
)
from models.enums import (
    TopicProgressStatus,
)
from models.revision import Revision
from models.topic import Topic
from models.topic_progress import (
    TopicProgress,
)
from models.bookmarked_topic import (
    BookmarkedTopic,
)


class HomeService:

    def get_home_data(
        self,
        db: Session,
        user_id: UUID,
    ):
        continue_learning = (
            db.query(
                TopicProgress,
                Topic,
            )
            .join(
                Topic,
                Topic.id
                == TopicProgress.topic_id,
            )
            .filter(
                TopicProgress.user_id
                == user_id,
                TopicProgress.status
                == TopicProgressStatus.IN_PROGRESS,
            )
            .order_by(
                TopicProgress.updated_at.desc(),
            )
            .limit(5)
            .all()
        )

        continue_learning_topics = [
            {
                "topic_id": topic.id,
                "title": topic.title,
                "slug": topic.slug,
                "progress_status": progress.status,
            }
            for progress, topic in continue_learning
        ]

        due_revisions = (
            db.query(func.count())
            .select_from(Revision)
            .filter(
                Revision.user_id == user_id,
                Revision.due_at
                <= datetime.now(
                    timezone.utc,
                ),
            )
            .scalar()
        )

        recent_bookmarks = (
            db.query(BookmarkedTopic)
            .filter(
                BookmarkedTopic.user_id
                == user_id,
            )
            .order_by(
                BookmarkedTopic.created_at.desc(),
            )
            .limit(5)
            .all()
        )
        recent_bookmark_items = [
            {
                "id": bookmark.id,
                "topic_id": bookmark.topic_id,
                "topic_title": bookmark.topic.title,
                "topic_slug": bookmark.topic.slug,
                "topic_description": bookmark.topic.description,
            }
            for bookmark in recent_bookmarks
        ]
        return {
            "continue_learning": continue_learning_topics,
            "due_revisions": due_revisions,
            "recent_bookmarks": recent_bookmark_items,
        }