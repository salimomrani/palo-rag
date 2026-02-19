import uuid
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models.db import Document
from rag.ingestion import IngestionService
from dependencies import get_provider, get_vectorstore, get_engine
from core.logging import get_logger

router = APIRouter(tags=["ingest"])
logger = get_logger(__name__)


class IngestTextRequest(BaseModel):
    text: str
    name: str


@router.post("/ingest")
def ingest_text(
    request: IngestTextRequest,
    provider=Depends(get_provider),
    vectorstore=Depends(get_vectorstore),
    engine=Depends(get_engine),
):
    service = IngestionService(provider=provider, vectorstore=vectorstore)
    chunk_count = service.ingest_text(request.text, source=request.name)
    doc_id = str(uuid.uuid4())
    doc = Document(id=doc_id, name=request.name, source=request.name, chunk_count=chunk_count)
    with Session(engine) as session:
        session.add(doc)
        session.commit()
    logger.info("Ingested %s: %d chunks", request.name, chunk_count)
    return {"name": request.name, "chunk_count": chunk_count, "document_id": doc_id}


@router.get("/documents")
def list_documents(engine=Depends(get_engine)):
    with Session(engine) as session:
        docs = session.query(Document).order_by(Document.ingested_at.desc()).all()
        return [
            {
                "id": d.id,
                "name": d.name,
                "chunk_count": d.chunk_count,
                "ingested_at": d.ingested_at.isoformat(),
            }
            for d in docs
        ]
