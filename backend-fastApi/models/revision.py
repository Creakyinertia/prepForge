from datetime import datetime
from uuid import UUID
from sqlalchemy import DateTime, ForeignKey, Integer, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import (
    Base,
    UUIDMixin,
    TimestampMixin,
)

class Revision(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "revisions"

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

    due_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    revision_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    user = relationship(
        "User",
        back_populates="revisions",
    )

    topic = relationship(
        "Topic",
        back_populates="revisions",
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "topic_id",
            name="uq_revision_user_topic",
        ),
        Index(
            "ix_revision_user_due",
            "user_id",
            "due_at",
        ),
    )