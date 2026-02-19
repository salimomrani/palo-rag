from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from rag.pipeline import RAGPipeline
from guardrails.input import InputGuardrail
from logging_service.store import LogStore
from dependencies import get_provider, get_vectorstore, get_engine

router = APIRouter(prefix="/api", tags=["query"])
_guardrail = InputGuardrail()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
def query(request: QueryRequest):
    check = _guardrail.check(request.question)
    if not check.passed:
        LogStore(engine=get_engine()).save(
            question=request.question,
            retrieved_chunk_ids=[],
            similarity_scores=[],
            answer="",
            faithfulness_score=0.0,
            latency_ms=0,
            guardrail_triggered=check.reason,
        )
        raise HTTPException(status_code=400, detail=check.reason)

    result = RAGPipeline(
        provider=get_provider(),
        vectorstore=get_vectorstore(),
    ).query(request.question)

    LogStore(engine=get_engine()).save(
        question=request.question,
        retrieved_chunk_ids=[s["source"] for s in result.sources],
        similarity_scores=[s["score"] for s in result.sources],
        answer=result.answer,
        faithfulness_score=result.confidence_score,
        latency_ms=result.latency_ms,
        guardrail_triggered=None,
    )
    return {
        "answer": result.answer,
        "sources": result.sources,
        "confidence_score": result.confidence_score,
        "low_confidence": result.low_confidence,
        "latency_ms": result.latency_ms,
    }
