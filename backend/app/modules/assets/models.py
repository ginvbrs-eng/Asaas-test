"""Assets module ORM models."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import OrganizationBase


class Asset(OrganizationBase):
    """Business asset scoped by organization."""

    __tablename__ = "assets"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(120), nullable=False)
