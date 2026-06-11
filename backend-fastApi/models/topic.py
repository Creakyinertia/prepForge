from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base, TimestampMixin, UUIDMixin, SoftDeleteMixin

class Topic(Base, TimestampMixin, UUIDMixin, SoftDeleteMixin):
    __tablename__ = "topics"
    title: Mapped[str]=mapped_column(
        String(255),
        nullable=False
    )
    slug: Mapped[str]=mapped_column(
        String(255),
        index=True,
        nullable=False,
        unique=True
    )
    description: Mapped[str | None]=mapped_column(
        Text,
        nullable=True
    )

    roadmaps = relationship(
        "RoadmapTopic",
        back_populates="topic",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    progress = relationship(
        "TopicProgress",
        back_populates="topic",
        cascade="all, delete-orphan",
    )
    revisions = relationship(
        "Revision",
        back_populates="topic",
        cascade="all, delete-orphan",
    )
    notes = relationship(
        "Note",
        back_populates="topic",
        cascade="all, delete-orphan",
    )
    resources = relationship(
        "Resource",
        back_populates="topic",
        cascade="all, delete-orphan",
    )