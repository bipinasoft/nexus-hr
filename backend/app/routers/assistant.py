from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.contracts import AssistantRequest, AssistantResponse, KnowledgeIngestRequest
from ..db.session import get_db_session
from ..platform import Permission, Principal, require_permissions
from ..services.assistant import answer_question, ingest_documents, stream_answer

router = APIRouter(prefix="/v1/assistant", tags=["assistant"])


@router.post("/query", response_model=AssistantResponse)
async def ask_assistant(
    payload: AssistantRequest,
    principal: Principal = Depends(require_permissions(Permission.ASSISTANT_USE)),
    session: AsyncSession | None = Depends(get_db_session),
) -> AssistantResponse:
    return await answer_question(
        org_id=principal.org_id,
        question=payload.question,
        top_k=payload.top_k,
        session=session,
    )


@router.post("/stream")
async def stream_assistant_query(
    payload: AssistantRequest,
    principal: Principal = Depends(require_permissions(Permission.ASSISTANT_USE)),
    session: AsyncSession | None = Depends(get_db_session),
) -> StreamingResponse:
    return StreamingResponse(
        stream_answer(
            org_id=principal.org_id,
            question=payload.question,
            top_k=payload.top_k,
            session=session,
        ),
        media_type="text/event-stream",
    )


@router.post("/index")
async def index_assistant_knowledge(
    payload: KnowledgeIngestRequest,
    principal: Principal = Depends(require_permissions(Permission.DOCUMENT_WRITE)),
    session: AsyncSession | None = Depends(get_db_session),
) -> dict[str, int | str]:
    return await ingest_documents(
        org_id=principal.org_id,
        documents=payload.documents,
        session=session,
    )
