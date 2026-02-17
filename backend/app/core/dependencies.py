"""Reusable FastAPI dependencies."""

from __future__ import annotations

from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.tenant import get_current_org


async def db_session_dependency() -> AsyncGenerator[AsyncSession, None]:
    """Provide a typed DB session dependency."""
    async for session in get_db_session():
        yield session


async def current_org_dependency(org_id: int = Depends(get_current_org)) -> int:
    """Provide typed organization id dependency."""
    return org_id
