"""FastAPI entrypoint for ASAAS platform."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import ping_database

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run startup and shutdown hooks."""
    # TODO: verify DB/Redis/MinIO connectivity and initialize resources.
    await ping_database()
    yield
    # TODO: close shared clients/resources.


app = FastAPI(
    title="ASAAS Platform API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    """Basic liveness endpoint."""
    return {"status": "ok"}


# TODO: include routers for auth, organizations, subscriptions, inventory, assets.
# app.include_router(...)
