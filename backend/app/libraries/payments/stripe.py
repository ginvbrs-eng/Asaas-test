"""Stripe payment provider implementation skeleton."""

from __future__ import annotations


class StripeProvider:
    """Stripe integration placeholder."""

    async def create_subscription(self, customer_id: str, plan_code: str) -> str:
        """Create Stripe subscription."""
        # TODO: call Stripe API and persist mapping.
        _ = (customer_id, plan_code)
        return ""
