"""Assets module API routes."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/assets", tags=["assets"])


@router.get("/")
async def get_assets() -> dict[str, str]:
    """Placeholder endpoint for assets list."""
    return {"status": "todo"}
