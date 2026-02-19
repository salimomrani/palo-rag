import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.db import EvaluationResult
from dependencies import get_provider, get_vectorstore, get_engine

router = APIRouter(tags=["evaluation"])


@router.post("/evaluation/run")
def run_quality_check(
    provider=Depends(get_provider),
    vectorstore=Depends(get_vectorstore),
    engine=Depends(get_engine),
):
    from quality.runner import run_quality_check as _run
    scores = _run(provider=provider, vectorstore=vectorstore, engine=engine)
    return {"status": "completed", "scores": scores}


@router.get("/evaluation/report")
def get_quality_report(engine=Depends(get_engine)):
    with Session(engine) as session:
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
