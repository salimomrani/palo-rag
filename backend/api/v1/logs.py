import json

from fastapi import APIRouter, Depends

from core.config import settings
from dependencies import get_engine
from logging_service.store import LogStore

router = APIRouter(tags=["logs"])


def _parse_json_list(value, default):
    if isinstance(value, list):
        return value
    if isinstance(value, str) and value.strip():
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, list) else default
        except json.JSONDecodeError:
            return default
    return default


@router.get("/logs")
def get_logs(limit: int = settings.default_logs_limit, engine=Depends(get_engine)):
    logs = LogStore(engine=engine).get_recent(limit=limit)
    return [
        {
            "id": log.id,
            "timestamp": log.timestamp.isoformat(),
            "question_masked": log.question_masked,
            "retrieved_sources": _parse_json_list(getattr(log, "retrieved_sources", None), []),
            "similarity_scores": _parse_json_list(log.similarity_scores, []),
            "answer": log.answer,
            "faithfulness_score": log.faithfulness_score,
            "latency_ms": log.latency_ms,
            "guardrail_triggered": log.guardrail_triggered,
            "rejected": log.guardrail_triggered is not None,
            "rejection_reason": log.guardrail_triggered,
        }
        for log in logs
    ]
