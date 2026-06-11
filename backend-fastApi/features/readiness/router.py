from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from core.database import get_db

from dependencies.auth import (
    get_current_user,
)

from features.readiness.schema import (
    TopicReadinessResponse,
)

from features.readiness.service import (
    ReadinessService,
)

from models.user import User


router = APIRouter()

readiness_service = ReadinessService()


@router.get(
    "/topics/{topic_id}",
    response_model=TopicReadinessResponse,
)
def get_topic_readiness(
    topic_id: UUID,
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    try:
        return readiness_service.get_topic_readiness(
            db,
            current_user.id,
            topic_id,
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Topic not found",
        )