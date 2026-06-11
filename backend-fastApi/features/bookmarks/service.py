from uuid import UUID

from sqlalchemy.orm import Session

from models.bookmarked_topic import (
    BookmarkedTopic,
)
from models.topic import Topic


class BookmarkService:

    def create_bookmark(
        self,
        db: Session,
        user_id: UUID,
        topic_id: UUID,
    ):
        topic = db.get(
            Topic,
            topic_id,
        )

        if not topic:
            raise ValueError(
                "Topic not found",
            )

        bookmark = (
            db.query(BookmarkedTopic)
            .filter(
                BookmarkedTopic.user_id == user_id,
                BookmarkedTopic.topic_id == topic_id,
            )
            .first()
        )

        if bookmark:
            return {
                        "id": bookmark.id,
                        "topic_id": bookmark.topic_id,
                        "topic_title": bookmark.topic.title,
                        "topic_slug": bookmark.topic.slug,
                        "topic_description": bookmark.topic.description,
                    }

        bookmark = BookmarkedTopic(
            user_id=user_id,
            topic_id=topic_id,
        )

        db.add(bookmark)

        db.commit()

        db.refresh(bookmark)

        return {
            "id": bookmark.id,
            "topic_id": bookmark.topic_id,
            "topic_title": bookmark.topic.title,
            "topic_slug": bookmark.topic.slug,
            "topic_description": bookmark.topic.description,
        }

    def remove_bookmark(
        self,
        db: Session,
        user_id: UUID,
        topic_id: UUID,
    ):
        bookmark = (
            db.query(BookmarkedTopic)
            .filter(
                BookmarkedTopic.user_id == user_id,
                BookmarkedTopic.topic_id == topic_id,
            )
            .first()
        )

        if not bookmark:
            raise ValueError(
                "Bookmark not found",
            )

        db.delete(bookmark)

        db.commit()

    def get_bookmarks(
        self,
        db: Session,
        user_id: UUID,
    ):
        bookmarks = (
            db.query(BookmarkedTopic)
            .filter(
                BookmarkedTopic.user_id == user_id,
            )
            .order_by(
                BookmarkedTopic.created_at.desc(),
            )
            .all()
        )

        return [
            {
                "id": bookmark.id,
                "topic_id": bookmark.topic_id,
                "topic_title": bookmark.topic.title,
                "topic_slug": bookmark.topic.slug,
                "topic_description": bookmark.topic.description,
            }
            for bookmark in bookmarks
        ]