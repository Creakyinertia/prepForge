from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from dependencies.admin import get_current_admin

from core.database import get_db

from features.resources.schema import (
    CreateResourceRequest,
    ResourceResponse,
)

from features.resources.service import (
    ResourceService,
)


router = APIRouter()

resource_service = ResourceService()


@router.post(
    "/{topic_id}",
    response_model=ResourceResponse,
    dependencies=[
        Depends(get_current_admin)
    ],
)
def create_resource(
    topic_id: UUID,
    payload: CreateResourceRequest,
    db: Session = Depends(get_db),
):
    try:
        return resource_service.create_resource(
            db,
            topic_id,
            payload.title,
            str(payload.url),
            payload.resource_type,
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Topic not found",
        )


@router.get(
    "/{topic_id}",
    response_model=list[ResourceResponse],
)
def get_topic_resources(
    topic_id: UUID,
    db: Session = Depends(get_db),
):
    return resource_service.get_topic_resources(
        db,
        topic_id,
    )