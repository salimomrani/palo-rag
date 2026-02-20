# PALO RAG — Knowledge Assistant

RAG API + Angular UI demo for Palo IT technical interview.

**Stack**: Python 3.12 · FastAPI · LangChain 0.3 · ChromaDB (embedded) · PostgreSQL 16 · Ollama · Angular 21

---

## Objective

This project demonstrates a reliable Retrieval-Augmented Generation (RAG) assistant for enterprise knowledge bases.

The goal is not to build a generic chatbot, but to explore how LLMs can be integrated into a real software system with strong engineering constraints:

- hallucination control
- traceability
- answer quality evaluation

The assistant answers from an internal documentation corpus and refuses to answer when confidence is too low.

---

## What This Project Is Not

This project is **not** a general AI assistant.

The system is intentionally constrained and only answers using retrieved documents.  
If the knowledge is not present in the corpus, the assistant must refuse.

This is a deliberate design choice: prioritize reliability over creativity.

---

## Prerequisites

- [Ollama](https://ollama.ai) running locally
- Docker (for PostgreSQL)
- Python 3.12, Node.js 22

```bash
# Pull required models once
ollama pull qwen2.5:7b
ollama pull mxbai-embed-large
```

---

## Setup (3 étapes)

```bash
# 1. Start PostgreSQL
docker-compose up -d

# 2. Start backend (first run: creates venv + installs deps)
cd backend
python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env          # uses defaults: localhost:5444, palo/palo
.venv/bin/python scripts/ingest_corpus.py   # load 15 corpus docs
.venv/bin/uvicorn main:app --reload --port 8000

# 3. Start frontend (new terminal)
cd frontend
npm install
npm start
```

Open **http://localhost:4200**

---

## API

Base URL: `http://localhost:8000/api/v1`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/query` | Ask a question (blocking) |
| `POST` | `/query/stream` | Ask a question (SSE streaming) |
| `POST` | `/ingest` | Ingest a document `{text, name}` |
| `GET` | `/documents` | List ingested documents |
| `DELETE` | `/documents/{id}` | Delete a document |
| `GET` | `/logs` | Audit log of all queries |
| `POST` | `/evaluation/run` | Run quality evaluation |
| `GET` | `/evaluation/report` | Get latest evaluation report |

Health check (outside `/api/v1`): `GET http://localhost:8000/health`

Interactive docs: **http://localhost:8000/docs**

### Example

```bash
# Ingest a document
curl -X POST http://localhost:8000/api/v1/ingest \
  -H "Content-Type: application/json" \
  -d '{"text": "PALO IT est une ESN fondée en 2009.", "name": "about.md"}'

# Ask a question
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Quand PALO IT a-t-il été fondé ?"}'

# Read logs
curl -X GET http://localhost:8000/api/v1/logs
```

Sample `GET /api/v1/logs` item:
```json
{
  "id": "24369911-0190-42bb-8b32-b069b192b3d3",
  "timestamp": "2026-02-20T14:23:33.856095",
  "question_masked": "Que dit smoke.md ?",
  "retrieved_sources": ["faq-onboarding.md", "spec-webhooks.md"],
  "similarity_scores": [0.455, 0.441],
  "answer": "Je n'ai pas d'information sur ce sujet dans la base de connaissance.",
  "faithfulness_score": 0.443,
  "latency_ms": 14263,
  "guardrail_triggered": null,
  "rejected": false,
  "rejection_reason": null
}
```

---

## Tests

```bash
cd backend
.venv/bin/pytest tests/ -v
```

Expected: **30 passed**

## Lint (Frontend)

```bash
cd frontend
npm run lint
```

Expected: **0 errors** (1 warning: `ViewChild` non-null assertion — documented in DECISIONS.md)

---

## Quality Evaluation

```bash
curl -X POST http://localhost:8000/api/v1/evaluation/run
# Report saved to reports/eval.md
```

---

## Architecture (quick view)

```text
[Angular UI]
   -> /api/v1 (FastAPI)
      -> Guardrails (input checks)
      -> RAG pipeline (retrieve + generate)
         -> Chroma (vector store, local disk)
         -> Ollama (LLM + embeddings)
      -> PostgreSQL (documents, query logs, evaluation results)
```

Detailed architecture: see `ARCHITECTURE.md`.

---

## How It Works

### 1) Ingestion flow
- User uploads a `.md` file from the UI (`/ingest`)
- Backend splits text into chunks (`500` chars, overlap `50`)
- Chunks are embedded and stored in Chroma
- Document metadata is saved in PostgreSQL (`documents`)

### 2) Query flow (RAG)
- User asks a question (`/query` or `/query/stream`)
- Guardrails validate input (empty, too long, injection-like, offensive)
- Top-`k=4` chunks are retrieved from Chroma
- If retrieval confidence is too low (default: `< 0.3`), fallback answer is returned
- Otherwise, Ollama generates the final answer from retrieved context

### 3) Traceability & quality
- Each query is logged in PostgreSQL (`query_logs`) with masked question, confidence, latency, and guardrail status
- Evaluation suite can be run via `/evaluation/run`
- Latest report is available via `/evaluation/report` and `reports/eval.md`

---

## Technical Choices & Trade-offs

- **FastAPI + Angular**: fast to implement and demo, good separation front/back
- **Ollama local**: no external API dependency for the interview, reproducible offline-like setup
- **Chroma embedded**: lightweight and simple for a small corpus
- **PostgreSQL for logs/eval**: structured persistence and easy querying
- **Trade-off**: optimized for demo speed and clarity, not yet production-grade operations

---

## Storage Strategy

The project intentionally separates storage responsibilities:

- **ChromaDB** stores vector embeddings for semantic retrieval
- **PostgreSQL** stores business data (document metadata, audit logs, evaluation results)

A vector store does not replace a transactional database; it complements it.

---

## Hallucination Handling

The assistant never answers blindly.

If semantic retrieval confidence is below a threshold (default `0.3`), the system returns a refusal response instead of generating an answer.
The threshold can be overridden via `.env` with `MIN_RETRIEVAL_SCORE`.

This is a deliberate design decision to reduce hallucinations and favor correctness over completeness.

---

## Security & Guardrails

Implemented:
- input guardrails (`empty`, `max length`, prompt-injection patterns, offensive content)
- PII masking in logs (`email`, `phone`)
- CORS restricted to frontend dev origin (`http://localhost:4200`)

Not implemented yet (production scope):
- authentication/authorization
- rate limiting
- secrets manager / key rotation
- stricter audit and retention policies

---

## Observability

- App logs: backend structured logs (`backend/core/logging.py`)
- Query audit: `GET /api/v1/logs`
- Evaluation report: `GET /api/v1/evaluation/report`
- Markdown report output: `reports/eval.md`

---

## Limitations & Next Steps

- Add authentication on ingest/delete/log/eval endpoints
- Add migration tooling (Alembic) for schema evolution
- Improve retrieval quality metrics and threshold calibration
- Add request tracing + metrics dashboard (latency, errors, guardrail hit rate)
- Support pluggable providers (Gen-e2 integration path in `provider.py`)

---

## Project Structure

```
PALO/
├── backend/
│   ├── api/v1/          # FastAPI routers (query, ingest, logs, evaluation)
│   ├── rag/             # Pipeline, provider (Ollama), ingestion
│   ├── guardrails/      # Input validation (injection, length, offensive)
│   ├── logging_service/ # PII masking + audit log store
│   ├── quality/         # Reference dataset, runner, report generator
│   ├── models/          # SQLAlchemy models
│   └── tests/           # 30 tests (TDD)
├── frontend/
│   └── src/app/
│       ├── components/  # Chat, Ingest, Logs (Angular 21 signals)
│       └── services/    # RagApiService
├── corpus/              # 15 synthetic Markdown knowledge base docs
├── specs/               # speckit: spec.md, plan.md, tasks.md
├── reports/             # eval.md, costs.md
└── docker-compose.yml   # PostgreSQL 16
```
