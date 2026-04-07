from __future__ import annotations

import math
from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.contracts import KnowledgeCitation, KnowledgeDocumentInput
from ..core.demo_data import DEMO_ORG_ID, DEMO_POLICY_DOCUMENTS
from ..db.models import KnowledgeChunk, KnowledgeDocument
from .embeddings import embedding_service


@dataclass
class RetrievedChunk:
    title: str
    source: str
    snippet: str
    score: float


_memory_chunks: list[dict[str, object]] = []


async def seed_memory_vector_store() -> None:
    if _memory_chunks:
        return
    await index_documents(
        org_id=DEMO_ORG_ID,
        documents=[
            KnowledgeDocumentInput.model_validate(item) for item in DEMO_POLICY_DOCUMENTS
        ],
        session=None,
    )


async def index_documents(
    *,
    org_id: str,
    documents: list[KnowledgeDocumentInput],
    session: AsyncSession | None,
) -> int:
    chunks_created = 0
    for document in documents:
        pieces = _chunk_content(document.content)
        embeddings = await embedding_service.embed_texts(pieces)
        _replace_memory_document(org_id=org_id, source=document.source)
        if session is not None:
            existing_document = await session.scalar(
                select(KnowledgeDocument).where(
                    KnowledgeDocument.org_id == org_id,
                    KnowledgeDocument.source == document.source,
                )
            )
            if existing_document is not None:
                await session.execute(
                    delete(KnowledgeChunk).where(
                        KnowledgeChunk.document_id == existing_document.id
                    )
                )
                await session.delete(existing_document)
                await session.flush()

            persisted_document = KnowledgeDocument(
                id=f"doc-{uuid4()}",
                org_id=org_id,
                title=document.title,
                source=document.source,
                tags=document.tags,
                status="indexed",
            )
            session.add(persisted_document)
            await session.flush()
        else:
            persisted_document = None

        for index, (content, embedding) in enumerate(zip(pieces, embeddings, strict=True)):
            memory_chunk = {
                "org_id": org_id,
                "title": document.title,
                "source": document.source,
                "content": content,
                "embedding": embedding,
            }
            _memory_chunks.append(memory_chunk)
            chunks_created += 1

            if session is not None and persisted_document is not None:
                session.add(
                    KnowledgeChunk(
                        id=f"chunk-{uuid4()}",
                        org_id=org_id,
                        document_id=persisted_document.id,
                        chunk_index=index,
                        content=content,
                        metadata_json={"source": document.source, "title": document.title},
                        embedding=embedding,
                    )
                )

    if session is not None:
        await session.commit()
    return chunks_created


async def search_knowledge(
    *,
    org_id: str,
    query: str,
    top_k: int,
    session: AsyncSession | None,
) -> list[RetrievedChunk]:
    query_embedding = (await embedding_service.embed_texts([query]))[0]
    if session is not None:
        try:
            result = await session.execute(
                select(KnowledgeChunk, KnowledgeDocument)
                .join(KnowledgeDocument, KnowledgeChunk.document_id == KnowledgeDocument.id)
                .where(KnowledgeChunk.org_id == org_id)
                .order_by(KnowledgeChunk.embedding.cosine_distance(query_embedding))
                .limit(top_k)
            )
            rows = result.all()
            if rows:
                return [
                    RetrievedChunk(
                        title=document.title,
                        source=document.source,
                        snippet=chunk.content[:320],
                        score=1.0,
                    )
                    for chunk, document in rows
                ]
        except Exception:
            pass

    await seed_memory_vector_store()
    scored_chunks = [
        RetrievedChunk(
            title=str(item["title"]),
            source=str(item["source"]),
            snippet=str(item["content"])[:320],
            score=_cosine_similarity(query_embedding, item["embedding"]),
        )
        for item in _memory_chunks
        if item["org_id"] == org_id
    ]
    scored_chunks.sort(key=lambda item: item.score, reverse=True)
    return scored_chunks[:top_k]


def to_citations(chunks: list[RetrievedChunk]) -> list[KnowledgeCitation]:
    return [
        KnowledgeCitation(
            title=chunk.title,
            source=chunk.source,
            snippet=chunk.snippet,
        )
        for chunk in chunks
    ]


def _replace_memory_document(*, org_id: str, source: str) -> None:
    global _memory_chunks
    _memory_chunks = [
        item
        for item in _memory_chunks
        if not (item["org_id"] == org_id and item["source"] == source)
    ]


def _chunk_content(content: str, chunk_size: int = 70, overlap: int = 12) -> list[str]:
    words = content.split()
    chunks: list[str] = []
    cursor = 0
    while cursor < len(words):
        chunk_words = words[cursor : cursor + chunk_size]
        chunks.append(" ".join(chunk_words))
        if cursor + chunk_size >= len(words):
            break
        cursor += max(chunk_size - overlap, 1)
    return chunks


def _cosine_similarity(left: list[float], right: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(left, right, strict=True))
    left_magnitude = math.sqrt(sum(a * a for a in left)) or 1.0
    right_magnitude = math.sqrt(sum(b * b for b in right)) or 1.0
    return dot_product / (left_magnitude * right_magnitude)
