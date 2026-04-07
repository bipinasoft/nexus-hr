from __future__ import annotations

import asyncio
import hashlib
import math

from ..platform.config import get_settings


class DeterministicEmbeddingService:
    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        settings = get_settings()
        dimensions = settings.vector_dimensions
        vectors: list[list[float]] = []
        for text in texts:
            vector = [0.0] * dimensions
            for token in text.lower().split():
                digest = hashlib.blake2b(token.encode("utf-8"), digest_size=16).digest()
                for index, value in enumerate(digest):
                    target_index = (value + index) % dimensions
                    delta = ((value / 255) * 2) - 1
                    vector[target_index] += delta
            magnitude = math.sqrt(sum(component * component for component in vector)) or 1.0
            vectors.append([component / magnitude for component in vector])
        return vectors


class OpenAIEmbeddingService:
    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        settings = get_settings()
        if not settings.openai_api_key:
            raise RuntimeError("OpenAI API key is not configured.")

        def _embed() -> list[list[float]]:
            from openai import OpenAI

            client = OpenAI(api_key=settings.openai_api_key)
            response = client.embeddings.create(
                model=settings.openai_embedding_model,
                input=texts,
            )
            return [item.embedding for item in response.data]

        return await asyncio.to_thread(_embed)


class EmbeddingService:
    def __init__(self) -> None:
        self._openai = OpenAIEmbeddingService()
        self._deterministic = DeterministicEmbeddingService()

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        settings = get_settings()
        if settings.openai_api_key:
            try:
                return await self._openai.embed_texts(texts)
            except Exception:
                pass
        return await self._deterministic.embed_texts(texts)


embedding_service = EmbeddingService()
