from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.exceptions import (
    AppError,
    to_http_exception,
)
from dependencies.auth import (
    get_current_user,
)
from features.revisions.schema import (
    RevisionResponse,
)
from features.revisions.service import (
    RevisionService,
)
from models.user import User

router = APIRouter()

revision_service = RevisionService()

@router.get(
    "/due",
    response_model=list[RevisionResponse],
)
def get_due_revisions(
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    return revision_service.get_due_revisions(
        db,
        current_user.id,
    )

@router.post(
    "/{revision_id}/complete",
    response_model=RevisionResponse,
)
def complete_revision(
    revision_id: UUID,
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    try:
        return revision_service.complete_revision(
            db,
            revision_id,
            current_user.id,
        )
    except AppError as exc:
        raise to_http_exception(exc) from exc
