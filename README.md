# PALO RAG — Knowledge Assistant

RAG API + Angular UI demo for Palo IT technical interview.

**Stack**: Python 3.12 · FastAPI · LangChain 0.3 · ChromaDB (embedded) · PostgreSQL 16 · Ollama · Angular 21

---

## Prerequisites

- [Ollama](https://ollama.ai) running locally
- Docker (for PostgreSQL)
- Python 3.12, Node.js 22

```bash
# Pull required models once
ollama pull llama3.2
ollama pull nomic-embed-text
```

---

## Setup (3 commands)

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
| `GET` | `/health` | Health check |
| `POST` | `/query` | Ask a question (blocking) |
| `POST` | `/query/stream` | Ask a question (SSE streaming) |
| `POST` | `/ingest` | Ingest a document `{text, name}` |
| `GET` | `/documents` | List ingested documents |
| `DELETE` | `/documents/{id}` | Delete a document |
| `GET` | `/logs` | Audit log of all queries |
| `POST` | `/evaluation/run` | Run quality evaluation |
| `GET` | `/evaluation/report` | Get latest evaluation report |

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
```

---

## Tests

```bash
cd backend
.venv/bin/pytest tests/ -v
```

Expected: **26 passed**

---

## Quality Evaluation

```bash
curl -X POST http://localhost:8000/api/v1/evaluation/run
# Report saved to reports/eval.md
```

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
│   └── tests/           # 26 tests (TDD)
├── frontend/
│   └── src/app/
│       ├── components/  # Chat, Ingest, Logs (Angular 21 signals)
│       └── services/    # RagApiService
├── corpus/              # 15 synthetic Markdown knowledge base docs
├── specs/               # speckit: spec.md, plan.md, tasks.md
├── reports/             # eval.md, costs.md
└── docker-compose.yml   # PostgreSQL 16
```
