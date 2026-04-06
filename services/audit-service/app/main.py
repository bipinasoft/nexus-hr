from fastapi import Depends, FastAPI, Query

from nexus_shared import AuditMiddleware, Permission, Principal, require_permissions

app = FastAPI(
    title="NexusHR Audit Service",
    version="0.1.0",
    summary="Centralized audit retrieval and compliance search APIs.",
)
app.add_middleware(AuditMiddleware)


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "audit-service"}


@app.get("/v1/audit/events", tags=["audit"])
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

