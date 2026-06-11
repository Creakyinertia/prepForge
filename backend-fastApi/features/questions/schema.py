from uuid import UUID

from pydantic import BaseModel

from models.enums import (
    QuestionDifficulty,
)


class CreateQuestionRequest(
    BaseModel
):
    topic_id: UUID

    title: str

    answer: str

    difficulty: QuestionDifficulty


class UpdateQuestionRequest(
    BaseModel
):
    title: str

    answer: str

    difficulty: QuestionDifficulty


class QuestionResponse(
    BaseModel
):
    id: UUID

    topic_id: UUID

    title: str

    answer: str

    difficulty: QuestionDifficulty

    model_config = {
        "from_attributes": True,
    }