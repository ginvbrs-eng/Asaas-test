"""Assets module schemas."""

from __future__ import annotations

from pydantic import BaseModel


class AssetCreate(BaseModel):
    """Payload for creating an asset."""

    name: str
    code: str
