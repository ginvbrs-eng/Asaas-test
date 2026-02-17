"""Tenant context helpers for single-database multi-tenancy."""

from __future__ import annotations

from contextvars import ContextVar

from fastapi import Depends, HTTPException, Request, status

from app.core.security import get_current_user

current_org_id: ContextVar[int | None] = ContextVar("current_org_id", default=None)


def set_current_org(org_id: int | None) -> None:
    """Store organization id in request-local context."""
    current_org_id.set(org_id)


def get_current_org_id() -> int:
    """Return active organization id from context."""
    org_id = current_org_id.get()
    if org_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing organization context")
    return org_id


async def extract_org_from_request(request: Request) -> int | None:
    """Extract organization id from headers or token claims."""
    raw_org_id = request.headers.get("X-Organization-Id")
    if raw_org_id is None:
        return None
    try:
        return int(raw_org_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid organization id") from exc


async def get_current_org(user: dict = Depends(get_current_user)) -> int:
    """Dependency to resolve organization id from authenticated context."""
    # TODO: prefer org claim in JWT and validate membership before returning org id.
    org_id = user.get("org_id")
    if org_id is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No organization selected")
    return int(org_id)
