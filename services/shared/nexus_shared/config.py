from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = "local"
    service_name: str = "nexus-service"
    auth_mode: str = "hybrid"
    oidc_issuer_url: str = "https://login.nexushr.example.com/realms/nexushr"
    oidc_jwks_url: str = (
        "https://login.nexushr.example.com/realms/nexushr/protocol/openid-connect/certs"
    )
    oidc_audience: str = "nexushr-api"
    oidc_algorithms: list[str] = Field(default_factory=lambda: ["RS256"])
    jwt_secret: str = "change-me-for-production"
    jwt_algorithm: str = "HS256"
    jwt_issuer: str = "https://api.nexushr.local/auth"
    jwt_access_ttl_minutes: int = 60
    demo_password: str = "NexusHR!2026"
    demo_mfa_code: str = "246810"
    platform_domain: str = "nexushr.local"
    tenant_header_name: str = "x-nexushr-org"
    database_url: str = "postgresql+asyncpg://nexushr:nexushr@localhost:5433/nexushr"
    database_echo: bool = False
    bootstrap_database: bool = True
    seed_demo_data: bool = True
    redis_url: str = "redis://localhost:6380/0"
    cache_ttl_seconds: int = 300
    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    )
    mongodb_audit_uri: str = "mongodb://localhost:27017"
    mongodb_audit_db: str = "nexushr_audit"
    mongodb_audit_collection: str = "events"
    vector_dimensions: int = 256
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    local_llm_base_url: str = "http://localhost:11434/v1"
    local_llm_model: str = "llama3.1"
    enable_local_llm_fallback: bool = True
    websocket_ping_interval_seconds: int = 30

    model_config = SettingsConfigDict(
        env_prefix="NEXUSHR_",
        env_file=".env",
        extra="ignore",
    )

    @field_validator("oidc_algorithms", "cors_origins", mode="before")
    @classmethod
    def parse_csv(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
