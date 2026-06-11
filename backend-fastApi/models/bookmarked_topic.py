from uuid import UUID

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


class BookmarkedTopic(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "bookmarked_topics"

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

    user = relationship(
        "User",
        back_populates="bookmarked_topics",
    )

    topic = relationship(
        "Topic",
        back_populates="bookmarked_by",
        lazy="joined",
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "topic_id",
            name="uq_user_topic_bookmark",
        ),
    )