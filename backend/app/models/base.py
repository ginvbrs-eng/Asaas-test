"""Base ORM mixins for shared fields and tenant scope."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Index, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TimestampMixin:
    """Common timestamp columns."""

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class IdMixin:
    """Common integer primary key."""

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)


class BaseModel(Base, IdMixin, TimestampMixin):
    """Base model for global/shared entities."""

    __abstract__ = True


class OrganizationBase(Base, IdMixin, TimestampMixin):
    """Base model for tenant-scoped entities."""

    __abstract__ = True

    org_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    @classmethod
    def __declare_last__(cls) -> None:
        """Add standard org composite index for tenant-scoped rows."""
        if not cls.__table__.indexes:
            Index(f"ix_{cls.__tablename__}_org_id_id", cls.__table__.c.org_id, cls.__table__.c.id)
