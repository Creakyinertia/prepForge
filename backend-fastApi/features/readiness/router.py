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

from features.readiness.schema import (
    TopicReadinessResponse,
    RoadmapReadinessResponse,
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

    except AppError as exc:
        raise to_http_exception(exc) from exc

@router.get(
    "/roadmaps/{roadmap_id}",
    response_model=RoadmapReadinessResponse,
)
def get_roadmap_readiness(
    roadmap_id: UUID,
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(
        get_db
    ),
):
    try:
        return (
            readiness_service.get_roadmap_readiness(
                db,
                current_user.id,
                roadmap_id,
            )
        )

    except AppError as exc:
        raise to_http_exception(exc) from exc

@router.get(
    "/roadmaps",
)
def get_all_roadmap_readiness(
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(
        get_db
    ),
):
    return (
        readiness_service.get_all_roadmap_readiness(
            db,
            current_user.id,
        )
    )
