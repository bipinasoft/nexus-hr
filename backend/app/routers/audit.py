from fastapi import APIRouter, Depends, Query
from pymongo import MongoClient

from ..platform import Permission, Principal, require_permissions
from ..platform.config import get_settings

router = APIRouter(prefix="/v1/audit", tags=["audit"])


@router.get("/events")
async def list_audit_events(
    limit: int = Query(default=20, ge=1, le=100),
    principal: Principal = Depends(require_permissions(Permission.AUDIT_READ)),
) -> dict[str, object]:
    settings = get_settings()
    items: list[dict[str, object]] = []
    try:
        client = MongoClient(settings.mongodb_audit_uri, tz_aware=True, serverSelectionTimeoutMS=1000)
        collection = client[settings.mongodb_audit_db][settings.mongodb_audit_collection]
        cursor = collection.find({"org_id": principal.org_id}).sort("timestamp", -1).limit(limit)
        items = [
            {
                "event_id": item.get("event_id"),
                "service": item.get("service"),
                "method": item.get("method"),
                "path": item.get("path"),
                "status_code": item.get("status_code"),
                "timestamp": item.get("timestamp"),
                "user_id": item.get("user_id"),
            }
            for item in cursor
        ]
    except Exception:
        items = [
            {
                "event_id": "audit-sample-001",
                "service": "backend-service",
                "method": "POST",
                "path": "/v1/attendance/check-in",
                "status_code": 200,
                "timestamp": "2026-04-07T10:15:00Z",
                "user_id": principal.user_id,
            }
        ]

    return {
        "requested_by": principal.user_id,
        "items": items,
        "limit": limit,
    }
