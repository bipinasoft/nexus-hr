from fastapi import APIRouter, Depends, Query

from nexus_shared import Permission, Principal, require_permissions

router = APIRouter(prefix="/v1/audit", tags=["audit"])


@router.get("/events")
async def list_audit_events(
    limit: int = Query(default=20, ge=1, le=100),
    principal: Principal = Depends(require_permissions(Permission.AUDIT_READ)),
) -> dict[str, object]:
    return {
        "requested_by": principal.user_id,
        "items": [
            {
                "event_id": "audit-sample-001",
                "service": "employee-service",
                "method": "POST",
                "path": "/v1/employees",
                "status_code": 201,
            }
        ],
        "limit": limit,
    }

