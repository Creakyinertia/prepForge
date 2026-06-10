from uuid import UUID

from sqlalchemy.orm import Session

from models.topic import Topic

from models.topic_progress import (
    TopicProgress,
)

from models.enums import (
    TopicProgressStatus,
)

class ProgressService:
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
            raise ValueError(
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
    
        if not progress:
            progress = TopicProgress(
                user_id=user_id,
                topic_id=topic_id,
                status=status,
            )
    
            db.add(progress)
        else:
            progress.status = status
    
        db.commit()
    
        db.refresh(progress)
    
        return progress