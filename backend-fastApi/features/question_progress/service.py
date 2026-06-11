from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundError
from models.question import Question
from models.question_progress import (
    QuestionProgress,
)

from models.enums import (
    QuestionStatus,
)


class QuestionProgressService:

    def update_progress(
        self,
        db: Session,
        user_id: UUID,
        question_id: UUID,
        status: QuestionStatus,
    ):
        question = db.get(
            Question,
            question_id,
        )

        if not question:
            raise NotFoundError(
                "Question not found",
            )

        progress = (
            db.query(QuestionProgress)
            .filter(
                QuestionProgress.user_id == user_id,
                QuestionProgress.question_id == question_id,
            )
            .first()
        )

        if not progress:
            progress = QuestionProgress(
                user_id=user_id,
                question_id=question_id,
                status=status,
            )

            db.add(progress)

        else:
            progress.status = status

        db.commit()
        db.refresh(progress)

        return progress
