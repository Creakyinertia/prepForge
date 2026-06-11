from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.exceptions import (
    AppError,
    NotFoundError,
    to_http_exception,
)
from features.roadmaps.schema import (
    CreateRoadmapRequest,
    RoadmapResponse,
)
from features.roadmaps.schema import AddTopicToRoadmapRequest, RoadmapProgressResponse
from features.roadmaps.service import (
    RoadmapService,
)
from dependencies.admin import get_current_admin
from dependencies.auth import (
    get_current_user,
)
from models.user import User

router = APIRouter()

roadmap_service = RoadmapService()

@router.post(
    "",
    response_model=RoadmapResponse,
    dependencies=[
        Depends(get_current_admin)
    ],
)
def create_roadmap(
    payload: CreateRoadmapRequest,
    db: Session = Depends(get_db),
):
    return roadmap_service.create_roadmap(
        db,
        payload.title,
        payload.description,
    )

@router.get(
    "",
    response_model=list[RoadmapResponse],
)
def get_roadmaps(
    db: Session = Depends(get_db),
):
    return roadmap_service.get_roadmaps(
        db
    )

@router.get(
    "/{roadmap_id}",
    response_model=RoadmapResponse,
)
def get_roadmap(
    roadmap_id: UUID,
    db: Session = Depends(get_db),
):
    roadmap = (
        roadmap_service.get_roadmap_by_id(
            db,
            roadmap_id,
        )
    )

    if not roadmap:
        raise to_http_exception(
            NotFoundError("Roadmap not found")
        )

    return roadmap

@router.post(
    "/{roadmap_id}/topics",
    dependencies=[
        Depends(get_current_admin)
    ],
)
def add_topic_to_roadmap(
    roadmap_id: UUID,
    payload: AddTopicToRoadmapRequest,
    
    db: Session = Depends(get_db),
):
    try:
        return roadmap_service.add_topic_to_roadmap(
            db,
            roadmap_id,
            payload.topic_id,
            payload.order_index,
        )
    except AppError as exc:
        raise to_http_exception(exc) from exc

@router.get(
    "/{roadmap_id}/progress",
    response_model=RoadmapProgressResponse,
)
def get_roadmap_progress(
    roadmap_id: UUID,
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    try:
        return roadmap_service.get_roadmap_progress(
            db,
            roadmap_id,
            current_user.id,
        )
    except AppError as exc:
        raise to_http_exception(exc) from exc

@router.get(
    "/progress/all",
)
def get_all_roadmap_progress(
    current_user: User = Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    return roadmap_service.get_all_roadmap_progress(
        db,
        current_user.id,
    )
