from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class AuthMethod(StrEnum):
    PASSWORD = "password"
    SSO = "sso"
    OTP = "otp"


class LoginRequest(BaseModel):
    email: str
    password: str | None = None
    mfa_code: str | None = None
    company_domain: str | None = None
    provider: str | None = None
    method: AuthMethod = AuthMethod.PASSWORD


class AuthUser(BaseModel):
    user_id: str
    employee_id: str
    name: str
    email: str
    org_id: str
    tenant_slug: str
    department_id: str | None = None
    team_id: str | None = None
    roles: list[str]
    permissions: list[str]
    employment_status: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
    user: AuthUser
    available_routes: list[str]
    sso_launch_url: str | None = None


class AuthConfig(BaseModel):
    issuer: str
    audience: str
    supported_login_flows: list[str]
    mfa_required: bool
    sso_providers: list[str]
    default_workspace_hint: str


class EmployeeProfile(BaseModel):
    employee_id: str
    full_name: str
    work_email: str
    department_id: str
    position_id: str
    role: str
    employment_status: str
    manager_id: str | None = None


class AttendanceCalendarDay(BaseModel):
    date: date
    day_label: str
    attendance_status: str
    total_hours: float | None = None
    check_in_at: datetime | None = None
    check_out_at: datetime | None = None
    leave_type: str | None = None
    leave_status: str | None = None
    holiday_name: str | None = None
    is_weekend: bool = False
    geofence_passed: bool | None = None
    location_label: str | None = None
    notes: str | None = None


class LeaveBalanceCard(BaseModel):
    leave_type: str
    allocated_days: float
    used_days: float
    pending_days: float
    available_days: float


class AttendanceSummary(BaseModel):
    present_days: int
    remote_days: int
    leave_days: int
    holiday_days: int
    absent_days: int
    average_hours: float


class NotificationItem(BaseModel):
    notification_id: str
    title: str
    message: str
    severity: str
    tags: list[str] = Field(default_factory=list)
    action_url: str | None = None
    created_at: datetime
    is_read: bool = False


class EmployeeDashboard(BaseModel):
    month: str
    employee: EmployeeProfile
    summary: AttendanceSummary
    calendar: list[AttendanceCalendarDay]
    leave_balances: list[LeaveBalanceCard]
    alerts: list[NotificationItem]


class SSOStartRequest(BaseModel):
    company_domain: str
    provider: str = "Azure AD"


class NotificationAck(BaseModel):
    notification_id: str
    status: str


class CheckInRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    source: str = "mobile"
    location_label: str | None = None


class LeaveApprovalRequest(BaseModel):
    comments: str | None = None


class KnowledgeDocumentInput(BaseModel):
    title: str
    source: str
    content: str = Field(min_length=40)
    tags: list[str] = Field(default_factory=list)


class KnowledgeCitation(BaseModel):
    title: str
    source: str
    snippet: str


class KnowledgeIngestRequest(BaseModel):
    documents: list[KnowledgeDocumentInput]


class AssistantRequest(BaseModel):
    question: str
    top_k: int = Field(default=4, ge=1, le=10)
    include_actions: bool = True


class AssistantResponse(BaseModel):
    answer: str
    strategy: str
    intent: str
    citations: list[KnowledgeCitation]
    follow_up_actions: list[str] = Field(default_factory=list)
