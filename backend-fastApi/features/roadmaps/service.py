from uuid import UUID
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.enums import TopicProgressStatus
from models.roadmap import Roadmap
from models.roadmap_topic import RoadmapTopic
from models.topic_progress import TopicProgress

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

    def get_roadmap_progress(
        self,
        db: Session,
        roadmap_id,
        user_id,
    ):
        roadmap = db.get(
            Roadmap,
            roadmap_id,
        )

        if not roadmap:
            raise ValueError(
                "Roadmap not found"
            )

        total_topics = (
            db.query(func.count())
            .select_from(RoadmapTopic)
            .filter(
                RoadmapTopic.roadmap_id == roadmap_id,
            )
            .scalar()
        )

        completed_topics = (
            db.query(func.count())
            .select_from(RoadmapTopic)
            .join(
                TopicProgress,
                TopicProgress.topic_id
                == RoadmapTopic.topic_id,
            )
            .filter(
                RoadmapTopic.roadmap_id == roadmap_id,
                TopicProgress.user_id == user_id,
                TopicProgress.status
                == TopicProgressStatus.COMPLETED,
            )
            .scalar()
        )

        progress_percentage = 0.0

        if total_topics:
            progress_percentage = round(
                (
                    completed_topics
                    / total_topics
                )
                * 100,
                2,
            )

        return {
            "roadmap_id": roadmap.id,
            "roadmap_title": roadmap.title,
            "total_topics": total_topics,
            "completed_topics": completed_topics,
            "progress_percentage": progress_percentage,
        }

    def get_all_roadmap_progress(
        self,
        db: Session,
        user_id,
    ):
        roadmaps = (
            db.query(Roadmap)
            .order_by(
                Roadmap.created_at.desc()
            )
            .all()
        )
    
        result = []
    
        for roadmap in roadmaps:
            result.append(
                self.get_roadmap_progress(
                    db,
                    roadmap.id,
                    user_id,
                )
            )
    
        return result