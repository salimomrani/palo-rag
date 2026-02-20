import json
import time
from dataclasses import dataclass, field
from typing import Generator
from core.config import settings

LOW_CONFIDENCE_THRESHOLD = 0.5
TOP_K = 4

NO_INFO = "Je n'ai pas d'information sur ce sujet dans la base de connaissance."

PROMPT_TEMPLATE = """Tu es l'assistant de support de PALO Platform. Utilise le contexte fourni pour répondre à la question de manière directe et concise.

Règles :
- Réponds en français.
- Base-toi sur le contexte fourni. Si une information est partielle, donne ce que tu sais et précise la limite.
- Si le contexte ne contient vraiment aucune information pertinente, dis uniquement : "Je n'ai pas d'information sur ce sujet dans la base de connaissance."
- Ne répète pas la question. Ne commence pas par "Bien sûr" ou des formules creuses.

Contexte :
{context}

Question : {question}

Réponse :"""


@dataclass
class QueryResult:
    answer: str
    sources: list[dict] = field(default_factory=list)
    confidence_score: float = 0.0
    low_confidence: bool = False
    latency_ms: int = 0


def _retrieve(vectorstore, question: str) -> tuple[list, float]:
    """Return (results, avg_score) using relevance scores normalized to [0, 1]."""
    results = vectorstore.similarity_search_with_relevance_scores(question, k=TOP_K)
    if not results:
        return [], 0.0
    scores = [max(0.0, min(1.0, s)) for _, s in results]
    return results, round(sum(scores) / len(scores), 3)


def _build_sources(results) -> list[dict]:
    return [
        {
            "source": doc.metadata.get("source", "unknown"),
            "excerpt": doc.page_content[:200],
            "score": round(max(0.0, min(1.0, score)), 3),
        }
        for doc, score in results
    ]


def _build_context(results) -> str:
    return "\n\n".join(
        f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
        for doc, _ in results
    )


class RAGPipeline:
    def __init__(self, provider, vectorstore):
        self._provider = provider
        self._vectorstore = vectorstore

    def query(self, question: str) -> QueryResult:
        start = time.time()
        results, avg_score = _retrieve(self._vectorstore, question)

        if not results or avg_score < settings.min_retrieval_score:
            return QueryResult(
                answer=NO_INFO,
                sources=[],
                confidence_score=0.0,
                low_confidence=True,
                latency_ms=int((time.time() - start) * 1000),
            )

        answer = self._provider.generate(
            PROMPT_TEMPLATE.format(context=_build_context(results), question=question)
        )
        return QueryResult(
            answer=answer,
            sources=_build_sources(results),
            confidence_score=avg_score,
            low_confidence=avg_score < LOW_CONFIDENCE_THRESHOLD,
            latency_ms=int((time.time() - start) * 1000),
        )

    def stream_query(self, question: str) -> Generator[str, None, None]:
        """Yield SSE-formatted events: meta → tokens → done."""
        start = time.time()
        results, avg_score = _retrieve(self._vectorstore, question)

        if not results or avg_score < settings.min_retrieval_score:
            yield f"data: {json.dumps({'type': 'meta', 'sources': [], 'confidence_score': 0.0, 'low_confidence': True})}\n\n"
            yield f"data: {json.dumps({'type': 'token', 'content': NO_INFO})}\n\n"
            yield f"data: {json.dumps({'type': 'done', 'latency_ms': int((time.time() - start) * 1000), 'answer': NO_INFO})}\n\n"
            return

        sources = _build_sources(results)
        yield f"data: {json.dumps({'type': 'meta', 'sources': sources, 'confidence_score': avg_score, 'low_confidence': avg_score < LOW_CONFIDENCE_THRESHOLD})}\n\n"

        full_answer = ""
        for token in self._provider.stream_generate(PROMPT_TEMPLATE.format(context=_build_context(results), question=question)):
            full_answer += token
            yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"

        yield f"data: {json.dumps({'type': 'done', 'latency_ms': int((time.time() - start) * 1000), 'answer': full_answer})}\n\n"
