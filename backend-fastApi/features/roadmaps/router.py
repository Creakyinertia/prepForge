from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from features.roadmaps.schema import (
    CreateRoadmapRequest,
    RoadmapResponse,
)
from features.roadmaps.service import (
    RoadmapService,
)

router = APIRouter()

roadmap_service = RoadmapService()

@router.post(
    "",
    response_model=RoadmapResponse,
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
        raise HTTPException(
            status_code=404,
            detail="Roadmap not found",
        )

    return roadmap