"""Inventory module service layer."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.models import Product


async def list_products(session: AsyncSession, org_id: int) -> list[Product]:
    """List products for active organization."""
    stmt = select(Product).where(Product.org_id == org_id)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def create_product(session: AsyncSession, org_id: int, payload: dict) -> Product:
    """Create product in organization scope."""
    # TODO: validate payload via schema and enforce quotas.
    product = Product(org_id=org_id, **payload)
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product
