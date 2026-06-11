from uuid import UUID

from pydantic import BaseModel
from features.bookmarks.schema import (
    BookmarkResponse,
)


class ContinueLearningTopic(
    BaseModel
):
    topic_id: UUID

    title: str

    slug: str

    progress_status: str


class HomeResponse(
    BaseModel
):
    continue_learning: list[
        ContinueLearningTopic
    ]

    due_revisions: int

    recent_bookmarks: list[
        BookmarkResponse
    ]