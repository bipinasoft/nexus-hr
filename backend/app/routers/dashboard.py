from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.contracts import EmployeeDashboard
from ..db.session import get_db_session
from ..platform import Permission, Principal, get_current_principal, require_permissions
from ..services.dashboard import get_employee_dashboard

router = APIRouter(prefix="/v1/dashboard", tags=["dashboard"])


@router.get("/me", response_model=EmployeeDashboard)
async def read_my_dashboard(
    month: str | None = Query(default=None, pattern=r"^\d{4}-\d{2}$"),
    principal: Principal = Depends(require_permissions(Permission.DASHBOARD_READ)),
    session: AsyncSession | None = Depends(get_db_session),
) -> EmployeeDashboard:
    return await get_employee_dashboard(
        org_id=principal.org_id,
        employee_id=principal.user_id,
        month=month,
        session=session,
    )
