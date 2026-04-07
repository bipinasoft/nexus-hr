from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.contracts import LoginRequest, LoginResponse, SSOStartRequest
from ..db.session import get_db_session
from ..platform import (
    Permission,
    Principal,
    get_current_principal,
    require_permissions,
)
from ..services.auth import (
    build_auth_config,
    build_session_payload,
    build_sso_launch_url,
    login,
    security_rotation_response,
)

router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.get("/config")
async def read_auth_config() -> dict[str, object]:
    return build_auth_config().model_dump(mode="json")


@router.post("/login", response_model=LoginResponse)
async def login_user(
    payload: LoginRequest,
    session: AsyncSession | None = Depends(get_db_session),
) -> LoginResponse:
    return await login(payload, session)


@router.post("/sso/start")
async def start_sso(payload: SSOStartRequest) -> dict[str, str]:
    return {
        "authorization_url": build_sso_launch_url(
            company_domain=payload.company_domain,
            provider=payload.provider,
        )
    }


@router.get("/me")
async def read_current_session(
    principal: Principal = Depends(get_current_principal),
) -> dict[str, object]:
    return build_session_payload(
        principal.user_id,
        {
            "user_id": principal.user_id,
            "email": principal.email,
            "name": principal.name,
            "org_id": principal.org_id,
            "tenant_slug": principal.tenant_slug,
            "roles": sorted(role.value for role in principal.roles),
            "permissions": sorted(principal.permissions),
            "auth_provider": principal.auth_provider,
            "mfa_verified": principal.mfa_verified,
        },
    )


@router.post("/admin/policies/rotate")
async def rotate_policy_keys(
    principal: Principal = Depends(
        require_permissions(Permission.SECURITY_WRITE)
    ),
) -> dict[str, str]:
    return security_rotation_response(principal.user_id)
