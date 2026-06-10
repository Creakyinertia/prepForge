from uuid import UUID
from pydantic import BaseModel, ConfigDict

class CreateRoadmapRequest(
    BaseModel
):
    title: str
    description: str | None = None

class RoadmapResponse(
    BaseModel
):
    id: UUID
    title: str
    description: str | None
    is_published: bool

    model_config = ConfigDict(
        from_attributes=True
    )
