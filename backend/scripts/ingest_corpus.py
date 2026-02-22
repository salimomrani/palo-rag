"""Ingest all corpus documents into ChromaDB and SQLite."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv

load_dotenv()

import uuid
from pathlib import Path

from sqlalchemy.orm import Session

from core.logging import get_logger
from dependencies import get_engine, get_provider, get_vectorstore
from models.db import Document
from rag.ingestion import IngestionService

logger = get_logger(__name__)

CORPUS_DIR = Path(__file__).parent.parent.parent / "corpus"


def main():
    provider = get_provider()
    vectorstore = get_vectorstore()
    engine = get_engine()

    service = IngestionService(provider=provider, vectorstore=vectorstore)

    docs = sorted(CORPUS_DIR.glob("*.md"))
    if not docs:
        logger.error("No documents found in %s", CORPUS_DIR)
        sys.exit(1)

    logger.info("Ingesting %d documents from %s", len(docs), CORPUS_DIR)

    for path in docs:
        text = path.read_text(encoding="utf-8")
        source = path.name
        doc_id = str(uuid.uuid4())
        chunk_count = service.ingest_text(text, source=source, doc_id=doc_id)
        with Session(engine) as session:
            session.add(Document(id=doc_id, name=source, source=source, chunk_count=chunk_count))
            session.commit()

        logger.info("  ✓ %s — %d chunks", source, chunk_count)

    logger.info("Done. %d documents ingested.", len(docs))


if __name__ == "__main__":
    main()
