import os
import uuid
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document as LCDocument
from core.config import settings


class IngestionService:
    """Splits documents into chunks and stores them in the vector store.

    Each chunk is tagged with the source filename, a shared doc_id UUID,
    and its position index within the document.
    """

    def __init__(self, provider, vectorstore):
        """Args:
            provider: AIProvider — unused directly, kept for interface symmetry.
            vectorstore: LangChain-compatible vector store (ChromaDB).
        """
        self._vectorstore = vectorstore
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

    def ingest_text(self, text: str, source: str, doc_id: str | None = None) -> int:
        """Split text into chunks and add them to the vector store.

        Args:
            text: Raw document content.
            source: Document name used as metadata (e.g. "onboarding.md").
            doc_id: Optional UUID to use as the document identifier in Chroma metadata.
                    If not provided, a new UUID is generated. Pass the DB Document.id
                    to keep Chroma metadata and PostgreSQL in sync.

        Returns:
            Number of chunks created and stored.

        Example:
            >>> svc.ingest_text("Palo IT est une ESN fondée en 2009.", "about.md")
            1
        """
        doc_id = doc_id or str(uuid.uuid4())
        chunks = self._splitter.split_text(text)
        documents = [
            LCDocument(
                page_content=f"[{source}] {chunk}",
                metadata={"source": source, "doc_id": doc_id, "chunk_index": i},
            )
            for i, chunk in enumerate(chunks)
        ]
        self._vectorstore.add_documents(documents)
        return len(documents)

    def ingest_file(self, file_path: str) -> int:
        """Read a file from disk and ingest it. Source is set to the file's basename."""
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return self.ingest_text(text, source=os.path.basename(file_path))
