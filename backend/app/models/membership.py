"""Membership model definitions."""

from __future__ import annotations

from enum import StrEnum

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class MembershipRole(StrEnum):
    """Supported organization roles."""

    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class MembershipStatus(StrEnum):
    """Supported membership statuses."""

    ACTIVE = "active"
    INVITED = "invited"
    SUSPENDED = "suspended"


class Membership(BaseModel):
    """User membership in an organization."""

    __tablename__ = "memberships"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False, index=True)
    role: Mapped[MembershipRole] = mapped_column(Enum(MembershipRole), nullable=False)
    status: Mapped[MembershipStatus] = mapped_column(Enum(MembershipStatus), nullable=False, default=MembershipStatus.ACTIVE)
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)
