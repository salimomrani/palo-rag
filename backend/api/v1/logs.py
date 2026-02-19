import json
from fastapi import APIRouter, Depends
from logging_service.store import LogStore
from dependencies import get_engine

router = APIRouter(tags=["logs"])


@router.get("/logs")
def get_logs(limit: int = 100, engine=Depends(get_engine)):
    logs = LogStore(engine=engine).get_recent(limit=limit)
    return [
        {
            "id": log.id,
            "timestamp": log.timestamp.isoformat(),
            "question_masked": log.question_masked,
            "answer": log.answer,
            "faithfulness_score": log.faithfulness_score,
            "latency_ms": log.latency_ms,
            "guardrail_triggered": log.guardrail_triggered,
            "similarity_scores": json.loads(log.similarity_scores),
        }
        for log in logs
    ]
