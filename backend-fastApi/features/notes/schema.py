from uuid import UUID
from pydantic import BaseModel

class UpsertNoteRequest(
    BaseModel
):
    content: str

class NoteResponse(
    BaseModel
):
    id: UUID
    topic_id: UUID
    content: str

    model_config = {
        "from_attributes": True,
    }