from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field

from nexus_shared import AuditMiddleware, Permission, Principal, require_permissions

app = FastAPI(
    title="NexusHR Payroll & Compliance Service",
    version="0.1.0",
    summary="Payroll processing, tax engines, payslips, and statutory reporting.",
)
app.add_middleware(AuditMiddleware)


class PayrollPreviewRequest(BaseModel):
    pay_period: str = Field(examples=["2026-04"])
    employee_ids: list[str]
    statutory_region: str = "IN"


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "payroll-service"}


@app.post("/v1/payroll/runs/preview", tags=["payroll"])
async def preview_payroll_run(
    payload: PayrollPreviewRequest,
    principal: Principal = Depends(require_permissions(Permission.PAYROLL_WRITE)),
) -> dict[str, object]:
    return {
        "pay_period": payload.pay_period,
        "employee_count": len(payload.employee_ids),
        "statutory_region": payload.statutory_region,
        "components": [
            "base_salary",
            "allowances",
            "epf",
            "esi",
            "tds",
        ],
        "generated_by": principal.user_id,
    }

