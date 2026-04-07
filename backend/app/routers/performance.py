from fastapi import APIRouter, Depends
from pydantic import BaseModel

from nexus_shared import (
    Permission,
    Principal,
    get_current_principal,
    require_permissions,
)

router = APIRouter(prefix="/v1/performance", tags=["performance"])


class FeedbackRequest(BaseModel):
    cycle_id: str
    subject_employee_id: str
    feedback_type: str
    comments: str


@router.get("/objectives/me")
async def read_my_objectives(
    principal: Principal = Depends(get_current_principal),
) -> dict[str, object]:
    return {
        "employee_id": principal.user_id,
        "objectives": [
            {"title": "Reduce payroll query turnaround", "progress_percent": 72},
            {"title": "Close onboarding tasks within SLA", "progress_percent": 81},
            {"title": "Increase dashboard adoption across field teams", "progress_percent": 64},
        ],
        "review_sentiment": {
            "summary": "Positive trend with scope for coaching on workload balance.",
            "score": 0.78,
        },
    }


@router.post("/feedback")
async def submit_feedback(
    payload: FeedbackRequest,
    principal: Principal = Depends(
        require_permissions(Permission.PERFORMANCE_WRITE)
    ),
) -> dict[str, str]:
    return {
        "cycle_id": payload.cycle_id,
        "subject_employee_id": payload.subject_employee_id,
        "submitted_by": principal.user_id,
        "sentiment_pipeline_status": "indexed-and-queued",
    }
