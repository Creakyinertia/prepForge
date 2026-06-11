from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from sqlalchemy.orm import Session

from core.database import get_db

from features.search.schema import (
    SearchTopicResponse,
)

from features.search.service import (
    SearchService,
)


router = APIRouter()

search_service = SearchService()


@router.get(
    "/topics",
    response_model=list[
        SearchTopicResponse
    ],
)
def search_topics(
    q: str = Query(
        min_length=1,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):
    return search_service.search_topics(
        db,
        q,
        limit,
    )