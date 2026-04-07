from __future__ import annotations

from calendar import monthrange
from datetime import UTC, date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.contracts import (
    AttendanceCalendarDay,
    AttendanceSummary,
    EmployeeDashboard,
    EmployeeProfile,
    LeaveBalanceCard,
    NotificationItem,
)
from ..core.demo_data import (
    demo_attendance_records,
    demo_holidays,
    demo_leave_requests,
    get_demo_employee,
    list_demo_notifications,
)
from ..db.models import AttendanceRecord, Employee, Holiday, LeaveBalance, LeaveRequest
from .cache import build_cache_key, cache_service
from .notifications import list_notifications


async def get_employee_dashboard(
    *,
    org_id: str,
    employee_id: str,
    month: str | None,
    session: AsyncSession | None,
) -> EmployeeDashboard:
    month_start = _month_start(month)
    cache_key = build_cache_key("dashboard", org_id, employee_id, month_start.isoformat())
    cached = await cache_service.get_json(cache_key)
    if cached is not None:
        return EmployeeDashboard.model_validate(cached)

    if session is not None:
        dashboard = await _build_database_dashboard(
            org_id=org_id,
            employee_id=employee_id,
            month_start=month_start,
            session=session,
        )
    else:
        dashboard = _build_demo_dashboard(
            org_id=org_id,
            employee_id=employee_id,
            month_start=month_start,
        )

    await cache_service.set_json(cache_key, dashboard.model_dump(mode="json"))
    return dashboard


async def invalidate_dashboard_cache(org_id: str, employee_id: str) -> None:
    await cache_service.delete_prefix(build_cache_key("dashboard", org_id, employee_id))


async def _build_database_dashboard(
    *,
    org_id: str,
    employee_id: str,
    month_start: date,
    session: AsyncSession,
) -> EmployeeDashboard:
    month_end = date(
        month_start.year, month_start.month, monthrange(month_start.year, month_start.month)[1]
    )
    employee = await session.scalar(
        select(Employee).where(Employee.id == employee_id, Employee.org_id == org_id)
    )
    if employee is None:
        return _build_demo_dashboard(org_id=org_id, employee_id=employee_id, month_start=month_start)

    attendance_rows = (
        await session.scalars(
            select(AttendanceRecord).where(
                AttendanceRecord.org_id == org_id,
                AttendanceRecord.employee_id == employee_id,
                AttendanceRecord.work_date >= month_start,
                AttendanceRecord.work_date <= month_end,
            )
        )
    ).all()
    leave_rows = (
        await session.scalars(
            select(LeaveRequest).where(
                LeaveRequest.org_id == org_id,
                LeaveRequest.employee_id == employee_id,
                LeaveRequest.start_date <= month_end,
                LeaveRequest.end_date >= month_start,
            )
        )
    ).all()
    holiday_rows = (
        await session.scalars(
            select(Holiday).where(
                Holiday.org_id == org_id,
                Holiday.holiday_date >= month_start,
                Holiday.holiday_date <= month_end,
            )
        )
    ).all()
    balance_rows = (
        await session.scalars(
            select(LeaveBalance).where(
                LeaveBalance.org_id == org_id,
                LeaveBalance.employee_id == employee_id,
            )
        )
    ).all()

    calendar = _build_calendar(
        month_start=month_start,
        attendance_rows=[
            {
                "work_date": row.work_date,
                "status": row.status,
                "total_hours": row.total_hours,
                "check_in_at": row.check_in_at,
                "check_out_at": row.check_out_at,
                "geofence_passed": row.geofence_passed,
                "location_label": row.location_label,
                "notes": row.notes,
            }
            for row in attendance_rows
        ],
        leave_rows=[
            {
                "leave_type": row.leave_type,
                "start_date": row.start_date,
                "end_date": row.end_date,
                "status": row.status,
                "reason": row.reason,
            }
            for row in leave_rows
        ],
        holiday_rows=[
            {
                "holiday_date": row.holiday_date,
                "name": row.name,
            }
            for row in holiday_rows
        ],
    )
    alerts = await list_notifications(
        org_id=org_id,
        recipient_id=employee_id,
        session=session,
    )
    balances = [
        LeaveBalanceCard(
            leave_type=row.leave_type,
            allocated_days=row.allocated_days,
            used_days=row.used_days,
            pending_days=row.pending_days,
            available_days=max(row.allocated_days - row.used_days - row.pending_days, 0),
        )
        for row in balance_rows
    ]
    return EmployeeDashboard(
        month=month_start.strftime("%Y-%m"),
        employee=EmployeeProfile(
            employee_id=employee.id,
            full_name=f"{employee.first_name} {employee.last_name}",
            work_email=employee.work_email,
            department_id=employee.department_id,
            position_id=employee.position_id,
            role=employee.role,
            employment_status=employee.employment_status,
            manager_id=employee.manager_id,
        ),
        summary=_summarize_calendar(calendar),
        calendar=calendar,
        leave_balances=balances,
        alerts=alerts,
    )


