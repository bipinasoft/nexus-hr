from fastapi import Depends, FastAPI
from pydantic import BaseModel

from nexus_shared import (
    AuditMiddleware,
    Permission,
    Principal,
    get_current_principal,
    require_permissions,
)
from nexus_shared.config import get_settings

app = FastAPI(
    title="NexusHR Auth Service",
    version="0.1.0",
    summary="Identity broker and security configuration service.",
)
app.add_middleware(AuditMiddleware)


class AuthConfig(BaseModel):
    issuer: str
    audience: str
    supported_login_flows: list[str]
    mfa_required: bool


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    settings = get_settings()
    return {"status": "ok", "service": settings.service_name}


@app.get("/v1/auth/config", response_model=AuthConfig, tags=["auth"])
async def read_auth_config() -> AuthConfig:
    settings = get_settings()
    return AuthConfig(
        issuer=settings.oidc_issuer_url,
        audience=settings.oidc_audience,
        supported_login_flows=["password+mfa", "enterprise-sso", "mobile-otp"],
        mfa_required=True,
    )


@app.get("/v1/auth/me", tags=["auth"])
async def read_current_session(
    principal: Principal = Depends(get_current_principal),
) -> dict[str, object]:
    return {
        "user_id": principal.user_id,
        "email": principal.email,
        "roles": sorted(principal.roles),
        "permissions": sorted(principal.permissions),
    }


@app.post("/v1/auth/admin/policies/rotate", tags=["auth"])
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

