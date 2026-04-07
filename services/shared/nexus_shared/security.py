import time
from datetime import UTC, datetime, timedelta
from typing import Any

import httpx
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from .config import get_settings
from .models import Principal, Role, TokenClaims


class JWKSCache:
    def __init__(self, ttl_seconds: int = 300) -> None:
        self.ttl_seconds = ttl_seconds
        self._keys: dict[str, dict[str, Any]] = {}
        self._fetched_at = 0.0

    async def refresh(self) -> None:
        settings = get_settings()

        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(settings.oidc_jwks_url)
            response.raise_for_status()
            payload = response.json()

        self._keys = {
            key["kid"]: key for key in payload.get("keys", []) if key.get("kid")
        }
        self._fetched_at = time.time()

    async def get_key(self, kid: str) -> dict[str, Any]:
        expired = (time.time() - self._fetched_at) >= self.ttl_seconds
        if expired or kid not in self._keys:
            await self.refresh()

        key = self._keys.get(kid)
        if not key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to resolve token signing key.",
            )

        return key


jwks_cache = JWKSCache()


class OIDCBearer(HTTPBearer):
    def __init__(self) -> None:
        super().__init__(auto_error=True)

    async def _verify_oidc_token(self, token: str) -> Principal:
        settings = get_settings()

        try:
            header = jwt.get_unverified_header(token)
            algorithm = header.get("alg")
            kid = header.get("kid")

            if algorithm not in settings.oidc_algorithms:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unsupported signing algorithm.",
                )

            if not kid:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token header is missing a key identifier.",
                )

            signing_key = await jwks_cache.get_key(kid)
            payload = jwt.decode(
                token,
                signing_key,
                algorithms=settings.oidc_algorithms,
                audience=settings.oidc_audience,
                issuer=settings.oidc_issuer_url,
                options={"verify_at_hash": False},
            )
            return Principal.from_claims(TokenClaims.model_validate(payload))
        except HTTPException:
            raise
        except JWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid or expired access token: {exc}",
            ) from exc

    def _verify_local_token(self, token: str) -> Principal:
        settings = get_settings()

        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
                audience=settings.oidc_audience,
                issuer=settings.jwt_issuer,
                options={"verify_at_hash": False},
            )
            return Principal.from_claims(TokenClaims.model_validate(payload))
        except JWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid or expired local access token: {exc}",
            ) from exc

    async def verify_token(self, token: str) -> Principal:
        settings = get_settings()

        try:
            header = jwt.get_unverified_header(token)
            claims = jwt.get_unverified_claims(token)
        except JWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Unable to read access token: {exc}",
            ) from exc

        token_issuer = claims.get("iss")
        algorithm = header.get("alg")
        local_algorithms = {settings.jwt_algorithm}

        if settings.auth_mode in {"local", "hybrid"} and (
            algorithm in local_algorithms or token_issuer == settings.jwt_issuer
        ):
            return self._verify_local_token(token)

        if settings.auth_mode == "local":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="External identity tokens are disabled for this environment.",
            )

        return await self._verify_oidc_token(token)

    async def __call__(self, request: Request) -> Principal:
        credentials = await super().__call__(request)
        if credentials is None or not isinstance(
            credentials, HTTPAuthorizationCredentials
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bearer token required.",
            )

        principal = await self.verify_token(credentials.credentials)
        request.state.principal = principal
        return principal


def issue_local_access_token(
    *,
    subject: str,
    org_id: str,
    tenant_slug: str,
    roles: list[Role],
    email: str | None = None,
    name: str | None = None,
    permissions: list[str] | None = None,
    department_ids: list[str] | None = None,
    team_ids: list[str] | None = None,
    auth_provider: str = "local-password",
    mfa_verified: bool = True,
) -> tuple[str, datetime]:
    settings = get_settings()
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.jwt_access_ttl_minutes)
    payload = {
        "sub": subject,
        "email": email,
        "name": name,
        "roles": [role.value for role in roles],
        "permissions": permissions or [],
        "org_id": org_id,
        "tenant_slug": tenant_slug,
        "department_ids": department_ids or [],
        "team_ids": team_ids or [],
        "auth_provider": auth_provider,
        "mfa_verified": mfa_verified,
        "exp": int(expires_at.timestamp()),
        "iss": settings.jwt_issuer,
        "aud": settings.oidc_audience,
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token, expires_at


async def resolve_principal_from_token(token: str) -> Principal:
    bearer = OIDCBearer()
    return await bearer.verify_token(token)
