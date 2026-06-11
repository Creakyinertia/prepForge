from uuid import UUID

from sqlalchemy.orm import Session

from models.resource import Resource
from models.topic import Topic


class ResourceService:

    def create_resource(
        self,
        db: Session,
        topic_id: UUID,
        title: str,
        url: str,
        resource_type,
    ):
        topic = db.get(
            Topic,
            topic_id,
        )

        if not topic:
            raise ValueError(
                "Topic not found",
            )

        resource = Resource(
            topic_id=topic_id,
            title=title,
            url=url,
            resource_type=resource_type,
        )

        db.add(resource)

        db.commit()

        db.refresh(resource)

        return resource

    def get_topic_resources(
        self,
        db: Session,
        topic_id: UUID,
    ):
        return (
            db.query(Resource)
            .filter(
                Resource.topic_id == topic_id,
            )
            .order_by(
                Resource.created_at.desc(),
            )
            .all()
        )