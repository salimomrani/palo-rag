import os
from functools import lru_cache
from sqlalchemy import create_engine
from langchain_community.vectorstores import Chroma
from rag.provider import get_provider as _get_provider


@lru_cache
def get_provider():
    return _get_provider()


@lru_cache
def get_vectorstore():
    provider = get_provider()
    chroma_path = os.getenv("CHROMA_PATH", "./chroma_data")
    return Chroma(
        persist_directory=chroma_path,
        embedding_function=provider.get_embeddings(),
        collection_name="corpus",
    )


@lru_cache
def get_engine():
    db_url = os.getenv("DB_URL", "postgresql://palo:palo@localhost:5432/palo_rag")
    from models.db import Base
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine
