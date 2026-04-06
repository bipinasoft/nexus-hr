from fastapi import FastAPI

from nexus_shared import AuditMiddleware

from .routers import attendance, audit, auth, employee, payroll, performance, system

app = FastAPI(
    title="NexusHR Backend",
    version="0.1.0",
    summary="Unified FastAPI backend for auth, employee, attendance, payroll, performance, and audit domains.",
)
app.add_middleware(AuditMiddleware)

app.include_router(system.router)
app.include_router(auth.router)
app.include_router(employee.router)
app.include_router(attendance.router)
app.include_router(payroll.router)
app.include_router(performance.router)
app.include_router(audit.router)

