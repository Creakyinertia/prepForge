from enum import Enum

class TopicProgressStatus(
    str,
    Enum,
):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class ResourceType(
    str,
    Enum,
):
    ARTICLE = "ARTICLE"
    VIDEO = "VIDEO"
    DOCUMENTATION = "DOCUMENTATION"
    OTHER = "OTHER"

class QuestionDifficulty(
    str,
    Enum,
):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"