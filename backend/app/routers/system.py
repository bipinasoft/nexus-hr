from fastapi import APIRouter

from nexus_shared.config import get_settings

router = APIRouter(tags=["system"])

DOMAIN_STATUS = [
    {"domain": "auth", "status": "ok"},
    {"domain": "employee", "status": "ok"},
    {"domain": "attendance", "status": "ok"},
    {"domain": "payroll", "status": "ok"},
    {"domain": "performance", "status": "ok"},
    {"domain": "audit", "status": "ok"},
]


@router.get("/health")
async def health() -> dict[str, str]:
    settings = get_settings()
    return {"status": "ok", "service": settings.service_name}


@router.get("/health/domains")
async def domain_health() -> dict[str, object]:
    return {"status": "ok", "domains": DOMAIN_STATUS}

