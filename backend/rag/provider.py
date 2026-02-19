import os
from typing import Protocol
from langchain_ollama import OllamaEmbeddings, ChatOllama


class AIProvider(Protocol):
    def embed(self, text: str) -> list[float]: ...
    def generate(self, prompt: str) -> str: ...
    def get_embeddings(self): ...


class OllamaProvider:
    def __init__(self):
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self._embeddings = OllamaEmbeddings(
            base_url=base_url,
            model=os.getenv("EMBED_MODEL", "nomic-embed-text"),
        )
        self._llm = ChatOllama(
            base_url=base_url,
            model=os.getenv("LLM_MODEL", "llama3.2"),
        )

    def embed(self, text: str) -> list[float]:
        return self._embeddings.embed_query(text)

    def generate(self, prompt: str) -> str:
        return self._llm.invoke(prompt).content

    def get_embeddings(self):
        return self._embeddings


def get_provider() -> OllamaProvider:
    name = os.getenv("AI_PROVIDER", "ollama")
    if name == "ollama":
        return OllamaProvider()
    raise ValueError(f"Unknown AI provider: {name}")
    # Gen-e2 would be wired here via AI_PROVIDER=gen-e2
