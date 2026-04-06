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

