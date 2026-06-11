from uuid import UUID
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import (
    Base,
    UUIDMixin,
    TimestampMixin,
)

class Resource(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "resources"

    topic_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "topics.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    resource_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    topic = relationship(
        "Topic",
        back_populates="resources",
    )