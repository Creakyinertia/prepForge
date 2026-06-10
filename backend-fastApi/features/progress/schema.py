from uuid import UUID
from pydantic import BaseModel

from models.enums import (
    TopicProgressStatus,
)

class UpdateProgressRequest(
    BaseModel
):
    status: TopicProgressStatus

class ProgressResponse(
    BaseModel
):
    id: UUID

    topic_id: UUID

    status: TopicProgressStatus

    model_config = {
        "from_attributes": True
    }