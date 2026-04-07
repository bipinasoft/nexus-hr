from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from nexus_shared import AuditMiddleware
from nexus_shared.config import get_settings

from .db.session import database_manager
from .routers import (
    assistant,
    attendance,
    audit,
    auth,
    dashboard,
    employee,
    notifications,
    payroll,
    performance,
    system,
)
from .services.cache import cache_service
from .services.vector_store import seed_memory_vector_store


@asynccontextmanager
async def lifespan(_: FastAPI):
    await cache_service.initialize()
    await database_manager.initialize()
    await seed_memory_vector_store()
    yield
    await cache_service.close()
    await database_manager.dispose()

app = FastAPI(
    title="NexusHR Backend",
    version="0.1.0",
    summary="Unified FastAPI backend for auth, dashboard, attendance, payroll, performance, audit, notifications, and LangGraph-powered HR assistance.",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuditMiddleware)

app.include_router(system.router)
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(employee.router)
app.include_router(attendance.router)
app.include_router(notifications.router)
app.include_router(assistant.router)
app.include_router(payroll.router)
app.include_router(performance.router)
app.include_router(audit.router)
