from fastapi import APIRouter, Depends
from pydantic import BaseModel

from nexus_shared import (
    Permission,
    Principal,
    get_current_principal,
    require_permissions,
)
from nexus_shared.config import get_settings

router = APIRouter(prefix="/v1/auth", tags=["auth"])


class AuthConfig(BaseModel):
    issuer: str
    audience: str
    supported_login_flows: list[str]
    mfa_required: bool


@router.get("/config", response_model=AuthConfig)
async def read_auth_config() -> AuthConfig:
    settings = get_settings()
    return AuthConfig(
        issuer=settings.oidc_issuer_url,
        audience=settings.oidc_audience,
        supported_login_flows=["password+mfa", "enterprise-sso", "mobile-otp"],
        mfa_required=True,
    )


@router.get("/me")
async def read_current_session(
    principal: Principal = Depends(get_current_principal),
) -> dict[str, object]:
    return {
        "user_id": principal.user_id,
        "email": principal.email,
        "roles": sorted(principal.roles),
        "permissions": sorted(principal.permissions),
    }


@router.post("/admin/policies/rotate")
async def rotate_policy_keys(
    principal: Principal = Depends(
        require_permissions(Permission.SECURITY_WRITE)
    ),
) -> dict[str, str]:
    return {
        "status": "accepted",
        "message": "Security policy rotation queued.",
        "requested_by": principal.user_id,
    }

