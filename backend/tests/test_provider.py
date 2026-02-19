from unittest.mock import patch, MagicMock
from rag.provider import OllamaProvider, get_provider


def test_get_provider_returns_ollama_by_default():
    with patch("rag.provider.settings") as mock_settings:
        mock_settings.ai_provider = "ollama"
        mock_settings.ollama_base_url = "http://localhost:11434"
        mock_settings.embed_model = "nomic-embed-text"
        mock_settings.llm_model = "llama3.2"
        with patch("rag.provider.OllamaEmbeddings"), patch("rag.provider.ChatOllama"):
            provider = get_provider()
            assert isinstance(provider, OllamaProvider)


def test_ollama_provider_embed_returns_list():
    mock_embeddings = MagicMock()
    mock_embeddings.embed_query.return_value = [0.1, 0.2, 0.3]
    with patch("rag.provider.OllamaEmbeddings", return_value=mock_embeddings), \
         patch("rag.provider.ChatOllama"):
        provider = OllamaProvider()
        result = provider.embed("test text")
        assert isinstance(result, list)
        assert len(result) == 3


def test_ollama_provider_generate_returns_string():
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = MagicMock(content="Generated answer")
    with patch("rag.provider.ChatOllama", return_value=mock_llm), \
         patch("rag.provider.OllamaEmbeddings"):
        provider = OllamaProvider()
        result = provider.generate("test prompt")
        assert result == "Generated answer"
