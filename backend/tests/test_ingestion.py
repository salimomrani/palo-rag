from unittest.mock import MagicMock
from rag.ingestion import IngestionService


def test_ingest_text_returns_chunk_count():
    provider = MagicMock()
    vectorstore = MagicMock()
    vectorstore.add_documents.return_value = ["id1", "id2"]
    service = IngestionService(provider=provider, vectorstore=vectorstore)
    count = service.ingest_text("This is a test document. " * 50, source="test.md")
    assert count > 0
    assert vectorstore.add_documents.called


def test_ingest_text_splits_into_multiple_chunks():
    provider = MagicMock()
    captured = []
    vectorstore = MagicMock()
    vectorstore.add_documents.side_effect = lambda docs: captured.extend(docs) or [f"id{i}" for i in range(len(docs))]
    service = IngestionService(provider=provider, vectorstore=vectorstore)
    service.ingest_text("Word " * 1000, source="large.md")
    assert len(captured) > 1
    for doc in captured:
        assert len(doc.page_content) <= 3000
