from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin
from models.roadmap_topic import RoadmapTopic


class Roadmap(Base, TimestampMixin, UUIDMixin, SoftDeleteMixin):
    __tablename__ = "roadmaps"
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_published: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    topics = relationship(
        "RoadmapTopic",
        back_populates="roadmap",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="RoadmapTopic.order_index",
    )
    sections = relationship(
        "RoadmapSection",
        back_populates="roadmap",
        cascade="all, delete-orphan",
        order_by="RoadmapSection.order_index",
    )
