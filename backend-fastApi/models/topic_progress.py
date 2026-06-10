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
    TopicProgressStatus,
)

class TopicProgress(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "topic_progress"

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

    status: Mapped[
        TopicProgressStatus
    ] = mapped_column(
        Enum(TopicProgressStatus),
        nullable=False,
        default=TopicProgressStatus.NOT_STARTED,
    )

    user = relationship(
        "User",
        back_populates="progress",
    )
    
    topic = relationship(
        "Topic",
        back_populates="progress",
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "topic_id",
            name="uq_user_topic_progress",
        ),
    )