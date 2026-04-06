import logging
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pymongo import MongoClient
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from .config import get_settings
from .models import Principal

logger = logging.getLogger("nexushr.audit")
WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


class AuditSink:
    def __init__(self) -> None:
        self._client: MongoClient | None = None

    def _collection(self):
        settings = get_settings()
        if self._client is None:
            self._client = MongoClient(settings.mongodb_audit_uri, tz_aware=True)

        return self._client[settings.mongodb_audit_db][settings.mongodb_audit_collection]

    def write(self, event: dict[str, Any]) -> None:
        try:
            self._collection().insert_one(event)
        except Exception as exc:
            logger.warning("Failed to persist audit event: %s", exc)


audit_sink = AuditSink()


def extract_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    if request.client:
        return request.client.host

    return "unknown"


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        settings = get_settings()
        status_code = 500
        error_message: str | None = None

        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        except Exception as exc:
            error_message = str(exc)
            raise
        finally:
            if request.method.upper() in WRITE_METHODS:
                principal: Principal | None = getattr(request.state, "principal", None)
                route = request.scope.get("route")
                route_path = getattr(route, "path", request.url.path)

                audit_sink.write(
                    {
                        "event_id": str(uuid4()),
                        "timestamp": datetime.now(UTC).isoformat(),
                        "service": settings.service_name,
                        "method": request.method.upper(),
                        "path": request.url.path,
                        "route": route_path,
                        "query_string": request.url.query,
                        "user_id": principal.user_id if principal else "anonymous",
                        "roles": sorted(principal.roles) if principal else [],
                        "ip_address": extract_client_ip(request),
                        "status_code": status_code,
                        "request_id": request.headers.get("x-request-id", str(uuid4())),
                        "error_message": error_message,
                    }
                )
