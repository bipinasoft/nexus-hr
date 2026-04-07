from datetime import UTC, datetime, time
from uuid import uuid4

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from nexus_shared import (
    Permission,
    Principal,
    Role,
    get_current_principal,
    require_permissions,
)

from ..core.contracts import EmployeeProfile
from ..core.demo_data import DEMO_ORG_ID, get_demo_employee
from ..core.passwords import hash_password
from ..db.models import Employee
from ..db.session import get_db_session

router = APIRouter(prefix="/v1/employees", tags=["employees"])


class EmployeeCreateRequest(BaseModel):
    first_name: str
    last_name: str
    work_email: str
    department_id: str
    position_id: str
    team_id: str | None = None
    role: Role = Role.EMPLOYEE


@router.get("/me", response_model=EmployeeProfile)
async def read_my_profile(
    principal: Principal = Depends(get_current_principal),
    session: AsyncSession | None = Depends(get_db_session),
) -> EmployeeProfile:
    if session is not None:
        employee = await session.scalar(
            select(Employee).where(
                Employee.id == principal.user_id,
                Employee.org_id == principal.org_id,
            )
        )
        if employee is not None:
            return EmployeeProfile(
                employee_id=employee.id,
                full_name=f"{employee.first_name} {employee.last_name}",
                work_email=employee.work_email,
                department_id=employee.department_id,
                position_id=employee.position_id,
                role=employee.role,
                employment_status=employee.employment_status,
                manager_id=employee.manager_id,
            )

    demo_employee = get_demo_employee(principal.user_id) or get_demo_employee("emp-maya-rao")
    if demo_employee is None:
        raise RuntimeError("Demo employee profile is unavailable.")
    return EmployeeProfile(
        employee_id=demo_employee.employee_id,
        full_name=demo_employee.full_name,
        work_email=demo_employee.work_email,
        department_id=demo_employee.department_id,
        position_id=demo_employee.position_id,
        role=demo_employee.role.value,
        employment_status=demo_employee.employment_status,
        manager_id=demo_employee.manager_id,
    )


@router.post("", response_model=EmployeeProfile)
async def create_employee(
    payload: EmployeeCreateRequest,
    principal: Principal = Depends(require_permissions(Permission.EMPLOYEE_WRITE)),
    session: AsyncSession | None = Depends(get_db_session),
) -> EmployeeProfile:
    employee_id = f"emp-{uuid4()}"
    if session is not None:
        employee = Employee(
            id=employee_id,
            user_id=f"usr-{uuid4()}",
            org_id=principal.org_id or DEMO_ORG_ID,
            employee_code=f"NHR-{str(uuid4())[:6].upper()}",
            first_name=payload.first_name,
            last_name=payload.last_name,
            work_email=payload.work_email.lower(),
            role=payload.role.value,
            employment_status="provisioned",
            password_hash=hash_password("Welcome@123"),
            department_id=payload.department_id,
            position_id=payload.position_id,
            team_id=payload.team_id,
            manager_id=principal.user_id,
            hire_date=datetime.combine(datetime.now(UTC).date(), time(9, 0), tzinfo=UTC),
        )
        session.add(employee)
        await session.commit()
        await session.refresh(employee)
        return EmployeeProfile(
            employee_id=employee.id,
            full_name=f"{employee.first_name} {employee.last_name}",
            work_email=employee.work_email,
            department_id=employee.department_id,
            position_id=employee.position_id,
            role=employee.role,
            employment_status=employee.employment_status,
            manager_id=employee.manager_id,
        )

    return EmployeeProfile(
        employee_id=employee_id,
        full_name=f"{payload.first_name} {payload.last_name}",
        work_email=payload.work_email.lower(),
        department_id=payload.department_id,
        position_id=payload.position_id,
        role=payload.role.value,
        employment_status=f"provisioned by {principal.user_id}",
        manager_id=principal.user_id,
    )
