from functools import lru_cache
from sqlalchemy import create_engine
from langchain_community.vectorstores import Chroma
from core.config import settings
from rag.provider import get_provider as _get_provider


@lru_cache
def get_provider():
    return _get_provider()


@lru_cache
def get_vectorstore():
    provider = get_provider()
    return Chroma(
        persist_directory=settings.chroma_path,
        embedding_function=provider.get_embeddings(),
        collection_name="corpus",
    )


@lru_cache
def get_engine():
    from models.db import Base
    engine = create_engine(settings.db_url)
    Base.metadata.create_all(engine)
    return engine
