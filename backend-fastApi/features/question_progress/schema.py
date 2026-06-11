from uuid import UUID

from pydantic import BaseModel

from models.enums import (
    QuestionStatus,
)


class UpdateQuestionProgressRequest(
    BaseModel
):
    status: QuestionStatus


class QuestionProgressResponse(
    BaseModel
):
    id: UUID

    question_id: UUID

    status: QuestionStatus

    model_config = {
        "from_attributes": True,
    }