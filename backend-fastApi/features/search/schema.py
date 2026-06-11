from uuid import UUID

from pydantic import BaseModel


class SearchTopicResponse(
    BaseModel
):
    id: UUID

    title: str

    slug: str

    model_config = {
        "from_attributes": True,
    }