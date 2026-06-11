from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from features.topics.schema import (
    CreateTopicRequest,
    TopicResponse,
)
from dependencies.admin import get_current_admin
from features.topics.service import (
    TopicService,
)

router = APIRouter()

topic_service = TopicService()

@router.post(
    "",
    response_model=TopicResponse,
    dependencies=[
        Depends(get_current_admin)
    ],
)
def create_topic(
    payload: CreateTopicRequest,
    db: Session = Depends(get_db),
):
    return topic_service.create_topic(
        db,
        payload.title,
        payload.description,
    )

@router.get(
    "",
    response_model=list[TopicResponse],
)
def get_topics(
    db: Session = Depends(get_db),
):
    return topic_service.get_topics(
        db
    )

@router.get(
    "/{topic_id}",
    response_model=TopicResponse,
)
def get_topic(
    topic_id: UUID,
    db: Session = Depends(get_db),
):
    topic = (
        topic_service.get_topic_by_id(
            db,
            topic_id,
        )
    )

    if not topic:
        raise HTTPException(
            status_code=404,
            detail="Topic not found",
        )

    return topic