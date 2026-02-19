import uuid
from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models.db import Document
from rag.ingestion import IngestionService
from dependencies import get_provider, get_vectorstore, get_engine

router = APIRouter(prefix="/api", tags=["ingest"])


class IngestTextRequest(BaseModel):
    text: str
    name: str


@router.post("/ingest")
def ingest_text(request: IngestTextRequest):
    service = IngestionService(
        provider=get_provider(),
        vectorstore=get_vectorstore(),
    )
    chunk_count = service.ingest_text(request.text, source=request.name)
    doc_id = str(uuid.uuid4())
    doc = Document(
        id=doc_id,
        name=request.name,
        source=request.name,
        chunk_count=chunk_count,
    )
    with Session(get_engine()) as session:
        session.add(doc)
        session.commit()
    return {"name": request.name, "chunk_count": chunk_count, "document_id": doc_id}


@router.get("/documents")
def list_documents():
    with Session(get_engine()) as session:
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
