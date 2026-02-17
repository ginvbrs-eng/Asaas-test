"""Inventory module API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.tenant import get_current_org
from app.modules.inventory import service

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/products")
async def get_products(
    org_id: int = Depends(get_current_org),
    session: AsyncSession = Depends(get_db_session),
):
    """List products for current organization."""
    products = await service.list_products(session, org_id)
    return products
