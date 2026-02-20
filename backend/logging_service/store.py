import uuid
from sqlalchemy.orm import Session
from models.db import QueryLog
from logging_service.pii import mask_pii


class LogStore:
    """Audit log store — persists every query (accepted or rejected) to PostgreSQL.

    Questions are PII-masked before storage; the original text is never written to DB.
    """

    def __init__(self, engine):
        """Args:
            engine: SQLAlchemy engine connected to the PostgreSQL instance.
        """
        self._engine = engine

    def save(
        self,
        question: str,
        retrieved_sources: list[str],
        similarity_scores: list[float],
        answer: str,
        faithfulness_score: float,
        latency_ms: int,
        guardrail_triggered: str | None,
    ) -> QueryLog:
        """Persist a query log entry with the question PII-masked.

        Args:
            guardrail_triggered: rejection reason string (e.g. "guardrail:prompt_injection"),
                                 or None if the query was accepted.

        Returns:
            The persisted QueryLog ORM instance (with generated UUID and timestamp).
        """
        log = QueryLog(
            id=str(uuid.uuid4()),
            question_masked=mask_pii(question),
            retrieved_sources=retrieved_sources,
            similarity_scores=similarity_scores,
            answer=answer,
            faithfulness_score=faithfulness_score,
            latency_ms=latency_ms,
            guardrail_triggered=guardrail_triggered,
        )
        with Session(self._engine) as session:
            session.add(log)
            session.commit()
            session.refresh(log)
        return log

    def get_recent(self, limit: int = 100) -> list[QueryLog]:
        """Return the most recent log entries ordered by timestamp descending."""
        with Session(self._engine) as session:
            return (
                session.query(QueryLog)
                .order_by(QueryLog.timestamp.desc())
                .limit(limit)
                .all()
            )
