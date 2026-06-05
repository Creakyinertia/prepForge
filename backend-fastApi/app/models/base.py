import uuid
from sqlalchemy import Datetime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

class Base(declarative_base):
    pass

class TimezoneMixin:
    created_at: Mapped[Datetime] = mapped_column(
        Datetime(timezone=True)
        server_default = func.now()
    )
    updated_at: Mapped[Datetime] = mapped_column(
        Datetime(timezone=True)
        server_default = func.now()
        onUpdate = func.now()
    )

class UUIDMixin:
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True)
        primary_key = True
        default = uuid.uuid4
    )