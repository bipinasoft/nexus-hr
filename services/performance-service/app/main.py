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
    title="NexusHR Performance Service",
    version="0.1.0",
    summary="OKR tracking, feedback cycles, and AI-assisted performance insight workflows.",
)
app.add_middleware(AuditMiddleware)


class FeedbackRequest(BaseModel):
    cycle_id: str
    subject_employee_id: str
    feedback_type: str
    comments: str


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "performance-service"}


@app.get("/v1/performance/objectives/me", tags=["performance"])
async def read_my_objectives(
    principal: Principal = Depends(get_current_principal),
) -> dict[str, object]:
    return {
        "employee_id": principal.user_id,
        "objectives": [
            {"title": "Reduce payroll query turnaround", "progress_percent": 72},
            {"title": "Close onboarding tasks within SLA", "progress_percent": 81},
        ],
    }


@app.post("/v1/performance/feedback", tags=["performance"])
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
        "sentiment_pipeline_status": "queued",
    }

