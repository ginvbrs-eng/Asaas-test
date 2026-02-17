"""Inventory module request/response schemas."""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel


class ProductCreate(BaseModel):
    """Payload for creating a product."""

    name: str
    sku: str
    price: Decimal
    stock: int


class ProductRead(ProductCreate):
    """Read model for product resources."""

    id: int
    org_id: int
