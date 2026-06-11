from sqlalchemy.orm import Session

from models.topic import Topic


class SearchService:

    def search_topics(
        self,
        db: Session,
        query: str,
        limit: int = 20,
    ):
        return (
            db.query(Topic)
            .filter(
                Topic.title.ilike(
                    f"%{query}%"
                )
            )
            .limit(limit)
            .all()
        )