from __future__ import annotations

import asyncio
from typing import Any, TypedDict

import httpx
from langgraph.graph import END, START, StateGraph
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.contracts import AssistantResponse, KnowledgeDocumentInput
from ..platform.config import get_settings
from .vector_store import RetrievedChunk, index_documents, search_knowledge, to_citations


class AssistantState(TypedDict, total=False):
    org_id: str
    question: str
    top_k: int
    session: AsyncSession | None
    intent: str
    retrieved_chunks: list[RetrievedChunk]
    answer: str
    strategy: str
    follow_up_actions: list[str]


class LLMFallbackService:
    async def generate(self, *, question: str, context: str) -> tuple[str, str]:
        settings = get_settings()
        if settings.openai_api_key:
            try:
                answer = await self._generate_with_openai(question=question, context=context)
                return answer, "openai"
            except Exception:
                pass

        if settings.enable_local_llm_fallback:
            try:
                answer = await self._generate_with_local_llm(
                    question=question,
                    context=context,
                )
                return answer, "local-llm"
            except Exception:
                pass

        return self._generate_rule_based_answer(question=question, context=context), "rule-based"

    async def _generate_with_openai(self, *, question: str, context: str) -> str:
        settings = get_settings()

        def _call_openai() -> str:
            from openai import OpenAI

            client = OpenAI(api_key=settings.openai_api_key)
            response = client.responses.create(
                model=settings.openai_model,
                input=(
                    "You are NexusHR Copilot. Answer using the supplied HR context only when relevant.\n\n"
                    f"Question: {question}\n\nContext:\n{context}"
                ),
            )
            return response.output_text

        return await asyncio.to_thread(_call_openai)

    async def _generate_with_local_llm(self, *, question: str, context: str) -> str:
        settings = get_settings()
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                f"{settings.local_llm_base_url.rstrip('/')}/chat/completions",
                json={
                    "model": settings.local_llm_model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are NexusHR Copilot. Keep answers direct and action-oriented.",
                        },
                        {
                            "role": "user",
                            "content": f"Question: {question}\n\nContext:\n{context}",
                        },
                    ],
                    "temperature": 0.2,
                },
            )
            response.raise_for_status()
            payload = response.json()
            return payload["choices"][0]["message"]["content"]

    def _generate_rule_based_answer(self, *, question: str, context: str) -> str:
        context_lines = [line.strip() for line in context.splitlines() if line.strip()]
        evidence = "; ".join(context_lines[:3]) or "No indexed policy context was found."
        return (
            f"NexusHR Copilot reviewed your question: '{question}'. "
            f"Relevant policy evidence: {evidence}. "
            "Recommended next step: confirm the dashboard action item, then escalate to HR if the exception remains unresolved."
        )


llm_fallback_service = LLMFallbackService()


def build_assistant_graph():
    workflow = StateGraph(AssistantState)
    workflow.add_node("classify", classify_intent)
    workflow.add_node("retrieve", retrieve_context)
    workflow.add_node("respond", generate_answer)
    workflow.add_node("actions", build_follow_up_actions)
    workflow.add_edge(START, "classify")
    workflow.add_edge("classify", "retrieve")
    workflow.add_edge("retrieve", "respond")
    workflow.add_edge("respond", "actions")
    workflow.add_edge("actions", END)
    return workflow.compile()


async def classify_intent(state: AssistantState) -> AssistantState:
    question = state["question"].lower()
    intent = "general"
    if any(keyword in question for keyword in {"leave", "holiday", "vacation"}):
        intent = "leave"
    elif any(keyword in question for keyword in {"attendance", "check-in", "geofence"}):
        intent = "attendance"
    elif any(keyword in question for keyword in {"payroll", "tds", "epf", "esi"}):
        intent = "payroll"
    elif any(keyword in question for keyword in {"performance", "okr", "feedback"}):
        intent = "performance"
    return {"intent": intent}


async def retrieve_context(state: AssistantState) -> AssistantState:
    chunks = await search_knowledge(
        org_id=state["org_id"],
        query=state["question"],
        top_k=state["top_k"],
        session=state.get("session"),
    )
    return {"retrieved_chunks": chunks}


async def generate_answer(state: AssistantState) -> AssistantState:
    chunks = state.get("retrieved_chunks", [])
    context = "\n".join(
        f"[{chunk.title}] {chunk.snippet}" for chunk in chunks
    )
    answer, strategy = await llm_fallback_service.generate(
        question=state["question"],
        context=context,
    )
    return {"answer": answer, "strategy": strategy}


async def build_follow_up_actions(state: AssistantState) -> AssistantState:
    intent = state.get("intent", "general")
    action_map = {
        "attendance": [
            "Open the attendance calendar and validate missed mark-ins.",
            "Review geofence exceptions before payroll cut-off.",
        ],
        "leave": [
            "Check the leave balance cards for available quota.",
            "Escalate multi-level approvals if the request is blocked.",
        ],
        "payroll": [
            "Review payroll compliance notes and statutory deductions.",
            "Confirm EPF, ESI, and TDS tags before finalizing the run.",
        ],
        "performance": [
            "Review active OKRs and any pending 360-degree feedback items.",
            "Use the sentiment signal to prioritize coaching follow-ups.",
        ],
        "general": [
            "Open the dashboard summary for the latest alerts.",
            "Use the notification center for high-priority tasks.",
        ],
    }
    return {"follow_up_actions": action_map[intent]}


async def answer_question(
    *,
    org_id: str,
    question: str,
    top_k: int,
    session: AsyncSession | None,
) -> AssistantResponse:
    state = await assistant_graph.ainvoke(
        {
            "org_id": org_id,
            "question": question,
            "top_k": top_k,
            "session": session,
        }
    )
    chunks = state.get("retrieved_chunks", [])
    return AssistantResponse(
        answer=state["answer"],
        strategy=state["strategy"],
        intent=state["intent"],
        citations=to_citations(chunks),
        follow_up_actions=state.get("follow_up_actions", []),
    )


async def stream_answer(
    *,
    org_id: str,
    question: str,
    top_k: int,
    session: AsyncSession | None,
):
    response = await answer_question(
        org_id=org_id,
        question=question,
        top_k=top_k,
        session=session,
    )
    for segment in response.answer.split(". "):
        yield f"data: {segment.strip()}\n\n"
        await asyncio.sleep(0.05)
    yield "event: complete\ndata: done\n\n"


async def ingest_documents(
    *,
    org_id: str,
    documents: list[KnowledgeDocumentInput],
    session: AsyncSession | None,
) -> dict[str, int | str]:
    chunks_created = await index_documents(
        org_id=org_id,
        documents=documents,
        session=session,
    )
    return {
        "status": "indexed",
        "documents": len(documents),
        "chunks": chunks_created,
    }


assistant_graph = build_assistant_graph()
