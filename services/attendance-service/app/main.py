from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field

from nexus_shared import (
    AuditMiddleware,
    Permission,
    Principal,
    require_permissions,
)

app = FastAPI(
    title="NexusHR Attendance & Leave Service",
    version="0.1.0",
    summary="Attendance, geofencing, leave policies, and approval workflows.",
)
app.add_middleware(AuditMiddleware)


class CheckInRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    source: str = "mobile"


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "attendance-service"}


@app.post("/v1/attendance/check-in", tags=["attendance"])
async def check_in(
    payload: CheckInRequest,
    principal: Principal = Depends(require_permissions(Permission.ATTENDANCE_WRITE)),
) -> dict[str, object]:
    geofence_passed = 12.90 <= payload.latitude <= 13.10 and 77.40 <= payload.longitude <= 77.75

    return {
        "employee_id": principal.user_id,
        "source": payload.source,
        "geofence_passed": geofence_passed,
        "status": "recorded",
    }


@app.post("/v1/leaves/{request_id}/approve", tags=["leave"])
async def approve_leave(
    request_id: str,
    principal: Principal = Depends(require_permissions(Permission.LEAVE_APPROVE)),
) -> dict[str, str]:
    return {
        "request_id": request_id,
        "approved_by": principal.user_id,
        "status": "approved",
    }

