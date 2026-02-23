from unittest.mock import MagicMock

from rag.pipeline import QueryResult, RAGPipeline


def make_pipeline():
    provider = MagicMock()
    provider.generate.return_value = "L'API supporte REST."
    mock_doc = MagicMock()
    mock_doc.page_content = "L'API supporte REST selon la spec v1."
    mock_doc.metadata = {"source": "spec-api-v1.md", "chunk_index": 0}
    vectorstore = MagicMock()
    vectorstore.similarity_search_with_relevance_scores.return_value = [(mock_doc, 0.87), (mock_doc, 0.72)]
    return RAGPipeline(provider=provider, vectorstore=vectorstore)


def _make_history_entry(role: str, content: str):
    entry = MagicMock()
    entry.role = role
    entry.content = content
    return entry


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
    vectorstore.similarity_search_with_relevance_scores.return_value = []
    pipeline = RAGPipeline(provider=provider, vectorstore=vectorstore)
    result = pipeline.query("Hors corpus")
    assert result.confidence_score == 0.0
    assert result.low_confidence is True


# T003 — RED: query() with history must pass history-aware prompt to provider
def test_query_with_history_uses_history_prompt():
    pipeline = make_pipeline()
    history = [
        _make_history_entry("user", "Quelles sont les étapes d'onboarding ?"),
        _make_history_entry("assistant", "Il y a 3 étapes : A, B, C."),
    ]
    pipeline.query("Qui est responsable de l'étape A ?", history=history)
    called_prompt = pipeline._provider.generate.call_args[0][0]
    assert "Historique" in called_prompt
    assert "Utilisateur" in called_prompt
    assert "étapes d'onboarding" in called_prompt


# T004 — RED: stream_query() with history must pass history-aware prompt
def test_stream_query_with_history_uses_history_prompt():
    pipeline = make_pipeline()
    pipeline._provider.stream_generate.return_value = iter(["token"])
    history = [
        _make_history_entry("user", "Comment configurer l'API ?"),
        _make_history_entry("assistant", "Via le fichier config.yaml."),
    ]
    list(pipeline.stream_query("Et pour l'authentification ?", history=history))
    called_prompt = pipeline._provider.stream_generate.call_args[0][0]
    assert "Historique" in called_prompt
    assert "Utilisateur" in called_prompt
    assert "config.yaml" in called_prompt
