from typing import Protocol
from langchain_ollama import OllamaEmbeddings, ChatOllama
from core.config import settings


class AIProvider(Protocol):
    def embed(self, text: str) -> list[float]: ...
    def generate(self, prompt: str) -> str: ...
    def get_embeddings(self): ...


class OllamaProvider:
    def __init__(self):
        self._embeddings = OllamaEmbeddings(
            base_url=settings.ollama_base_url,
            model=settings.embed_model,
        )
        self._llm = ChatOllama(
            base_url=settings.ollama_base_url,
            model=settings.llm_model,
        )

    def embed(self, text: str) -> list[float]:
        return self._embeddings.embed_query(text)

    def generate(self, prompt: str) -> str:
        return self._llm.invoke(prompt).content

    def get_embeddings(self):
        return self._embeddings


def get_provider() -> OllamaProvider:
    if settings.ai_provider == "ollama":
        return OllamaProvider()
    raise ValueError(f"Unknown AI provider: {settings.ai_provider}")
    # Gen-e2 would be wired here via AI_PROVIDER=gen-e2
