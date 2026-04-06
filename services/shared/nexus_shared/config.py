from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = "local"
    service_name: str = "nexus-service"
    oidc_issuer_url: str = "https://login.nexushr.example.com/realms/nexushr"
    oidc_jwks_url: str = (
        "https://login.nexushr.example.com/realms/nexushr/protocol/openid-connect/certs"
    )
    oidc_audience: str = "nexushr-api"
    oidc_algorithms: list[str] = Field(default_factory=lambda: ["RS256"])
    mongodb_audit_uri: str = "mongodb://localhost:27017"
    mongodb_audit_db: str = "nexushr_audit"
    mongodb_audit_collection: str = "events"

    model_config = SettingsConfigDict(
        env_prefix="NEXUSHR_",
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

