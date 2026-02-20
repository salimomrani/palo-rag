import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.db import Base, Document, QueryLog, EvaluationResult

engine = create_engine("sqlite:///:memory:")


def setup_function():
    Base.metadata.create_all(engine)


def teardown_function():
    Base.metadata.drop_all(engine)


def test_document_creation():
    with Session(engine) as session:
        doc = Document(id=str(uuid.uuid4()), name="test.md", source="corpus/test.md", chunk_count=5)
        session.add(doc)
        session.commit()
        fetched = session.get(Document, doc.id)
        assert fetched.name == "test.md"
        assert fetched.chunk_count == 5
        assert fetched.ingested_at is not None


def test_query_log_creation():
    with Session(engine) as session:
        log = QueryLog(
            id=str(uuid.uuid4()),
            question_masked="Comment fonctionne [EMAIL] ?",
            retrieved_sources=["doc1.md"],
            similarity_scores=[0.87],
            answer="L'API utilise REST.",
            faithfulness_score=0.91,
            latency_ms=1240,
            guardrail_triggered=None,
        )
        session.add(log)
        session.commit()
        fetched = session.get(QueryLog, log.id)
        assert fetched.faithfulness_score == 0.91


def test_evaluation_result_creation():
    with Session(engine) as session:
        result = EvaluationResult(
            id=str(uuid.uuid4()),
            faithfulness=0.85,
            answer_relevancy=0.78,
            context_recall=0.82,
            per_question=[],
        )
        session.add(result)
        session.commit()
        fetched = session.get(EvaluationResult, result.id)
        assert fetched.faithfulness == 0.85
