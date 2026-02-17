"""SQLAlchemy async database setup."""

from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy import MetaData, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

metadata = MetaData()


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""

    metadata = metadata


engine = create_async_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a DB session per request."""
    async with SessionLocal() as session:
        yield session


async def ping_database() -> None:
    """Check that database connection is available."""
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))
