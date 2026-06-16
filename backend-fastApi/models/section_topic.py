from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from models.base import (
    Base,
    UUIDMixin,
)


class SectionTopic(
    Base,
    UUIDMixin,
):
    __tablename__ = "section_topics"

    section_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "roadmap_sections.id",
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

    order_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    section = relationship(
        "RoadmapSection",
        back_populates="topics",
    )

    topic = relationship(
        "Topic",
        back_populates="sections",
    )
