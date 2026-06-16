from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from models.base import (
    Base,
    TimestampMixin,
    UUIDMixin,
)


class RoadmapSection(
    Base,
    TimestampMixin,
    UUIDMixin,
):
    __tablename__ = "roadmap_sections"

    roadmap_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "roadmaps.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    order_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    roadmap = relationship(
        "Roadmap",
        back_populates="sections",
    )

    topics = relationship(
        "SectionTopic",
        back_populates="section",
        cascade="all, delete-orphan",
        order_by="SectionTopic.order_index",
    )
