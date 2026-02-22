import json
import time
from dataclasses import dataclass, field
from typing import Generator

from core.config import settings
from rag.prompts import RAG_PROMPT


@dataclass
class QueryResult:
    answer: str
    sources: list[dict] = field(default_factory=list)
    confidence_score: float = 0.0
    low_confidence: bool = False
    latency_ms: int = 0


def _retrieve(vectorstore, question: str) -> tuple[list, float]:
    """Return (results, avg_score) using relevance scores normalized to [0, 1]."""
    results = vectorstore.similarity_search_with_relevance_scores(question, k=settings.top_k)
    if not results:
        return [], 0.0
    scores = [max(0.0, min(1.0, s)) for _, s in results]
    return results, round(sum(scores) / len(scores), 3)


def _build_sources(results) -> list[dict]:
    """Build serializable source list with excerpt and clamped similarity score."""
    return [
        {
            "source": doc.metadata.get("source", "unknown"),
            "excerpt": doc.page_content[:200],
            "score": round(max(0.0, min(1.0, score)), 3),
        }
        for doc, score in results
    ]


def _build_context(results) -> str:
    """Concatenate retrieved chunks into a single labelled context string for the prompt."""
    return "\n\n".join(
        f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
        for doc, _ in results
    )


class RAGPipeline:
    def __init__(self, provider, vectorstore):
        """
        Args:
            provider: AIProvider implementation (OllamaProvider or any swappable backend).
            vectorstore: LangChain-compatible vector store (ChromaDB).
        """
        self._provider = provider
        self._vectorstore = vectorstore

    def query(self, question: str) -> QueryResult:
        """Run a blocking RAG query: retrieve → generate → return structured result.

        Returns a refusal QueryResult if retrieval confidence is below MIN_RETRIEVAL_SCORE.
        """
        start = time.time()
        results, avg_score = _retrieve(self._vectorstore, question)

        if not results or avg_score < settings.min_retrieval_score:
            return QueryResult(
                answer=settings.no_info_message,
                sources=[],
                confidence_score=0.0,
                low_confidence=True,
                latency_ms=int((time.time() - start) * 1000),
            )

        answer = self._provider.generate(
            RAG_PROMPT.format(context=_build_context(results), question=question)
        )
        return QueryResult(
            answer=answer,
            sources=_build_sources(results),
            confidence_score=avg_score,
            low_confidence=avg_score < settings.low_confidence_threshold,
            latency_ms=int((time.time() - start) * 1000),
        )

    def stream_query(self, question: str) -> Generator[str, None, None]:
        """Yield SSE-formatted events: meta → tokens → done."""
        start = time.time()
        results, avg_score = _retrieve(self._vectorstore, question)

        if not results or avg_score < settings.min_retrieval_score:
            yield f"data: {json.dumps({'type': 'meta', 'sources': [], 'confidence_score': 0.0, 'low_confidence': True})}\n\n"
            yield f"data: {json.dumps({'type': 'token', 'content': settings.no_info_message})}\n\n"
            yield f"data: {json.dumps({'type': 'done', 'latency_ms': int((time.time() - start) * 1000), 'answer': settings.no_info_message})}\n\n"
            return

        sources = _build_sources(results)
        yield f"data: {json.dumps({'type': 'meta', 'sources': sources, 'confidence_score': avg_score, 'low_confidence': avg_score < settings.low_confidence_threshold})}\n\n"

        full_answer = ""
        for token in self._provider.stream_generate(RAG_PROMPT.format(context=_build_context(results), question=question)):
            full_answer += token
            yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"

        yield f"data: {json.dumps({'type': 'done', 'latency_ms': int((time.time() - start) * 1000), 'answer': full_answer})}\n\n"
