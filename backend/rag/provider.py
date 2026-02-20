from typing import Generator, Protocol
from langchain_ollama import OllamaEmbeddings, ChatOllama
from core.config import settings


class AIProvider(Protocol):
    """Structural protocol for LLM backends — implement this to swap providers.

    To add a new backend (e.g. Gen-e2):
        1. Create a class implementing all four methods.
        2. Add a branch in `get_provider()` keyed by AI_PROVIDER env var.
        3. No other file needs to change.
    """

    def embed(self, text: str) -> list[float]: ...
    def generate(self, prompt: str) -> str: ...
    def stream_generate(self, prompt: str) -> Generator[str, None, None]: ...
    def get_embeddings(self): ...


class OllamaProvider:
    """AIProvider backed by a local Ollama instance.

    Uses `mxbai-embed-large` for embeddings and `qwen2.5:7b` for generation
    (configurable via EMBED_MODEL / LLM_MODEL in .env).
    """

    def __init__(self):
        self._embeddings = OllamaEmbeddings(
            base_url=settings.ollama_base_url,
            model=settings.embed_model,
        )
        self._llm = ChatOllama(
            base_url=settings.ollama_base_url,
            model=settings.llm_model,
            temperature=settings.llm_temperature,
        )

    def embed(self, text: str) -> list[float]:
        return self._embeddings.embed_query(text)

    def generate(self, prompt: str) -> str:
        return self._llm.invoke(prompt).content

    def stream_generate(self, prompt: str) -> Generator[str, None, None]:
        for chunk in self._llm.stream(prompt):
            yield chunk.content

    def get_embeddings(self):
        return self._embeddings


def get_provider() -> OllamaProvider:
    """Instantiate the configured AI provider from the AI_PROVIDER env var.

    Supported values: "ollama" (default).
    Future: set AI_PROVIDER=gen-e2 and add the corresponding branch here.
    """
    if settings.ai_provider == "ollama":
        return OllamaProvider()
    raise ValueError(f"Unknown AI provider: {settings.ai_provider}")
    # Gen-e2 would be wired here via AI_PROVIDER=gen-e2
