from fastapi import APIRouter

from nexus_shared.config import get_settings

from ..db.session import database_manager
from ..services.cache import cache_service

router = APIRouter(tags=["system"])


@router.get("/health")
async def health() -> dict[str, object]:
    settings = get_settings()
    return {
        "status": "ok",
        "service": settings.service_name,
        "database": "ok" if database_manager.available else "degraded",
        "cache": "ok" if cache_service.available else "degraded",
    }


@router.get("/health/domains")
async def domain_health() -> dict[str, object]:
    return {
        "status": "ok",
        "domains": [
            {"domain": "auth", "status": "ok"},
            {"domain": "employee", "status": "ok"},
            {"domain": "attendance", "status": "ok"},
            {"domain": "payroll", "status": "ok"},
            {"domain": "performance", "status": "ok"},
            {"domain": "notifications", "status": "ok"},
            {"domain": "assistant", "status": "ok"},
            {"domain": "audit", "status": "ok"},
        ],
        "platform": {
            "database_available": database_manager.available,
            "database_error": database_manager.startup_error,
            "cache_available": cache_service.available,
        },
    }
