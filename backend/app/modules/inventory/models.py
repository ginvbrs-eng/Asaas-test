"""Inventory module ORM models."""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Index, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import OrganizationBase


class Category(OrganizationBase):
    """Product category scoped by organization."""

    __tablename__ = "inventory_categories"

    name: Mapped[str] = mapped_column(String(120), nullable=False)


class Product(OrganizationBase):
    """Product item scoped by organization."""

    __tablename__ = "inventory_products"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sku: Mapped[str] = mapped_column(String(120), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    stock: Mapped[int] = mapped_column(nullable=False, default=0)

    __table_args__ = (
        Index("ix_inventory_products_org_id_id", "org_id", "id"),
        Index("ix_inventory_products_org_id_sku", "org_id", "sku", unique=True),
    )
