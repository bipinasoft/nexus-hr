from enum import StrEnum

from pydantic import BaseModel, Field


class Role(StrEnum):
    SUPER_ADMIN = "super_admin"
    HR_MANAGER = "hr_manager"
    MANAGER = "manager"
    EMPLOYEE = "employee"


class Permission(StrEnum):
    EMPLOYEE_READ = "employees.read"
    EMPLOYEE_WRITE = "employees.write"
    ATTENDANCE_READ = "attendance.read"
    ATTENDANCE_WRITE = "attendance.write"
    LEAVE_READ = "leave.read"
    LEAVE_WRITE = "leave.write"
    LEAVE_APPROVE = "leave.approve"
    PAYROLL_READ = "payroll.read"
    PAYROLL_WRITE = "payroll.write"
    PERFORMANCE_READ = "performance.read"
    PERFORMANCE_WRITE = "performance.write"
    AUDIT_READ = "audit.read"
    SECURITY_WRITE = "security.write"
    DASHBOARD_READ = "dashboard.read"
    NOTIFICATION_READ = "notifications.read"
    NOTIFICATION_WRITE = "notifications.write"
    ASSISTANT_USE = "assistant.use"
    DOCUMENT_READ = "documents.read"
    DOCUMENT_WRITE = "documents.write"


DEFAULT_ROLE_PERMISSIONS: dict[Role, set[str]] = {
    Role.SUPER_ADMIN: {"*"},
    Role.HR_MANAGER: {
        Permission.EMPLOYEE_READ,
        Permission.EMPLOYEE_WRITE,
        Permission.ATTENDANCE_READ,
        Permission.ATTENDANCE_WRITE,
        Permission.LEAVE_READ,
        Permission.LEAVE_WRITE,
        Permission.LEAVE_APPROVE,
        Permission.PAYROLL_READ,
        Permission.PERFORMANCE_READ,
        Permission.PERFORMANCE_WRITE,
        Permission.AUDIT_READ,
        Permission.DASHBOARD_READ,
        Permission.NOTIFICATION_READ,
        Permission.NOTIFICATION_WRITE,
        Permission.ASSISTANT_USE,
        Permission.DOCUMENT_READ,
        Permission.DOCUMENT_WRITE,
    },
    Role.MANAGER: {
        Permission.EMPLOYEE_READ,
        Permission.ATTENDANCE_READ,
        Permission.LEAVE_READ,
        Permission.LEAVE_APPROVE,
        Permission.PERFORMANCE_READ,
        Permission.PERFORMANCE_WRITE,
        Permission.DASHBOARD_READ,
        Permission.NOTIFICATION_READ,
        Permission.ASSISTANT_USE,
    },
    Role.EMPLOYEE: {
        Permission.EMPLOYEE_READ,
        Permission.ATTENDANCE_READ,
        Permission.ATTENDANCE_WRITE,
        Permission.LEAVE_READ,
        Permission.LEAVE_WRITE,
        Permission.PERFORMANCE_READ,
        Permission.DASHBOARD_READ,
        Permission.NOTIFICATION_READ,
        Permission.ASSISTANT_USE,
        Permission.DOCUMENT_READ,
    },
}


class TokenClaims(BaseModel):
    sub: str
    email: str | None = None
    name: str | None = None
    roles: list[Role] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)
    org_id: str
    tenant_slug: str
    department_ids: list[str] = Field(default_factory=list)
    team_ids: list[str] = Field(default_factory=list)
    auth_provider: str = "local-password"
    mfa_verified: bool = False
    exp: int
    iss: str
    aud: str | list[str]


class Principal(BaseModel):
    user_id: str
    email: str | None = None
    name: str | None = None
    org_id: str
    tenant_slug: str
    roles: set[Role] = Field(default_factory=set)
    permissions: set[str] = Field(default_factory=set)
    department_ids: set[str] = Field(default_factory=set)
    team_ids: set[str] = Field(default_factory=set)
    auth_provider: str = "local-password"
    mfa_verified: bool = False

    @classmethod
    def from_claims(cls, claims: TokenClaims) -> "Principal":
        merged_permissions = set(claims.permissions)
        for role in claims.roles:
            merged_permissions.update(DEFAULT_ROLE_PERMISSIONS.get(role, set()))

        return cls(
            user_id=claims.sub,
            email=claims.email,
            name=claims.name,
            org_id=claims.org_id,
            tenant_slug=claims.tenant_slug,
            roles=set(claims.roles),
            permissions=merged_permissions,
            department_ids=set(claims.department_ids),
            team_ids=set(claims.team_ids),
            auth_provider=claims.auth_provider,
            mfa_verified=claims.mfa_verified,
        )

    def has_role(self, role: Role) -> bool:
        return role in self.roles

    def has_permission(self, permission: str) -> bool:
        return "*" in self.permissions or permission in self.permissions

    def is_in_org(self, org_id: str) -> bool:
        return self.org_id == org_id or self.has_role(Role.SUPER_ADMIN)
