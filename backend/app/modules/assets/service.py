"""Assets module service layer."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession


async def list_assets(session: AsyncSession, org_id: int) -> list[dict[str, object]]:
    """List assets in tenant scope."""
    # TODO: query `Asset` model filtered by `org_id`.
    _ = (session, org_id)
    return []
