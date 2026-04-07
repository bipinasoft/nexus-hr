from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from .models import Principal, Role
from .security import OIDCBearer

oidc_bearer = OIDCBearer()


async def get_current_principal(
    principal: Principal = Depends(oidc_bearer),
) -> Principal:
    return principal


def require_permissions(*permissions: str) -> Callable[..., Principal]:
    async def dependency(
        principal: Principal = Depends(get_current_principal),
    ) -> Principal:
        missing = [
            permission
            for permission in permissions
            if not principal.has_permission(permission)
        ]

        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permissions: {', '.join(missing)}",
            )

        return principal

    return dependency


def require_roles(*roles: Role) -> Callable[..., Principal]:
    async def dependency(
        principal: Principal = Depends(get_current_principal),
    ) -> Principal:
        if any(principal.has_role(role) for role in roles):
            return principal

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Role restriction violation.",
        )

    return dependency


def enforce_org_scope(org_id: str, principal: Principal) -> None:
    if principal.is_in_org(org_id):
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Tenant scope violation.",
    )


def enforce_department_scope(department_id: str, principal: Principal) -> None:
    if principal.has_role(Role.SUPER_ADMIN) or department_id in principal.department_ids:
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Department scope violation.",
    )


def enforce_team_scope(team_id: str, principal: Principal) -> None:
    if principal.has_role(Role.SUPER_ADMIN) or team_id in principal.team_ids:
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Team scope violation.",
    )
