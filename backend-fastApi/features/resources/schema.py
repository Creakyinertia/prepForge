from uuid import UUID
from pydantic import BaseModel, HttpUrl
from models.enums import ResourceType

class CreateResourceRequest(
    BaseModel
):
    title: str
    url: HttpUrl
    resource_type: ResourceType

class ResourceResponse(
    BaseModel
):
    id: UUID
    topic_id: UUID
    title: str
    url: str
    resource_type: ResourceType

    model_config = {
        "from_attributes": True,
    }