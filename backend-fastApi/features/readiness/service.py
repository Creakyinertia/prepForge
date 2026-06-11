from datetime import datetime
from datetime import timezone
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

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
            raise ValueError(
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