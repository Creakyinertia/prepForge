from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from dependencies.auth import (
    get_current_user,
)
from features.notes.schema import (
    NoteResponse,
    UpsertNoteRequest,
)
from features.notes.service import (
    NoteService,
)
from models.user import User

router = APIRouter()
note_service = NoteService()

@router.put(
    "/{topic_id}",
    response_model=NoteResponse,
)
def upsert_note(
    topic_id: UUID,
    payload: UpsertNoteRequest,
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    try:
        return note_service.upsert_note(
            db,
            current_user.id,
            topic_id,
            payload.content,
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Topic not found",
        )


@router.get(
    "/{topic_id}",
    response_model=NoteResponse,
)
def get_note(
    topic_id: UUID,
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    note = note_service.get_note(
        db,
        current_user.id,
        topic_id,
    )

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    return note