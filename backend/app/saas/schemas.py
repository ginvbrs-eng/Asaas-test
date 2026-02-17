"""Pydantic schemas for SaaS operations."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class SubscriptionUpdateRequest(BaseModel):
    """Request payload to switch plan."""

    plan_id: int


class SubscriptionResponse(BaseModel):
    """Basic subscription response payload."""

    organization_id: int
    plan_id: int
    status: str
    current_period_end: datetime
