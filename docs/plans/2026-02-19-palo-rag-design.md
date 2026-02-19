# Design: PALO RAG Knowledge Assistant

**Date**: 2026-02-19
**Spec**: specs/1-rag-assistant/spec.md

---

## Architecture

### Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| LLM | Ollama (`llama3.2`) | Local inference, no API key, fast on M-series |
| Embeddings | Ollama (`nomic-embed-text`) | High quality, free, local |
| Vector Store | ChromaDB (embedded) | Zero config, file-based, sufficient for demo |
| RAG framework | LangChain (Python) | Industry standard, mature ecosystem |
| Evaluation | RAGAS | Purpose-built for RAG metrics |
| API | FastAPI | Async, auto-docs, Pydantic validation |
| Persistence | SQLite + SQLAlchemy | Zero config, embedded, queryable |
| Frontend | Angular 21 | User's primary stack, standalone components |
| Gen-e2 mock | `AIProvider` interface | Swappable via env var `AI_PROVIDER=gen-e2|ollama` |

### Repository Layout

```
PALO-RAG/
├── backend/
│   ├── main.py                  ← FastAPI app + CORS
│   ├── api/
│   │   ├── ingest.py            ← POST /api/ingest, GET /api/documents
│   │   ├── query.py             ← POST /api/query
│   │   ├── logs.py              ← GET /api/logs
│   │   └── eval.py              ← POST /api/eval/run, GET /api/eval/report
│   ├── rag/
│   │   ├── provider.py          ← AIProvider interface (Ollama / Gen-e2 mock)
│   │   ├── ingestion.py         ← chunk → embed → ChromaDB
│   │   └── pipeline.py          ← query → retrieve → augment → generate
│   ├── guardrails/
│   │   ├── input.py             ← length, injection, off-topic
│   │   └── output.py            ← groundedness, confidence
│   ├── eval/
│   │   ├── runner.py            ← RAGAS evaluation
│   │   ├── dataset.py           ← 15-Q reference dataset
│   │   └── report.py            ← generates reports/eval.md
│   ├── models/
│   │   └── db.py                ← SQLAlchemy models (Document, QueryLog, EvalResult)
│   └── requirements.txt
├── frontend/
│   └── src/app/
│       ├── chat/                ← ChatComponent (signals, OnPush)
│       ├── ingest/              ← IngestComponent
│       └── logs/                ← LogsComponent
├── corpus/
│   ├── faq-produits.md
│   ├── spec-technique-api.md
│   ├── tickets-support.md
│   └── ... (15 files total)
├── reports/
│   └── eval.md                  ← auto-generated
├── specs/                       ← spec-kit artifacts
├── docs/plans/                  ← design docs
├── README.md
└── DECISIONS.md
```

---

## RAG Pipeline

### Ingestion Flow

```
File upload / text paste
  → TextSplitter(chunk_size=500, chunk_overlap=50)
  → OllamaEmbeddings("nomic-embed-text")
  → ChromaDB.add_documents()
  → SQLite: Document record created
```

### Query Flow

```
User question
  → InputGuardrail
      ├─ length check (>500 chars → 400)
      ├─ injection patterns (regex → 400)
      └─ off-topic check (embedding similarity to anchor < 0.3 → flagged)
  → OllamaEmbeddings("nomic-embed-text")
  → ChromaDB.similarity_search(k=4)
  → OutputGuardrail: avg_score < 0.5 → low_confidence flag
  → PromptTemplate(question, chunks)
  → Ollama("llama3.2")
  → Response: { answer, sources[], confidence_score, latency_ms }
  → SQLite: QueryLog persisted (PII masked)
```

---

## Guardrails

### Input

| Check | Threshold | Response |
|-------|-----------|----------|
| Max length | 500 chars | 400 + reason |
| Prompt injection | Regex patterns | 400 + reason |
| Off-topic | Embedding similarity < 0.3 to corpus anchor | 200 + low_confidence flag |
| Rate limit | 10 req/min/IP | 429 |

### Output

| Check | Threshold | Behavior |
|-------|-----------|----------|
| Low groundedness | Avg chunk score < 0.5 | Response flagged, user notified |
| No chunks retrieved | 0 results | "I don't have information on this" |

---

## Traceability

Each `QueryLog` record contains:
```json
{
  "id": "uuid",
  "timestamp": "2026-02-19T14:30:00Z",
  "question_masked": "Comment puis-je [REDACTED] ?",
  "retrieved_chunk_ids": ["doc1#chunk3", "doc2#chunk1"],
  "similarity_scores": [0.87, 0.72, 0.65, 0.61],
  "answer": "...",
  "faithfulness_score": 0.91,
  "latency_ms": 2340,
  "guardrail_triggered": null
}
```

PII masking: regex applied to `question` before log insertion (`\b[\w.-]+@[\w.-]+\.\w+\b` → `[EMAIL]`, phone patterns → `[PHONE]`).

---

## Evaluation

**Reference dataset**: 15 Q/A pairs, one per corpus document category.

**RAGAS metrics computed**:
- `faithfulness`: Is the answer supported by the retrieved context?
- `answer_relevancy`: Does the answer address the question?
- `context_recall`: Are the right chunks retrieved?

**Output**: `reports/eval.md` with table of per-question scores + aggregate.

---

## Frontend (Angular 21)

3 standalone components, router-based navigation:

| Route | Component | Key Features |
|-------|-----------|--------------|
| `/chat` | ChatComponent | Signal-based state, response display with sources + confidence |
| `/ingest` | IngestComponent | File input + text area, progress indicator, document list |
| `/logs` | LogsComponent | Paginated table, color-coded guardrail status |

HTTP calls via Angular `HttpClient` to `http://localhost:8000/api`.

---

## Gen-e2 Abstraction

```python
class AIProvider(Protocol):
    def embed(self, text: str) -> list[float]: ...
    def generate(self, prompt: str) -> str: ...

class OllamaProvider(AIProvider): ...   # default
class GenE2Provider(AIProvider): ...    # activated via AI_PROVIDER=gen-e2
```

Swap via env var. Zero code change needed for the real interview if Gen-e2 becomes accessible.
