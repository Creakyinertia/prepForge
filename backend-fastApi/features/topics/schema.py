from uuid import UUID
from pydantic import BaseModel, ConfigDict

class CreateTopicRequest(BaseModel):
    title: str
    description: str | None = None

class TopicResponse(BaseModel):
    id: UUID
    title: str
    slug: str
    description: str | None
    
    model_config = ConfigDict(
        from_attributes=True
    )
