from datetime import datetime
from datetime import timezone
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from core.exceptions import NotFoundError
from models.enums import (
    TopicProgressStatus,
    QuestionStatus,
)

from models.question import Question
from models.question_progress import (
    QuestionProgress,
)
from models.revision import Revision
from models.topic import Topic
from models.topic_progress import (
    TopicProgress,
)
from models.roadmap import Roadmap
from models.roadmap_topic import RoadmapTopic

class ReadinessService:

    def get_topic_readiness(
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
            raise NotFoundError(
                "Topic not found",
            )

        progress = (
            db.query(TopicProgress)
            .filter(
                TopicProgress.user_id == user_id,
                TopicProgress.topic_id == topic_id,
            )
            .first()
        )

        topic_completed = (
            progress is not None
            and progress.status
            == TopicProgressStatus.COMPLETED
        )

        total_questions = (
            db.query(func.count())
            .select_from(Question)
            .filter(
                Question.topic_id == topic_id,
            )
            .scalar()
        )

        mastered_questions = (
            db.query(func.count())
            .select_from(QuestionProgress)
            .join(
                Question,
                Question.id
                == QuestionProgress.question_id,
            )
            .filter(
                Question.topic_id == topic_id,
                QuestionProgress.user_id == user_id,
                QuestionProgress.status
                == QuestionStatus.MASTERED,
            )
            .scalar()
        )

        due_revisions = (
            db.query(func.count())
            .select_from(Revision)
            .filter(
                Revision.user_id == user_id,
                Revision.topic_id == topic_id,
                Revision.due_at
                <= datetime.now(
                    timezone.utc
                ),
            )
            .scalar()
        )

        score = self.calculate_score(
            topic_completed,
            total_questions,
            mastered_questions,
            due_revisions,
        )

        return {
            "topic_id": topic.id,
            "topic_title": topic.title,
            "topic_completed": topic_completed,
            "total_questions": total_questions,
            "mastered_questions": mastered_questions,
            "due_revisions": due_revisions,
            "readiness_score": score,
        }

    def calculate_score(
        self,
        topic_completed: bool,
        total_questions: int,
        mastered_questions: int,
        due_revisions: int,
    ):
        score = 0

        if topic_completed:
            score += 40

        if total_questions:
            score += (
                mastered_questions
                / total_questions
            ) * 50

        if due_revisions == 0:
            score += 10

        return round(score, 2)
    
    def get_roadmap_readiness(
        self,
        db: Session,
        user_id: UUID,
        roadmap_id: UUID,
    ):
        roadmap = db.get(
            Roadmap,
            roadmap_id,
        )

        if not roadmap:
            raise NotFoundError(
                "Roadmap not found"
            )

        roadmap_topics = (
            db.query(
                RoadmapTopic,
            )
            .filter(
                RoadmapTopic.roadmap_id
                == roadmap_id
            )
            .all()
        )

        topic_ids = [
            rt.topic_id
            for rt in roadmap_topics
        ]

        total_topics = len(
            topic_ids
        )

        if not topic_ids:
            return {
                "roadmap_id": roadmap.id,
                "roadmap_title": roadmap.title,
                "total_topics": 0,
                "completed_topics": 0,
                "readiness_score": 0,
            }

        completed_topics = (
            db.query(
                TopicProgress,
            )
            .filter(
                TopicProgress.user_id
                == user_id,
                TopicProgress.topic_id.in_(
                    topic_ids
                ),
                TopicProgress.status
                == TopicProgressStatus.COMPLETED,
            )
            .count()
        )

        total_questions = (
            db.query(
                Question,
            )
            .filter(
                Question.topic_id.in_(
                    topic_ids
                )
            )
            .count()
        )

        mastered_questions = (
            db.query(
                QuestionProgress,
            )
            .join(
                Question,
                Question.id
                == QuestionProgress.question_id,
            )
            .filter(
                QuestionProgress.user_id
                == user_id,
                QuestionProgress.status
                == QuestionStatus.MASTERED,
                Question.topic_id.in_(
                    topic_ids
                ),
            )
            .count()
        )

        completion_score = (
            completed_topics
            / total_topics
        ) * 50

        question_score = 0

        if total_questions:
            question_score = (
                mastered_questions
                / total_questions
            ) * 50

        readiness_score = round(
            completion_score
            + question_score,
            2,
        )

        return {
            "roadmap_id": roadmap.id,
            "roadmap_title": roadmap.title,
            "total_topics": total_topics,
            "completed_topics": completed_topics,
            "readiness_score": readiness_score,
        }

    def get_all_roadmap_readiness(
        self,
        db: Session,
        user_id: UUID,
    ):
        roadmaps = (
            db.query(
                Roadmap
            )
            .order_by(
                Roadmap.title
            )
            .all()
        )
    
        return [
            self.get_roadmap_readiness(
                db,
                user_id,
                roadmap.id,
            )
            for roadmap in roadmaps
        ]
