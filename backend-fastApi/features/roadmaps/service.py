from uuid import UUID
from sqlalchemy.orm import Session
from models.roadmap_topic import RoadmapTopic
from models.roadmap import Roadmap

class RoadmapService:
    def create_roadmap(
        self,
        db: Session,
        title: str,
        description: str | None,
    ):
        roadmap = Roadmap(
            title=title,
            description=description,
        )

        db.add(roadmap)

        db.commit()

        db.refresh(roadmap)

        return roadmap

    def get_roadmaps(
        self,
        db:Session,
        limit: int = 20,
        offset: int = 0,
    ):
        return (
            db.query(Roadmap)
            .order_by(
                Roadmap.created_at.desc()
            )
            .offset(offset)
            .limit(limit)
            .all()
        )
    
    def get_roadmap_by_id(
        self,
        db:Session,
        roadmap_id: UUID
    ):
        return (
            db.get(
                Roadmap,
                roadmap_id
            )
        )

    def add_topic_to_roadmap(
        self,
        db: Session,
        roadmap_id: UUID,
        topic_id: UUID,
        order_index: int,
    ):
        roadmap = db.get(
            Roadmap,
            roadmap_id,
        )

        if not roadmap:
            raise ValueError(
                "Roadmap not found"
            )
        
        topic = db.get(
            Topic,
            topic_id,
        )

        if not topic:
            raise ValueError(
                "Topic not found"
            )

        roadmap_topic = RoadmapTopic(
            roadmap_id=roadmap_id,
            topic_id=topic_id,
            order_index=order_index,
        )

        db.add(roadmap_topic)

        db.commit()
        
        db.refresh(roadmap_topic)
        
        return roadmap_topic