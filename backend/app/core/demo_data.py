from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from typing import Any
from uuid import uuid4

from ..platform import Role

DEMO_ORG_ID = "org-nexus-demo"
DEMO_TENANT_SLUG = "nexushr-demo"
DEMO_DOMAIN = "nexushr.example"


@dataclass(frozen=True)
class DemoEmployee:
    employee_id: str
    user_id: str
    employee_code: str
    first_name: str
    last_name: str
    work_email: str
    department_id: str
    position_id: str
    team_id: str
    role: Role
    employment_status: str
    hire_date: date
    manager_id: str | None = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


DEMO_DEPARTMENTS = [
    {"id": "dept-people", "name": "People Operations", "code": "HR"},
    {"id": "dept-platform", "name": "Platform Engineering", "code": "ENG"},
]

DEMO_POSITIONS = [
    {"id": "pos-hr-manager", "title": "HR Manager", "level": "L4"},
    {"id": "pos-team-manager", "title": "Engineering Manager", "level": "L5"},
    {"id": "pos-architect", "title": "Senior Full-Stack Architect", "level": "L5"},
    {"id": "pos-admin", "title": "Platform Super Admin", "level": "L6"},
]

DEMO_EMPLOYEES = [
    DemoEmployee(
        employee_id="emp-priya-shah",
        user_id="usr-priya-shah",
        employee_code="NHR-101",
        first_name="Priya",
        last_name="Shah",
        work_email="priya.shah@nexushr.example",
        department_id="dept-people",
        position_id="pos-hr-manager",
        team_id="team-hr",
        role=Role.HR_MANAGER,
        employment_status="active",
        hire_date=date(2023, 5, 8),
    ),
    DemoEmployee(
        employee_id="emp-arjun-sen",
        user_id="usr-arjun-sen",
        employee_code="NHR-102",
        first_name="Arjun",
        last_name="Sen",
        work_email="arjun.sen@nexushr.example",
        department_id="dept-platform",
        position_id="pos-team-manager",
        team_id="team-product-platform",
        role=Role.MANAGER,
        employment_status="active",
        hire_date=date(2022, 9, 1),
    ),
    DemoEmployee(
        employee_id="emp-maya-rao",
        user_id="usr-maya-rao",
        employee_code="NHR-103",
        first_name="Maya",
        last_name="Rao",
        work_email="maya.rao@nexushr.example",
        department_id="dept-platform",
        position_id="pos-architect",
        team_id="team-product-platform",
        role=Role.EMPLOYEE,
        employment_status="active",
        hire_date=date(2024, 1, 15),
        manager_id="emp-arjun-sen",
    ),
    DemoEmployee(
        employee_id="emp-aisha-khan",
        user_id="usr-aisha-khan",
        employee_code="NHR-104",
        first_name="Aisha",
        last_name="Khan",
        work_email="aisha.khan@nexushr.example",
        department_id="dept-people",
        position_id="pos-admin",
        team_id="team-admin",
        role=Role.SUPER_ADMIN,
        employment_status="active",
        hire_date=date(2021, 11, 5),
    ),
]

DEMO_LEAVE_BALANCES = [
    {
        "employee_id": "emp-maya-rao",
        "leave_type": "Annual Leave",
        "allocated_days": 18.0,
        "used_days": 3.0,
        "pending_days": 1.0,
    },
    {
        "employee_id": "emp-maya-rao",
        "leave_type": "Sick Leave",
        "allocated_days": 12.0,
        "used_days": 1.0,
        "pending_days": 0.0,
    },
]

DEMO_POLICY_DOCUMENTS = [
    {
        "title": "Attendance Policy 2026",
        "source": "policy://attendance/2026",
        "tags": ["attendance", "geofence", "leave"],
        "content": """
NexusHR employees can check in through web or mobile. Geofenced attendance is required for office workdays,
while approved remote work records a remote-present status. Managers review anomalies within one business day.
Late arrivals above fifteen minutes trigger an alert but do not block payroll.
""",
    },
    {
        "title": "Leave Governance Playbook",
        "source": "policy://leave/governance",
        "tags": ["leave", "approval", "hr"],
        "content": """
Annual leave accrues monthly. Requests up to two days route to the reporting manager.
Requests above two days escalate to the department HR manager for second-level approval.
Company holidays supersede planned leave and should not reduce the employee balance.
""",
    },
    {
        "title": "Payroll Compliance Notes",
        "source": "policy://payroll/india-compliance",
        "tags": ["payroll", "epf", "esi", "tds"],
        "content": """
Monthly payroll processing includes base salary, allowances, EPF, ESI, TDS, and local reimbursements.
Payroll cut-off is the twenty-fifth of each month, and statutory reports are generated after pay run approval.
Payslips are published to the employee self-service portal with immutable audit logging.
""",
    },
]


def get_demo_employee(employee_id: str) -> DemoEmployee | None:
    return next((item for item in DEMO_EMPLOYEES if item.employee_id == employee_id), None)


def get_demo_employee_by_email(email: str) -> DemoEmployee | None:
    lowered = email.strip().lower()
    return next((item for item in DEMO_EMPLOYEES if item.work_email == lowered), None)


def current_month(month: str | None = None) -> date:
    if month:
        return date.fromisoformat(f"{month}-01")
    today = date.today()
    return date(today.year, today.month, 1)


def demo_holidays(month_start: date) -> list[dict[str, Any]]:
    return [
        {
            "id": "holiday-founders-day",
            "holiday_date": date(month_start.year, month_start.month, min(14, 28)),
            "name": "Founders' Day",
            "kind": "company",
        },
        {
            "id": "holiday-wellness-friday",
            "holiday_date": date(month_start.year, month_start.month, min(25, 28)),
            "name": "Wellness Friday",
            "kind": "optional",
        },
    ]


