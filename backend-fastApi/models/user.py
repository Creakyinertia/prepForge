import uuid
from sqlalchemy import Boolean,String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base, UUIDMixin, TimestampMixin

class User(Base, TimestampMixin, UUIDMixin):
    __tablename__ = "users"

    username: Mapped[str]=mapped_column(
        String(55),
        unique=True,
        nullable=False
    )
    email: Mapped[str]=mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
    hashed_password: Mapped[str]=mapped_column(
        String(255),
        nullable=False
    )
    is_active: Mapped[bool]=mapped_column(
        Boolean,
        default=True
    )
    is_verified: Mapped[bool]=mapped_column(
        Boolean,
        default=False
    )
    refresh_tokens=relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    progress = relationship(
        "TopicProgress",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    revisions = relationship(
        "Revision",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    notes = relationship(
        "Note",
        back_populates="user",
        cascade="all, delete-orphan",
    )