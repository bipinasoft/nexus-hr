from fastapi import APIRouter, Depends
from pydantic import BaseModel

from nexus_shared import (
    Permission,
    Principal,
    get_current_principal,
    require_permissions,
)

router = APIRouter(prefix="/v1/employees", tags=["employees"])


class EmployeeProfile(BaseModel):
    employee_id: str
    full_name: str
    department_id: str
    position_id: str
    employment_status: str


class EmployeeCreateRequest(BaseModel):
    first_name: str
    last_name: str
    work_email: str
    department_id: str
    position_id: str


@router.get("/me", response_model=EmployeeProfile)
async def read_my_profile(
    principal: Principal = Depends(get_current_principal),
) -> EmployeeProfile:
    return EmployeeProfile(
        employee_id=principal.user_id,
        full_name=principal.name or "NexusHR Employee",
        department_id=next(iter(principal.department_ids), "dept-core"),
        position_id="position-architect",
        employment_status="active",
    )


@router.post("", response_model=EmployeeProfile)
async def create_employee(
    payload: EmployeeCreateRequest,
    principal: Principal = Depends(require_permissions(Permission.EMPLOYEE_WRITE)),
) -> EmployeeProfile:
    return EmployeeProfile(
        employee_id="emp-sample-001",
        full_name=f"{payload.first_name} {payload.last_name}",
        department_id=payload.department_id,
        position_id=payload.position_id,
        employment_status=f"provisioned by {principal.user_id}",
    )

