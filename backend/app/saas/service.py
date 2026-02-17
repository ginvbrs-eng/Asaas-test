"""SaaS services for quotas and subscription lifecycle."""

from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


async def check_quota(session: AsyncSession, org_id: int, feature_key: str) -> None:
    """Validate whether organization can use a feature."""
    # TODO: load plan limits + usage counter and raise if limit reached.
    _ = (session, org_id, feature_key)


async def increment_usage(session: AsyncSession, org_id: int, feature_key: str) -> None:
    """Increment usage counter for quota tracking."""
    # TODO: upsert usage counter in current billing period.
    _ = (session, org_id, feature_key)


async def update_subscription(session: AsyncSession, org_id: int, plan_id: int) -> None:
    """Switch organization subscription plan."""
    # TODO: validate plan, update subscription row, recalculate limits.
    _ = (session, org_id, plan_id)


async def enforce_readonly_mode(session: AsyncSession, org_id: int) -> None:
    """Block write actions if subscription is expired."""
    # TODO: check subscription expiration and raise when writes are blocked.
    _ = (session, org_id)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Readonly mode enforcement not implemented")
