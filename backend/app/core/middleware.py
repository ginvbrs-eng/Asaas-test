"""Application middlewares for request context and multi-tenancy."""

from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.tenant import extract_org_from_request, set_current_org


class TenantContextMiddleware(BaseHTTPMiddleware):
    """Inject organization id into context for each request."""

    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        org_id = await extract_org_from_request(request)
        set_current_org(org_id)
        response: Response = await call_next(request)
        return response
