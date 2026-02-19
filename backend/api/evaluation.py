import json
from fastapi import APIRouter
from sqlalchemy.orm import Session
from models.db import EvaluationResult
from dependencies import get_provider, get_vectorstore, get_engine

router = APIRouter(prefix="/api", tags=["evaluation"])


@router.post("/evaluation/run")
def run_quality_check():
    from quality.runner import run_quality_check as _run
    scores = _run(
        provider=get_provider(),
        vectorstore=get_vectorstore(),
        engine=get_engine(),
    )
    return {"status": "completed", "scores": scores}


@router.get("/evaluation/report")
def get_quality_report():
    with Session(get_engine()) as session:
        result = (
            session.query(EvaluationResult)
            .order_by(EvaluationResult.run_at.desc())
            .first()
        )
        if not result:
            return {"message": "No evaluation run yet. Call POST /api/evaluation/run first."}
        return {
            "run_at": result.run_at.isoformat(),
            "faithfulness": result.faithfulness,
            "answer_relevancy": result.answer_relevancy,
            "context_recall": result.context_recall,
            "per_question": json.loads(result.per_question),
        }
