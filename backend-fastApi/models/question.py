from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Enum

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from models.base import (
    Base,
    UUIDMixin,
    TimestampMixin,
)

from models.enums import QuestionDifficulty


class Question(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "questions"

    topic_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "topics.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    answer: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    difficulty: Mapped[QuestionDifficulty] = mapped_column(
        Enum(QuestionDifficulty),
        nullable=False,
    )

    topic = relationship(
        "Topic",
        back_populates="questions",
    )
    progress = relationship(
        "QuestionProgress",
        back_populates="question",
        cascade="all, delete-orphan",
    )