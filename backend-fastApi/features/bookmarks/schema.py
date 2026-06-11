from uuid import UUID

from pydantic import BaseModel


class BookmarkResponse(
    BaseModel
):
    id: UUID

    topic_id: UUID

    topic_title: str

    topic_slug: str
    
    topic_description: str | None

    model_config = {
        "from_attributes": True,
    }