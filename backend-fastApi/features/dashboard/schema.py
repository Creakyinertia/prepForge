from pydantic import BaseModel


class DashboardResponse(
    BaseModel
):
    total_topics_completed: int

    total_topics_in_progress: int

    total_notes: int

    due_revisions: int

    roadmaps_started: int