def _build_demo_dashboard(
    *,
    org_id: str,
    employee_id: str,
    month_start: date,
) -> EmployeeDashboard:
    demo_employee = get_demo_employee(employee_id) or get_demo_employee("emp-maya-rao")
    if demo_employee is None:
        raise ValueError("Demo employee dataset is unavailable.")
    attendance_rows = demo_attendance_records(demo_employee.employee_id, month_start)
    leave_rows = demo_leave_requests(demo_employee.employee_id, month_start)
    holiday_rows = demo_holidays(month_start)
    calendar = _build_calendar(
        month_start=month_start,
        attendance_rows=attendance_rows,
        leave_rows=leave_rows,
        holiday_rows=holiday_rows,
    )
    notifications = [
        NotificationItem.model_validate(item)
        for item in list_demo_notifications(demo_employee.employee_id)
    ]
    return EmployeeDashboard(
        month=month_start.strftime("%Y-%m"),
        employee=EmployeeProfile(
            employee_id=demo_employee.employee_id,
            full_name=demo_employee.full_name,
            work_email=demo_employee.work_email,
            department_id=demo_employee.department_id,
            position_id=demo_employee.position_id,
            role=demo_employee.role.value,
            employment_status=demo_employee.employment_status,
            manager_id=demo_employee.manager_id,
        ),
        summary=_summarize_calendar(calendar),
        calendar=calendar,
        leave_balances=[
            LeaveBalanceCard(
                leave_type="Annual Leave",
                allocated_days=18.0,
                used_days=3.0,
                pending_days=1.0,
                available_days=14.0,
            ),
            LeaveBalanceCard(
                leave_type="Sick Leave",
                allocated_days=12.0,
                used_days=1.0,
                pending_days=0.0,
                available_days=11.0,
            ),
        ],
        alerts=notifications,
    )


def _build_calendar(
    *,
    month_start: date,
    attendance_rows: list[dict[str, object]],
    leave_rows: list[dict[str, object]],
    holiday_rows: list[dict[str, object]],
) -> list[AttendanceCalendarDay]:
    today = datetime.now(UTC).date()
    attendance_by_day = {
        row["work_date"]: row
        for row in attendance_rows
    }
    holiday_by_day = {row["holiday_date"]: row for row in holiday_rows}
    leave_by_day: dict[date, dict[str, object]] = {}
    for row in leave_rows:
        current_day = row["start_date"]
        while current_day <= row["end_date"]:
            leave_by_day[current_day] = row
            current_day += timedelta(days=1)

    days: list[AttendanceCalendarDay] = []
    for day_number in range(1, monthrange(month_start.year, month_start.month)[1] + 1):
        day = date(month_start.year, month_start.month, day_number)
        is_weekend = day.weekday() >= 5
        holiday = holiday_by_day.get(day)
        leave = leave_by_day.get(day)
        attendance = attendance_by_day.get(day)
        status = "upcoming" if day > today else "not_marked"
        payload: dict[str, object] = {
            "date": day,
            "day_label": day.strftime("%a"),
            "attendance_status": status,
            "is_weekend": is_weekend,
        }

        if is_weekend:
            payload["attendance_status"] = "weekend"
            payload["notes"] = "Weekend"
        if holiday is not None:
            payload["attendance_status"] = "holiday"
            payload["holiday_name"] = holiday["name"]
            payload["notes"] = f"Holiday: {holiday['name']}"
        if leave is not None:
            payload["attendance_status"] = "leave"
            payload["leave_type"] = leave["leave_type"]
            payload["leave_status"] = leave["status"]
            payload["notes"] = leave["reason"]
        if attendance is not None:
            payload["attendance_status"] = attendance["status"]
            payload["total_hours"] = attendance["total_hours"]
            payload["check_in_at"] = attendance["check_in_at"]
            payload["check_out_at"] = attendance["check_out_at"]
            payload["geofence_passed"] = attendance["geofence_passed"]
            payload["location_label"] = attendance["location_label"]
            payload["notes"] = attendance["notes"]

        days.append(AttendanceCalendarDay.model_validate(payload))
    return days


def _summarize_calendar(calendar: list[AttendanceCalendarDay]) -> AttendanceSummary:
    present_days = sum(item.attendance_status == "present" for item in calendar)
    remote_days = sum(item.attendance_status == "remote" for item in calendar)
    leave_days = sum(item.attendance_status == "leave" for item in calendar)
    holiday_days = sum(item.attendance_status == "holiday" for item in calendar)
    absent_days = sum(item.attendance_status == "absent" for item in calendar)
    hours = [item.total_hours for item in calendar if item.total_hours]
    average_hours = round(sum(hours) / len(hours), 2) if hours else 0.0
    return AttendanceSummary(
        present_days=present_days,
        remote_days=remote_days,
        leave_days=leave_days,
        holiday_days=holiday_days,
        absent_days=absent_days,
        average_hours=average_hours,
    )


def _month_start(month: str | None) -> date:
    if month:
        return date.fromisoformat(f"{month}-01")
    today = datetime.now(UTC).date()
    return date(today.year, today.month, 1)
