from fastapi import Depends, FastAPI
from pydantic import BaseModel

from nexus_shared import (
    AuditMiddleware,
    Permission,
    Principal,
    get_current_principal,
    require_permissions,
)

app = FastAPI(
    title="NexusHR Employee Lifecycle Service",
    version="0.1.0",
    summary="Employee lifecycle, onboarding, documents, and asset workflows.",
)
app.add_middleware(AuditMiddleware)


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


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "employee-service"}


@app.get("/v1/employees/me", response_model=EmployeeProfile, tags=["employees"])
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


@app.post("/v1/employees", response_model=EmployeeProfile, tags=["employees"])
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
