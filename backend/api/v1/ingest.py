import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.logging import get_logger
from dependencies import get_engine, get_provider, get_vectorstore
from models.db import Document
from rag.ingestion import IngestionService
from rag.vectorstore import delete_by_source

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
    with Session(engine) as session:
        existing = session.query(Document).filter_by(name=request.name).first()
        if existing:
            raise HTTPException(
                status_code=409,
                detail=f"Document '{request.name}' déjà ingéré.",
            )

    doc_id = str(uuid.uuid4())
    service = IngestionService(provider=provider, vectorstore=vectorstore)
    chunk_count = service.ingest_text(request.text, source=request.name, doc_id=doc_id)
    doc = Document(id=doc_id, name=request.name, source=request.name, chunk_count=chunk_count)
    with Session(engine) as session:
        session.add(doc)
        session.commit()
    logger.info("Ingested %s: %d chunks", request.name, chunk_count)
    return {"name": request.name, "chunk_count": chunk_count, "document_id": doc_id}


@router.delete("/documents/{doc_id}", status_code=204)
def delete_document(
    doc_id: str,
    vectorstore=Depends(get_vectorstore),
    engine=Depends(get_engine),
):
    with Session(engine) as session:
        doc = session.get(Document, doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail=f"Document '{doc_id}' introuvable.")
        delete_by_source(vectorstore, doc.name)
        session.delete(doc)
        session.commit()
    logger.info("Deleted document %s (%s)", doc_id, doc.name)


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