def demo_leave_requests(employee_id: str, month_start: date) -> list[dict[str, Any]]:
    return [
        {
            "id": "leave-approved-planning",
            "employee_id": employee_id,
            "approver_id": "emp-arjun-sen",
            "leave_type": "Annual Leave",
            "start_date": date(month_start.year, month_start.month, min(8, 28)),
            "end_date": date(month_start.year, month_start.month, min(9, 28)),
            "status": "approved",
            "reason": "Family travel",
        },
        {
            "id": "leave-pending-wellbeing",
            "employee_id": employee_id,
            "approver_id": "emp-priya-shah",
            "leave_type": "Wellbeing Day",
            "start_date": date(month_start.year, month_start.month, min(22, 28)),
            "end_date": date(month_start.year, month_start.month, min(22, 28)),
            "status": "pending",
            "reason": "Recharge day",
        },
    ]


def demo_attendance_records(employee_id: str, month_start: date) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    holidays = {item["holiday_date"] for item in demo_holidays(month_start)}
    leave_days = set()
    for leave_request in demo_leave_requests(employee_id, month_start):
        current_day = leave_request["start_date"]
        while current_day <= leave_request["end_date"]:
            leave_days.add(current_day)
            current_day += timedelta(days=1)

    for offset in range(31):
        work_day = month_start + timedelta(days=offset)
        if work_day.month != month_start.month:
            break
        if work_day.weekday() >= 5 or work_day in holidays or work_day in leave_days:
            continue

        status = "present"
        location_label = "HQ Bengaluru"
        geofence_passed = True
        check_in_hour = 9
        if work_day.day in {3, 17}:
            status = "remote"
            location_label = "Remote workspace"
        if work_day.day in {11, 27}:
            status = "late"
            check_in_hour = 10
        if work_day.day in {19}:
            status = "absent"
            location_label = "No check-in"
            geofence_passed = False

        if status == "absent":
            records.append(
                {
                    "id": f"att-{work_day.isoformat()}",
                    "employee_id": employee_id,
                    "work_date": work_day,
                    "status": status,
                    "check_in_at": None,
                    "check_out_at": None,
                    "total_hours": 0.0,
                    "geofence_passed": geofence_passed,
                    "location_label": location_label,
                    "notes": "Missed mark-in. Manager follow-up required.",
                }
            )
            continue

        check_in_at = datetime.combine(
            work_day, time(check_in_hour, 7), tzinfo=UTC
        )
        check_out_at = datetime.combine(work_day, time(18, 11), tzinfo=UTC)
        records.append(
            {
                "id": f"att-{work_day.isoformat()}",
                "employee_id": employee_id,
                "work_date": work_day,
                "status": status,
                "check_in_at": check_in_at,
                "check_out_at": check_out_at,
                "total_hours": round(
                    (check_out_at - check_in_at).total_seconds() / 3600, 2
                ),
                "geofence_passed": geofence_passed,
                "location_label": location_label,
                "notes": "Auto-synced from attendance edge node.",
            }
        )
    return records


def initial_notifications() -> list[dict[str, Any]]:
    now = datetime.now(UTC)
    return [
        {
            "notification_id": "notif-leave-review",
            "recipient_id": "emp-maya-rao",
            "title": "Leave request requires your review",
            "message": "Your wellbeing day request is still pending with People Ops.",
            "severity": "medium",
            "tags": ["leave", "approval"],
            "action_url": "/dashboard?focus=leave",
            "created_at": now - timedelta(hours=2),
            "is_read": False,
        },
        {
            "notification_id": "notif-attendance-anomaly",
            "recipient_id": "emp-maya-rao",
            "title": "Attendance anomaly detected",
            "message": "March 19 missed check-in needs a quick explanation before payroll cut-off.",
            "severity": "high",
            "tags": ["attendance", "action-required"],
            "action_url": "/dashboard?focus=attendance",
            "created_at": now - timedelta(hours=6),
            "is_read": False,
        },
        {
            "notification_id": "notif-payslip-ready",
            "recipient_id": "emp-maya-rao",
            "title": "Payslip ready for download",
            "message": "Your latest payslip has been published to self-service with full audit capture.",
            "severity": "low",
            "tags": ["payroll", "documents"],
            "action_url": "/dashboard?focus=payslips",
            "created_at": now - timedelta(days=1),
            "is_read": True,
        },
    ]


_demo_notifications = initial_notifications()


def list_demo_notifications(recipient_id: str) -> list[dict[str, Any]]:
    return deepcopy(
        [
            item
            for item in _demo_notifications
            if item["recipient_id"] == recipient_id
        ]
    )


def append_demo_notification(
    recipient_id: str,
    title: str,
    message: str,
    severity: str,
    tags: list[str],
    action_url: str | None = None,
) -> dict[str, Any]:
    record = {
        "notification_id": f"notif-{uuid4()}",
        "recipient_id": recipient_id,
        "title": title,
        "message": message,
        "severity": severity,
        "tags": tags,
        "action_url": action_url,
        "created_at": datetime.now(UTC),
        "is_read": False,
    }
    _demo_notifications.insert(0, record)
    return deepcopy(record)


def mark_demo_notification_read(notification_id: str, recipient_id: str) -> bool:
    for item in _demo_notifications:
        if (
            item["notification_id"] == notification_id
            and item["recipient_id"] == recipient_id
        ):
            item["is_read"] = True
            return True
    return False
