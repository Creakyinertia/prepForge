from uuid import UUID
from sqlalchemy.orm import Session
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
