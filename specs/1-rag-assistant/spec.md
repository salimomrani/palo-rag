# Spec: RAG Knowledge Assistant

**Branch**: `1-rag-assistant`
**Date**: 2026-02-19
**Status**: Approved

---

## Overview

An internal knowledge assistant that lets users query a corpus of simulated company documents (product FAQ, technical specs, support tickets) using natural language. The system retrieves relevant context, generates grounded answers, and provides full traceability of each interaction.

**User value**: Instead of searching through dozens of documents manually, a user asks a question and gets a cited, confidence-scored answer in seconds — with a full audit trail.

---

## User Scenarios & Testing

### P1 — Query the knowledge base

**As a** company employee,
**I want to** ask a question in natural language,
**So that** I get a direct answer grounded in internal documents, with source references.

**Acceptance criteria**:
- Given a question within the corpus domain, when submitted, then the response includes the answer and 2-4 source document references with similarity scores
- Given a question outside the corpus domain, when submitted, then the system responds with "I don't have enough information to answer this" (not a hallucination)
- Given a response is returned, then it arrives in under 10 seconds (local Ollama)

---

### P1 — Ingest documents

**As a** knowledge manager,
**I want to** upload or paste documents into the system,
**So that** they become queryable immediately after ingestion.

**Acceptance criteria**:
- Given a Markdown or plain text file, when ingested, then it is chunked, embedded, and stored in the vector database
- Given ingestion completes, then the document appears in the documents list
- Given a duplicate document name, then the system warns and allows overwrite or skip

---

### P1 — Input guardrails block inappropriate queries

**As a** system operator,
**I want** prompt injection and off-topic queries to be rejected before reaching the LLM,
**So that** the system cannot be manipulated or misused.

**Acceptance criteria**:
- Given a query containing prompt injection patterns (e.g., "ignore previous instructions"), when submitted, then the API returns 400 with reason "guardrail:prompt_injection"
- Given a query exceeding 500 characters, when submitted, then the API returns 400 with reason "guardrail:length_exceeded"
- Given a query with no semantic similarity to the corpus topics, when submitted, then the API returns a low-confidence response flagged as "guardrail:off_topic"

---

### P1 — Every query is logged and traceable

**As a** system auditor,
**I want** every query and response to be stored with full context,
**So that** I can review, audit, and evaluate system behaviour at any time.

**Acceptance criteria**:
- Given any query (including rejected ones), when processed, then a log entry is created with: timestamp, question (PII-masked), retrieved chunk IDs, response, faithfulness score, latency, guardrail status
- Given a log query to `GET /api/logs`, then the last 100 entries are returned in descending order
- Given a log entry, then no raw email addresses or phone numbers appear (masked to `[REDACTED]`)

---

### P2 — Automated evaluation report

**As a** technical reviewer,
**I want** to run an automated evaluation of RAG quality against a reference Q&A set,
**So that** I can measure faithfulness, relevance, and context recall objectively.

**Acceptance criteria**:
- Given `POST /api/eval/run`, when called, then RAGAS metrics are computed over a 15-question reference dataset
- Given evaluation completes, then `reports/eval.md` is updated with: per-question results, aggregate scores (faithfulness, answer_relevancy, context_recall)
- Given `GET /api/eval/report`, then the latest report is returned as JSON

---

### P2 — View logs and metrics in the UI

**As a** user,
**I want to** see recent queries and their quality scores in a dedicated view,
**So that** I can understand system performance without accessing raw logs.

**Acceptance criteria**:
- Given the logs view is open, then the last 20 queries are displayed with question, guardrail status, faithfulness score, and latency
- Given a query was rejected by a guardrail, then it appears in red with the rejection reason

---

### P3 — Output confidence flagging

**As a** user,
**I want to** see a confidence indicator on each response,
**So that** I know when to trust the answer and when to verify manually.

**Acceptance criteria**:
- Given a response with avg chunk similarity < 0.5, then it is flagged as "low confidence" in the UI
- Given a high-confidence response, then sources are shown with their similarity percentage

---

## Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-001 | The system shall accept document ingestion via file upload (Markdown, TXT) and plain text paste |
| FR-002 | Ingested documents shall be split into chunks of ~500 tokens with 50-token overlap |
| FR-003 | Chunks shall be embedded using `nomic-embed-text` via Ollama and stored in ChromaDB |
| FR-004 | Queries shall be embedded and used for cosine similarity search (top-k=4) |
| FR-005 | Retrieved chunks shall be injected into a structured prompt sent to `llama3.2` via Ollama |
| FR-006 | Each query shall pass through input guardrails before embedding |
| FR-007 | Each response shall include: answer text, source references (doc name + chunk excerpt), confidence score |
| FR-008 | All interactions (including rejections) shall be logged to a persistent SQLite store |
| FR-009 | PII (email, phone) shall be masked in logs using regex before persistence |
| FR-010 | The eval endpoint shall compute RAGAS metrics on a predefined reference dataset |
| FR-011 | The frontend shall expose three views: Chat, Ingest, Logs |
| FR-012 | The API shall expose CORS headers for localhost Angular development |

---

## Success Criteria

| ID | Criterion |
|----|-----------|
| SC-001 | P1 user stories all pass acceptance criteria in a live demo |
| SC-002 | Faithfulness score ≥ 0.70 on the reference evaluation dataset |
| SC-003 | Answer relevancy score ≥ 0.65 on the reference dataset |
| SC-004 | Query response time < 10s (P95) on local Ollama with llama3.2 |
| SC-005 | All input guardrails trigger correctly on the 5 test injection cases |
| SC-006 | `reports/eval.md` is generated automatically and readable without tooling |
| SC-007 | Setup from zero to working demo takes < 5 minutes following README |

---

## Key Entities

**Document**
- `id` (uuid), `name` (str), `source` (str), `ingested_at` (datetime), `chunk_count` (int)

**Chunk**
- `id` (uuid), `document_id` (uuid), `content` (str), `embedding` (stored in ChromaDB)

**QueryLog**
- `id` (uuid), `timestamp` (datetime), `question_masked` (str), `retrieved_chunk_ids` (list), `similarity_scores` (list), `answer` (str), `faithfulness_score` (float), `latency_ms` (int), `guardrail_triggered` (str | null)

**EvalResult**
- `run_id` (uuid), `run_at` (datetime), `faithfulness` (float), `answer_relevancy` (float), `context_recall` (float), `per_question` (list)

---

## Assumptions

- Ollama is pre-installed and running on `localhost:11434`
- Models `llama3.2` and `nomic-embed-text` are pulled before demo
- Corpus is static for the demo (no real-time document updates)
- Single-user, single-tenant (no auth required)
- ChromaDB persists to a local directory (`./chroma_data`)

---

## Constraints & Dependencies

- All AI inference must run locally (no external API calls)
- Gen-e2 is mocked via an abstraction layer (`AIProvider` interface) that can be swapped
- Backend: Python 3.11+, FastAPI, LangChain, RAGAS, ChromaDB, SQLAlchemy
- Frontend: Angular 21, standalone components, signals, OnPush
- No Docker required for the demo (local dev setup only)
