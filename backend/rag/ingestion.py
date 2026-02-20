import os
import uuid
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document as LCDocument

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


class IngestionService:
    def __init__(self, provider, vectorstore):
        self._vectorstore = vectorstore
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )

    def ingest_text(self, text: str, source: str) -> int:
        doc_id = str(uuid.uuid4())
        chunks = self._splitter.split_text(text)
        documents = [
            LCDocument(
                page_content=chunk,
                metadata={"source": source, "doc_id": doc_id, "chunk_index": i},
            )
            for i, chunk in enumerate(chunks)
        ]
        self._vectorstore.add_documents(documents)
        return len(documents)

    def ingest_file(self, file_path: str) -> int:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return self.ingest_text(text, source=os.path.basename(file_path))
