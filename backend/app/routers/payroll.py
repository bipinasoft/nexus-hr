from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from nexus_shared import Permission, Principal, require_permissions

router = APIRouter(prefix="/v1/payroll", tags=["payroll"])


class PayrollPreviewRequest(BaseModel):
    pay_period: str = Field(examples=["2026-04"])
    employee_ids: list[str]
    statutory_region: str = "IN"


@router.get("/summary/me")
async def read_my_payroll_summary(
    principal: Principal = Depends(require_permissions(Permission.PAYROLL_READ)),
) -> dict[str, object]:
    return {
        "employee_id": principal.user_id,
        "latest_payslip": {
            "pay_period": "2026-04",
            "gross_pay": 168000,
            "net_pay": 141200,
            "deductions": {
                "epf": 1800,
                "esi": 0,
                "tds": 21000,
            },
            "status": "published",
        },
    }


@router.post("/runs/preview")
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
