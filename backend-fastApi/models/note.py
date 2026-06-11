from uuid import UUID
from sqlalchemy import ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import (
    Base,
    UUIDMixin,
    TimestampMixin,
)

class Note(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "notes"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    topic_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "topics.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="notes",
    )

    topic = relationship(
        "Topic",
        back_populates="notes",
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "topic_id",
            name="uq_user_topic_note",
        ),
    )