from enum import Enum


class TopicProgressStatus(
    str,
    Enum,
):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"