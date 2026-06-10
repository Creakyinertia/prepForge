from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from core.database import get_db

from dependencies.auth import (
    get_current_user,
)
from features.progress.service import ProgressService
from features.progress.schema import ProgressResponse, UpdateProgressRequest
from models.user import User

router = APIRouter()

progress_service = ProgressService()

@router.put(
    "/{topic_id}",
    response_model=ProgressResponse,
)
def update_progress(
    topic_id: UUID,
    payload: UpdateProgressRequest,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    return progress_service.update_progress(
        db,
        current_user.id,
        topic_id,
        payload.status,
    )