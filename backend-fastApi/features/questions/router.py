from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from dependencies.admin import get_current_admin

from core.database import get_db

from features.questions.schema import (
    CreateQuestionRequest,
    UpdateQuestionRequest,
    QuestionResponse,
)

from features.questions.service import (
    QuestionService,
)


router = APIRouter()

question_service = QuestionService()


@router.post(
    "",
    response_model=QuestionResponse,
    dependencies=[
        Depends(get_current_admin)
    ],
)
def create_question(
    payload: CreateQuestionRequest,
    db: Session = Depends(get_db),
):
    try:
        return question_service.create_question(
            db,
            payload.topic_id,
            payload.title,
            payload.answer,
            payload.difficulty,
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Topic not found",
        )


@router.get(
    "/{question_id}",
    response_model=QuestionResponse,
)
def get_question(
    question_id: UUID,
    db: Session = Depends(get_db),
):
    question = question_service.get_question(
        db,
        question_id,
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found",
        )

    return question


@router.get(
    "/topic/{topic_id}",
    response_model=list[QuestionResponse],
)
def get_topic_questions(
    topic_id: UUID,
    db: Session = Depends(get_db),
):
    return question_service.get_topic_questions(
        db,
        topic_id,
    )


@router.put(
    "/{question_id}",
    response_model=QuestionResponse,
    dependencies=[
        Depends(get_current_admin)
    ],
)
def update_question(
    question_id: UUID,
    payload: UpdateQuestionRequest,
    db: Session = Depends(get_db),
):
    try:
        return question_service.update_question(
            db,
            question_id,
            payload.title,
            payload.answer,
            payload.difficulty,
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Question not found",
        )


@router.delete(
    "/{question_id}",
)
def delete_question(
    question_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        question_service.delete_question(
            db,
            question_id,
        )

        return {
            "message": "Question deleted"
        }

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Question not found",
        )