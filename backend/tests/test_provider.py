from unittest.mock import patch, MagicMock
from rag.provider import OllamaProvider, get_provider


def test_get_provider_returns_ollama_by_default(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "ollama")
    provider = get_provider()
    assert isinstance(provider, OllamaProvider)


def test_ollama_provider_embed_returns_list(monkeypatch):
    monkeypatch.setenv("EMBED_MODEL", "nomic-embed-text")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434")
    mock_embeddings = MagicMock()
    mock_embeddings.embed_query.return_value = [0.1, 0.2, 0.3]
    with patch("rag.provider.OllamaEmbeddings", return_value=mock_embeddings):
        provider = OllamaProvider()
        result = provider.embed("test text")
        assert isinstance(result, list)
        assert len(result) == 3


def test_ollama_provider_generate_returns_string(monkeypatch):
    monkeypatch.setenv("LLM_MODEL", "llama3.2")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434")
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = MagicMock(content="Generated answer")
    with patch("rag.provider.ChatOllama", return_value=mock_llm):
        provider = OllamaProvider()
        result = provider.generate("test prompt")
        assert result == "Generated answer"
