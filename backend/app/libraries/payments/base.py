"""Base interfaces for payment providers."""

from __future__ import annotations

from typing import Protocol


class PaymentProvider(Protocol):
    """Protocol for payment provider implementations."""

    async def create_subscription(self, customer_id: str, plan_code: str) -> str:
        """Create a provider subscription and return external id."""
        ...
