from __future__ import annotations

import json
import logging
import time
from collections.abc import Iterable
from typing import Any

from redis.asyncio import Redis

from ..platform.config import get_settings

logger = logging.getLogger("nexushr.cache")


class CacheService:
    def __init__(self) -> None:
        self._client: Redis | None = None
        self._memory_cache: dict[str, tuple[str, float | None]] = {}
        self.available = False

    async def initialize(self) -> None:
        settings = get_settings()
        try:
            self._client = Redis.from_url(settings.redis_url, decode_responses=True)
            await self._client.ping()
            self.available = True
        except Exception as exc:
            logger.warning(
                "Redis unavailable, falling back to in-memory cache: %s", exc
            )
            self._client = None
            self.available = False

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()

    async def get_json(self, key: str) -> Any | None:
        if self._client is not None:
            payload = await self._client.get(key)
            return json.loads(payload) if payload else None

        payload = self._memory_cache.get(key)
        if payload is None:
            return None
        raw_value, expires_at = payload
        if expires_at is not None and expires_at < time.time():
            self._memory_cache.pop(key, None)
            return None
        return json.loads(raw_value)

    async def set_json(
        self, key: str, value: Any, ttl_seconds: int | None = None
    ) -> None:
        settings = get_settings()
        ttl = ttl_seconds or settings.cache_ttl_seconds
        payload = json.dumps(value, default=str)

        if self._client is not None:
            await self._client.set(key, payload, ex=ttl)
            return

        expires_at = time.time() + ttl if ttl else None
        self._memory_cache[key] = (payload, expires_at)

    async def delete_prefix(self, prefix: str) -> None:
        if self._client is not None:
            cursor = 0
            pattern = f"{prefix}*"
            while True:
                cursor, keys = await self._client.scan(cursor=cursor, match=pattern)
                if keys:
                    await self._client.delete(*keys)
                if cursor == 0:
                    break
            return

        for key in list(self._memory_cache):
            if key.startswith(prefix):
                self._memory_cache.pop(key, None)

    async def warm_many(self, entries: Iterable[tuple[str, Any]]) -> None:
        for key, value in entries:
            await self.set_json(key, value)


cache_service = CacheService()


def build_cache_key(*parts: object) -> str:
    return ":".join(str(part) for part in parts)
