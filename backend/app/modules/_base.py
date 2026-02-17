"""Shared patterns and contracts for business modules."""

from __future__ import annotations


class ModuleServiceError(Exception):
    """Domain-level exception for module services."""
