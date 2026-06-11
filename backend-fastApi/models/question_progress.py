from uuid import UUID

from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from models.base import (
    Base,
    UUIDMixin,
    TimestampMixin,
)

from models.enums import (
    QuestionStatus,
)


class QuestionProgress(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "question_progress"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    question_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "questions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    status: Mapped[QuestionStatus] = mapped_column(
        Enum(QuestionStatus),
        nullable=False,
        default=QuestionStatus.NOT_ATTEMPTED,
    )

    user = relationship(
        "User",
        back_populates="question_progress",
    )

    question = relationship(
        "Question",
        back_populates="progress",
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "question_id",
            name="uq_user_question_progress",
        ),
    )