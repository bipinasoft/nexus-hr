from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from nexus_shared import Permission, Principal, require_permissions

router = APIRouter(tags=["attendance", "leave"])


class CheckInRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    source: str = "mobile"


@router.post("/v1/attendance/check-in")
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


@router.post("/v1/leaves/{request_id}/approve")
async def approve_leave(
    request_id: str,
    principal: Principal = Depends(require_permissions(Permission.LEAVE_APPROVE)),
) -> dict[str, str]:
    return {
        "request_id": request_id,
        "approved_by": principal.user_id,
        "status": "approved",
    }

