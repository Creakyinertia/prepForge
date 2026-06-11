from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from core.exceptions import (
    AppError,
    to_http_exception,
)
from core.database import get_db

from dependencies.auth import (
    get_current_user,
)

from models.user import User

from features.bookmarks.schema import (
    BookmarkResponse,
)

from features.bookmarks.service import (
    BookmarkService,
)

router = APIRouter()

bookmark_service = BookmarkService()


@router.post(
    "/{topic_id}",
    response_model=BookmarkResponse,
)
def create_bookmark(
    topic_id: UUID,
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    try:
        return bookmark_service.create_bookmark(
            db,
            current_user.id,
            topic_id,
        )

    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.delete(
    "/{topic_id}",
)
def remove_bookmark(
    topic_id: UUID,
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    try:
        bookmark_service.remove_bookmark(
            db,
            current_user.id,
            topic_id,
        )

        return {
            "message": "Bookmark removed",
        }

    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.get(
    "",
    response_model=list[BookmarkResponse],
)
def get_bookmarks(
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    return bookmark_service.get_bookmarks(
        db,
        current_user.id,
    )
