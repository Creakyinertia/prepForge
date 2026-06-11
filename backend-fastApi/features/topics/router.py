from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.exceptions import (
    AppError,
    NotFoundError,
    to_http_exception,
)
from features.topics.schema import (
    CreateTopicRequest,
    UpdateTopicRequest,
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
    try:
        return topic_service.create_topic(
            db,
            payload.title,
            payload.description,
            payload.content,
        )
    except AppError as exc:
        raise to_http_exception(exc) from exc

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
        raise to_http_exception(
            NotFoundError("Topic not found")
        )

    return topic

@router.put(
    "/{topic_id}",
    response_model=TopicResponse,
    dependencies=[
        Depends(get_current_admin)
    ],
)
def update_topic(
    topic_id: UUID,
    payload: UpdateTopicRequest,
    db: Session = Depends(get_db),
):
    try:
        return topic_service.update_topic(
            db,
            topic_id,
            payload.title,
            payload.description,
            payload.content,
        )

    except AppError as exc:
        raise to_http_exception(exc) from exc
