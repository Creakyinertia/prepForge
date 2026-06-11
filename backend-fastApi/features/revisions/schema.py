from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class RevisionResponse(
    BaseModel
):
    id: UUID
    topic_id: UUID
    due_at: datetime
    revision_count: int

    model_config = {
        "from_attributes": True,
    }