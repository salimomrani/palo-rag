import time
from dataclasses import dataclass, field

LOW_CONFIDENCE_THRESHOLD = 0.5
TOP_K = 4

PROMPT_TEMPLATE = """Tu es un assistant de support interne. Réponds à la question en te basant UNIQUEMENT sur le contexte fourni.
Si le contexte ne contient pas l'information, dis "Je n'ai pas d'information sur ce sujet dans la base de connaissance."

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


class RAGPipeline:
    def __init__(self, provider, vectorstore):
        self._provider = provider
        self._vectorstore = vectorstore

    def query(self, question: str) -> QueryResult:
        start = time.time()
        results = self._vectorstore.similarity_search_with_score(question, k=TOP_K)

        if not results:
            return QueryResult(
                answer="Je n'ai pas d'information sur ce sujet dans la base de connaissance.",
                sources=[],
                confidence_score=0.0,
                low_confidence=True,
                latency_ms=int((time.time() - start) * 1000),
            )

        scores = [s for _, s in results]
        avg_score = sum(scores) / len(scores)
        context = "\n\n".join(
            f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
            for doc, _ in results
        )
        answer = self._provider.generate(
            PROMPT_TEMPLATE.format(context=context, question=question)
        )
        sources = [
            {
                "source": doc.metadata.get("source", "unknown"),
                "excerpt": doc.page_content[:200],
                "score": round(score, 3),
            }
            for doc, score in results
        ]
        return QueryResult(
            answer=answer,
            sources=sources,
            confidence_score=round(avg_score, 3),
            low_confidence=avg_score < LOW_CONFIDENCE_THRESHOLD,
            latency_ms=int((time.time() - start) * 1000),
        )
