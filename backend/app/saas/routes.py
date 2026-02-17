"""HTTP routes for SaaS management operations."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/saas", tags=["saas"])


@router.get("/status")
async def saas_status() -> dict[str, str]:
    """Simple endpoint to validate SaaS router wiring."""
    return {"status": "todo"}
