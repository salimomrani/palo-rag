from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session as DBSession

from dependencies import get_engine
from models.db import QueryLog

router = APIRouter(tags=["history"])


@router.get("/history")
def get_history(limit: int = 50, offset: int = 0, engine=Depends(get_engine)):
    with DBSession(engine) as session:
        rows = (
            session.query(
                QueryLog.session_id,
                func.min(QueryLog.timestamp).label("started_at"),
                func.count(QueryLog.id).label("exchange_count"),
            )
            .filter(QueryLog.session_id.isnot(None))
            .group_by(QueryLog.session_id)
            .order_by(func.max(QueryLog.timestamp).desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        if not rows:
            return []

        # Single bulk query for first_question — avoids N+1
        conditions = [
            and_(QueryLog.session_id == r.session_id, QueryLog.timestamp == r.started_at)
            for r in rows
        ]
        oldest_rows = (
            session.query(QueryLog.session_id, QueryLog.question_masked)
            .filter(or_(*conditions))
            .all()
        )
        first_questions = {r.session_id: r.question_masked[:80] for r in oldest_rows}

        return [
            {
                "session_id": row.session_id,
                "started_at": row.started_at.isoformat(),
                "first_question": first_questions.get(row.session_id, ""),
                "exchange_count": row.exchange_count,
            }
            for row in rows
        ]


@router.delete("/history/{session_id}", status_code=204)
def delete_session(session_id: str, engine=Depends(get_engine)):
    with DBSession(engine) as session:
        rows = session.query(QueryLog).filter(QueryLog.session_id == session_id).all()
        if not rows:
            raise HTTPException(status_code=404, detail="Session not found")
        for row in rows:
            session.delete(row)
        session.commit()
    return Response(status_code=204)


@router.get("/history/{session_id}")
def get_session_detail(session_id: str, engine=Depends(get_engine)):
    with DBSession(engine) as session:
        rows = (
            session.query(QueryLog)
            .filter(QueryLog.session_id == session_id)
            .order_by(QueryLog.timestamp.asc())
            .all()
        )
        if not rows:
            raise HTTPException(status_code=404, detail="Session not found")
        return {
            "session_id": session_id,
            "exchanges": [
                {
                    "id": row.id,
                    "timestamp": row.timestamp.isoformat(),
                    "question_masked": row.question_masked,
                    "answer": row.answer,
                    "guardrail_triggered": row.guardrail_triggered,
                    "rejected": row.guardrail_triggered is not None,
                }
                for row in rows
            ],
        }
