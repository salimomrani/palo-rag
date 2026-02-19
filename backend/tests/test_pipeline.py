from unittest.mock import MagicMock
from rag.pipeline import RAGPipeline, QueryResult


def make_pipeline():
    provider = MagicMock()
    provider.generate.return_value = "L'API supporte REST."
    mock_doc = MagicMock()
    mock_doc.page_content = "L'API supporte REST selon la spec v1."
    mock_doc.metadata = {"source": "spec-api-v1.md", "chunk_index": 0}
    vectorstore = MagicMock()
    vectorstore.similarity_search_with_score.return_value = [(mock_doc, 0.87), (mock_doc, 0.72)]
    return RAGPipeline(provider=provider, vectorstore=vectorstore)


def test_query_returns_answer():
    result = make_pipeline().query("Quels protocoles ?")
    assert isinstance(result, QueryResult)
    assert len(result.answer) > 0


def test_query_returns_sources():
    result = make_pipeline().query("Quels protocoles ?")
    assert len(result.sources) > 0
    assert result.sources[0]["source"] == "spec-api-v1.md"
    assert result.sources[0]["score"] == 0.87


def test_query_returns_confidence():
    result = make_pipeline().query("Quels protocoles ?")
    assert 0.0 <= result.confidence_score <= 1.0


def test_query_no_results_returns_low_confidence():
    provider = MagicMock()
    provider.generate.return_value = "Je ne sais pas."
    vectorstore = MagicMock()
    vectorstore.similarity_search_with_score.return_value = []
    pipeline = RAGPipeline(provider=provider, vectorstore=vectorstore)
    result = pipeline.query("Hors corpus")
    assert result.confidence_score == 0.0
    assert result.low_confidence is True
