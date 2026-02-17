"""Subscription plan model definitions."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from sqlalchemy import JSON, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class Plan(BaseModel):
    """Billing plan with quotas."""

    __tablename__ = "plans"

    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price_monthly: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    limits_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
