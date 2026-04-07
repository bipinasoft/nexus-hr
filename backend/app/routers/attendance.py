from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from nexus_shared import Permission, Principal, get_current_principal, require_permissions

from ..core.contracts import CheckInRequest, LeaveApprovalRequest
from ..core.demo_data import demo_leave_requests
from ..db.models import AttendanceRecord, LeaveRequest
from ..db.session import get_db_session
from ..services.dashboard import get_employee_dashboard, invalidate_dashboard_cache
from ..services.notifications import create_notification

router = APIRouter(tags=["attendance", "leave"])


@router.get("/v1/attendance/monthly")
async def read_monthly_attendance(
    month: str | None = Query(default=None, pattern=r"^\d{4}-\d{2}$"),
    principal: Principal = Depends(get_current_principal),
    session: AsyncSession | None = Depends(get_db_session),
) -> dict[str, object]:
    dashboard = await get_employee_dashboard(
        org_id=principal.org_id,
        employee_id=principal.user_id,
        month=month,
        session=session,
    )
    return {
        "employee_id": dashboard.employee.employee_id,
        "month": dashboard.month,
        "summary": dashboard.summary.model_dump(mode="json"),
        "calendar": [item.model_dump(mode="json") for item in dashboard.calendar],
    }


@router.post("/v1/attendance/check-in")
async def check_in(
    payload: CheckInRequest,
    principal: Principal = Depends(require_permissions(Permission.ATTENDANCE_WRITE)),
    session: AsyncSession | None = Depends(get_db_session),
) -> dict[str, object]:
    geofence_passed = 12.90 <= payload.latitude <= 13.10 and 77.40 <= payload.longitude <= 77.75
    now = datetime.now(UTC)
    attendance_status = "present" if geofence_passed else "manual-review"

    if session is not None:
        existing = await session.scalar(
            select(AttendanceRecord).where(
                AttendanceRecord.org_id == principal.org_id,
                AttendanceRecord.employee_id == principal.user_id,
                AttendanceRecord.work_date == now.date(),
            )
        )
        if existing is None:
            session.add(
                AttendanceRecord(
                    id=f"att-{uuid4()}",
                    org_id=principal.org_id,
                    employee_id=principal.user_id,
                    work_date=now.date(),
                    status=attendance_status,
                    check_in_at=now,
                    check_out_at=None,
                    total_hours=None,
                    geofence_passed=geofence_passed,
                    location_label=payload.location_label or "Geo edge node",
                    notes="Real-time check-in captured.",
                )
            )
        else:
            existing.check_in_at = now
            existing.status = attendance_status
            existing.geofence_passed = geofence_passed
            existing.location_label = payload.location_label or existing.location_label
        await session.commit()

    await invalidate_dashboard_cache(principal.org_id, principal.user_id)
    await create_notification(
        org_id=principal.org_id,
        recipient_id=principal.user_id,
        title="Attendance check-in recorded",
        message=(
            "Your location passed geofence validation."
            if geofence_passed
            else "Your check-in needs manual review because the geofence was not matched."
        ),
        severity="low" if geofence_passed else "medium",
        tags=["attendance", "check-in"],
        action_url="/dashboard?focus=attendance",
        session=session,
    )

    return {
        "employee_id": principal.user_id,
        "source": payload.source,
        "geofence_passed": geofence_passed,
        "status": "recorded",
        "attendance_status": attendance_status,
    }


@router.get("/v1/leaves/mine")
async def list_my_leaves(
    principal: Principal = Depends(require_permissions(Permission.LEAVE_READ)),
    session: AsyncSession | None = Depends(get_db_session),
) -> dict[str, object]:
    if session is not None:
        items = (
            await session.scalars(
                select(LeaveRequest)
                .where(
                    LeaveRequest.org_id == principal.org_id,
                    LeaveRequest.employee_id == principal.user_id,
                )
                .order_by(LeaveRequest.start_date.desc())
            )
        ).all()
        return {
            "employee_id": principal.user_id,
            "items": [
                {
                    "request_id": item.id,
                    "leave_type": item.leave_type,
                    "start_date": item.start_date.isoformat(),
                    "end_date": item.end_date.isoformat(),
                    "status": item.status,
                    "reason": item.reason,
                }
                for item in items
            ],
        }

    month_start = datetime.now(UTC).date().replace(day=1)
    return {
        "employee_id": principal.user_id,
        "items": demo_leave_requests(principal.user_id, month_start),
    }


@router.post("/v1/leaves/{request_id}/approve")
async def approve_leave(
    request_id: str,
    payload: LeaveApprovalRequest,
    principal: Principal = Depends(require_permissions(Permission.LEAVE_APPROVE)),
    session: AsyncSession | None = Depends(get_db_session),
) -> dict[str, str]:
    employee_id = principal.user_id
    if session is not None:
        leave_request = await session.scalar(
            select(LeaveRequest).where(
                LeaveRequest.id == request_id,
                LeaveRequest.org_id == principal.org_id,
            )
        )
        if leave_request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Leave request not found.",
            )
        leave_request.status = "approved"
        employee_id = leave_request.employee_id
        await session.commit()

    await invalidate_dashboard_cache(principal.org_id, employee_id)
    await create_notification(
        org_id=principal.org_id,
        recipient_id=employee_id,
        title="Leave request approved",
        message=payload.comments or "Your leave request has been approved.",
        severity="low",
        tags=["leave", "approval"],
        action_url="/dashboard?focus=leave",
        session=session,
    )

    return {
        "request_id": request_id,
        "approved_by": principal.user_id,
        "status": "approved",
    }
