from uuid import UUID
from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base, UUIDMixin

class RoadmapTopic(Base, UUIDMixin):
    __tablename__ = "roadmap_topics"
    roadmap_id: Mapped[UUID]=mapped_column(
        ForeignKey(
            "roadmaps.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )
    topic_id: Mapped[UUID]=mapped_column(
        ForeignKey(
            "topics.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )
    order_index: Mapped[int]=mapped_column(
        Integer,
        nullable=False
    )
    roadmap = relationship(
        "Roadmap",
        back_populates="topics"
    )
    topic = relationship(
        "Topic",
        back_populates="roadmaps"
    )
    __table_args__ = (
        UniqueConstraint(
            "roadmap_id",
            "topic_id",
            name="uq_roadmap_topic",
        ),
        UniqueConstraint(
            "roadmap_id",
            "order_index",
            name="uq_roadmap_order",
        ),
    )