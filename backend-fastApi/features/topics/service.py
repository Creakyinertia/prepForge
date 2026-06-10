from sqlalchemy.orm import Session
from uuid import UUID
from models.topic import Topic
from core.utils import generate_slug


class TopicService:
    def create_topic(
        self,
        db: Session,
        title: str,
        description: str | None,
    ):
        slug = generate_slug(title)

        existing = (
            db.query(Topic)
            .filter(Topic.slug == slug)
            .first()
        )

        if existing:
            raise ValueError(
                "Topic already exists"
            )

        topic = Topic(
            title=title,
            slug=slug,
            description=description,
        )

        db.add(topic)

        db.commit()

        db.refresh(topic)

        return topic

    def get_topics(
        self,
        db: Session,
        limit: int = 20,
        offset: int = 0,
    ):
        return (
            db.query(Topic)
            .order_by(
                Topic.created_at.desc()
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_topic_by_id(
        self,
        db: Session,
        topic_id: UUID,
    ):
        return db.get(
            Topic,
            topic_id,
        )