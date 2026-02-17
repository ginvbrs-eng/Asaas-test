"""Ollama client abstraction."""

from __future__ import annotations

from typing import Any


class OllamaClient:
    """Client wrapper for Ollama API calls."""

    async def generate(self, prompt: str) -> dict[str, Any]:
        """Generate text from a prompt."""
        # TODO: implement HTTP call to Ollama service.
        _ = prompt
        return {"output": ""}
