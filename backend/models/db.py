import uuid
from datetime import datetime, UTC
from sqlalchemy import String, Float, Integer, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    chunk_count: Mapped[int] = mapped_column(Integer, default=0)
    ingested_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))


class QueryLog(Base):
    __tablename__ = "query_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    question_masked: Mapped[str] = mapped_column(Text, nullable=False)
    retrieved_chunk_ids: Mapped[str] = mapped_column(Text, default="[]")
    similarity_scores: Mapped[str] = mapped_column(Text, default="[]")
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    faithfulness_score: Mapped[float] = mapped_column(Float, default=0.0)
    latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    guardrail_triggered: Mapped[str | None] = mapped_column(String, nullable=True)


class EvaluationResult(Base):
    __tablename__ = "evaluation_results"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    run_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    faithfulness: Mapped[float] = mapped_column(Float, default=0.0)
    answer_relevancy: Mapped[float] = mapped_column(Float, default=0.0)
    context_recall: Mapped[float] = mapped_column(Float, default=0.0)
    per_question: Mapped[str] = mapped_column(Text, default="[]")
