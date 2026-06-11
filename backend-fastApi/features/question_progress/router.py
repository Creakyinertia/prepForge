from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from core.exceptions import (
    AppError,
    to_http_exception,
)
from core.database import get_db

from dependencies.auth import (
    get_current_user,
)

from models.user import User

from features.question_progress.schema import (
    UpdateQuestionProgressRequest,
    QuestionProgressResponse,
)

from features.question_progress.service import (
    QuestionProgressService,
)


router = APIRouter()

question_progress_service = (
    QuestionProgressService()
)


@router.put(
    "/{question_id}",
    response_model=QuestionProgressResponse,
)
def update_question_progress(
    question_id: UUID,
    payload: UpdateQuestionProgressRequest,
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    try:
        return question_progress_service.update_progress(
            db,
            current_user.id,
            question_id,
            payload.status,
        )

    except AppError as exc:
        raise to_http_exception(exc) from exc
