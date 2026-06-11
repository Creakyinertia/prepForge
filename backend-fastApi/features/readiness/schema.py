from uuid import UUID

from pydantic import BaseModel


class TopicReadinessResponse(
    BaseModel
):
    topic_id: UUID

    topic_title: str

    topic_completed: bool

    total_questions: int

    mastered_questions: int

    due_revisions: int

    readiness_score: float

class RoadmapReadinessResponse(
    BaseModel
):
    roadmap_id: UUID

    roadmap_title: str

    total_topics: int

    average_readiness_score: float