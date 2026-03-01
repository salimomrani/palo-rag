from functools import lru_cache

from langchain_chroma import Chroma
from sqlalchemy import create_engine, text

from core.config import settings
from rag.provider import get_provider as _get_provider


@lru_cache
def get_provider():
    """Return the singleton AIProvider instance (cached per process)."""
    return _get_provider()


@lru_cache
def get_vectorstore():
    """Return the singleton ChromaDB vector store (cached per process).

    Uses the provider's embedding function so the same model is used
    for both ingestion and retrieval.
    """
    provider = get_provider()
    return Chroma(
        persist_directory=settings.chroma_path,
        embedding_function=provider.get_embeddings(),
        collection_name="corpus",
    )


@lru_cache
def get_engine():
    """Return the singleton SQLAlchemy engine and ensure all tables exist."""
    from models.db import Base
    engine = create_engine(settings.db_url)
    Base.metadata.create_all(engine)
    with engine.connect() as conn:
        conn.execute(text(
            "ALTER TABLE query_logs ADD COLUMN IF NOT EXISTS session_id VARCHAR;"
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS ix_query_logs_session_id ON query_logs(session_id);"
        ))
        conn.commit()
    return engine
