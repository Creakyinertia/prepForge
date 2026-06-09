from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from backend.connections.database import Base
import uuid
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)

    hashed_password = Column(String, nullable=False)

    is_verified =  Column(Boolean, default=True, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    last_updated = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    refresh_tokens = relationship(
        "RefreshToken",
        back_populates="user"
    )
    
    
    
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    token_hash = Column(
        String(255),
        nullable=False
    )

    expires_at = Column(
        DateTime,
        nullable=False
    )

    revoked_at = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    last_updated = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="refresh_tokens"
    )
    
    
    
# class UserProfile(Base):
#     __tablename__ = "user_profile"

#     id = Column(
#         String(36),
#         primary_key=True,
#         default=lambda: str(uuid.uuid4())
#     )

#     user_id = Column(
#         String(36),
#         ForeignKey("users.id", ondelete="CASCADE"),
#         nullable=False,
#     )

#     first_name =  Column(
#         String(255),
#         nullable=False
#     )

#     last_name =  Column(
#         String(255),
#         nullable=False
#     )

#     phone =  Column(
#         String(255),
#         nullable=False
#     )

#     bio = Column(
#     Text,
#         nullable=True
#     )

#     linkedin_url = Column(
#     String(255),
#     nullable=True
#     )

#     github_url = Column(
#         String(255),
#         nullable=True
#     )
    
#     resume_url = Column(
#         String(500),
#         nullable=True
#     )

#     created_at = Column(
#         DateTime,
#         default=datetime.utcnow,
#         nullable=False
#     )

#     last_updated = Column(
#         DateTime,
#         default=datetime.utcnow,
#         onupdate=datetime.utcnow,
#         nullable=False
#     )

#     user_profile = relationship(
#     "UserProfile",
#         back_populates="user"
#     )