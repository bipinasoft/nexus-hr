from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from nexus_shared import Permission, Role, issue_local_access_token
from nexus_shared.config import get_settings
from nexus_shared.models import DEFAULT_ROLE_PERMISSIONS

from ..core.contracts import AuthConfig, AuthMethod, AuthUser, LoginRequest, LoginResponse
from ..core.demo_data import (
    DEMO_DOMAIN,
    DEMO_ORG_ID,
    DEMO_TENANT_SLUG,
    get_demo_employee_by_email,
)
from ..core.passwords import verify_password
from ..db.models import Employee, Organization


def build_auth_config() -> AuthConfig:
    settings = get_settings()
    return AuthConfig(
        issuer=settings.oidc_issuer_url,
        audience=settings.oidc_audience,
        supported_login_flows=["password+mfa", "enterprise-sso", "mobile-otp"],
        mfa_required=True,
        sso_providers=["Azure AD", "Okta", "Google Workspace", "Ping Identity"],
        default_workspace_hint=DEMO_DOMAIN,
    )


def build_sso_launch_url(company_domain: str, provider: str) -> str:
    settings = get_settings()
    normalized_domain = company_domain.strip().lower()
    normalized_provider = provider.strip().replace(" ", "+")
    return (
        f"{settings.oidc_issuer_url}/protocol/openid-connect/auth?"
        f"client_id={settings.oidc_audience}&tenant={normalized_domain}&idp_hint={normalized_provider}"
    )


async def login(
    payload: LoginRequest,
    session: AsyncSession | None,
) -> LoginResponse:
    settings = get_settings()
    if payload.method == AuthMethod.SSO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use the SSO start endpoint to initiate enterprise login.",
        )

    record = await _load_employee_by_email(payload.email, session)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unknown workspace account.",
        )

    role = Role(record["role"])
    if payload.method == AuthMethod.PASSWORD:
        if not payload.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is required for this login flow.",
            )
        password_hash = record.get("password_hash")
        password_is_valid = (
            verify_password(payload.password, password_hash)
            if password_hash
            else payload.password == settings.demo_password
        )
        if not password_is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials.",
            )

    if payload.method in {AuthMethod.PASSWORD, AuthMethod.OTP}:
        if payload.mfa_code != settings.demo_mfa_code:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid MFA challenge code.",
            )

    permissions = sorted(DEFAULT_ROLE_PERMISSIONS[role])
    access_token, expires_at = issue_local_access_token(
        subject=record["employee_id"],
        org_id=record["org_id"],
        tenant_slug=record["tenant_slug"],
        roles=[role],
        email=record["work_email"],
        name=record["full_name"],
        permissions=permissions,
        department_ids=[record["department_id"]],
        team_ids=[record["team_id"]] if record.get("team_id") else [],
        auth_provider="local-password"
        if payload.method == AuthMethod.PASSWORD
        else "local-otp",
        mfa_verified=True,
    )
    return LoginResponse(
        access_token=access_token,
        expires_at=expires_at,
        user=AuthUser(
            user_id=record["user_id"],
            employee_id=record["employee_id"],
            name=record["full_name"],
            email=record["work_email"],
            org_id=record["org_id"],
            tenant_slug=record["tenant_slug"],
            department_id=record["department_id"],
            team_id=record.get("team_id"),
            roles=[role.value],
            permissions=permissions,
            employment_status=record["employment_status"],
        ),
        available_routes=[
            "/dashboard",
            "/v1/dashboard/me",
            "/v1/notifications/me",
            "/v1/assistant/query",
        ],
        sso_launch_url=build_sso_launch_url(
            payload.company_domain or DEMO_DOMAIN,
            payload.provider or "Azure AD",
        ),
    )


def build_session_payload(principal_user_id: str, session_data: dict[str, Any]) -> dict[str, Any]:
    return {
        "principal_user_id": principal_user_id,
        "profile": session_data,
        "recommended_actions": [
            "Review monthly attendance anomalies",
            "Clear pending leave approvals",
            "Acknowledge high-priority notifications",
        ],
    }


async def _load_employee_by_email(
    email: str, session: AsyncSession | None
) -> dict[str, Any] | None:
    if session is not None:
        statement = (
            select(Employee, Organization)
            .join(Organization, Employee.org_id == Organization.id)
            .where(Employee.work_email == email.strip().lower())
        )
        result = await session.execute(statement)
        row = result.first()
        if row is not None:
            employee, organization = row
            return {
                "employee_id": employee.id,
                "user_id": employee.user_id,
                "org_id": employee.org_id,
                "tenant_slug": organization.slug,
                "full_name": f"{employee.first_name} {employee.last_name}",
                "work_email": employee.work_email,
                "department_id": employee.department_id,
                "team_id": employee.team_id,
                "role": employee.role,
                "employment_status": employee.employment_status,
                "password_hash": employee.password_hash,
            }

    demo_employee = get_demo_employee_by_email(email)
    if demo_employee is None:
        return None

    return {
        "employee_id": demo_employee.employee_id,
        "user_id": demo_employee.user_id,
        "org_id": DEMO_ORG_ID,
        "tenant_slug": DEMO_TENANT_SLUG,
        "full_name": demo_employee.full_name,
        "work_email": demo_employee.work_email,
        "department_id": demo_employee.department_id,
        "team_id": demo_employee.team_id,
        "role": demo_employee.role.value,
        "employment_status": demo_employee.employment_status,
        "password_hash": None,
    }


def security_rotation_response(requested_by: str) -> dict[str, str]:
    return {
        "status": "accepted",
        "message": "JWT secret and SSO metadata rotation queued.",
        "requested_by": requested_by,
        "compliance_scope": Permission.SECURITY_WRITE.value,
    }
