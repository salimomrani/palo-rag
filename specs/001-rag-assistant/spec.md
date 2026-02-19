# Feature Specification: RAG Knowledge Assistant

**Feature Branch**: `001-rag-assistant`
**Created**: 2026-02-19
**Status**: Approved
**Input**: User description: "RAG Knowledge Assistant: API + Angular UI for semantic search over internal documents with guardrails, traceability and auto-evaluation"

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Ask a Question and Get a Cited Answer (Priority: P1)

A company employee types a natural language question about internal products, processes, or support topics and receives a direct, grounded answer with source document references and a confidence indicator — without needing to search through multiple documents manually.

**Why this priority**: Core value proposition. Without this, nothing else matters.

**Independent Test**: Can be fully tested by sending a question to the query endpoint and verifying the response contains an answer, at least one source reference, and a confidence score.

**Acceptance Scenarios**:

1. **Given** the corpus is ingested, **When** a user submits a question within the corpus domain, **Then** the response contains a grounded answer, 1-4 source references with similarity scores, and a confidence score between 0 and 1
2. **Given** a question outside the corpus domain, **When** submitted, **Then** the system responds with an explicit "I don't have information on this topic" message — not a hallucination
3. **Given** a valid question, **When** submitted, **Then** the response arrives within 10 seconds

---

### User Story 2 — Ingest Documents into the Knowledge Base (Priority: P1)

A knowledge manager uploads or pastes documents (Markdown or plain text) so they become immediately queryable.

**Why this priority**: Without ingestion, the query feature has no data. Co-equal P1 with querying.

**Independent Test**: Can be tested by ingesting a single document and querying for content that only exists in it, verifying the answer references it.

**Acceptance Scenarios**:

1. **Given** a Markdown or plain text document, **When** ingested via the API, **Then** the system confirms the number of chunks created and the document appears in the document list
2. **Given** an empty text body, **When** submitted for ingestion, **Then** the API returns a validation error
3. **Given** a document is ingested, **When** a question is asked about its content, **Then** that document appears in the source references

---

### User Story 3 — Inappropriate Queries Are Blocked Before Reaching the AI (Priority: P1)

A system operator wants prompt injection attacks, excessively long inputs, and empty queries to be rejected automatically before they reach the language model.

**Why this priority**: Security is non-negotiable. A RAG system without input validation is a liability.

**Independent Test**: Can be tested by submitting known attack patterns and verifying 400 responses with specific reason codes — independently of other features.

**Acceptance Scenarios**:

1. **Given** a query containing prompt injection patterns (e.g., "ignore previous instructions"), **When** submitted, **Then** the API returns HTTP 400 with reason code `guardrail:prompt_injection`
2. **Given** a query exceeding 500 characters, **When** submitted, **Then** the API returns HTTP 400 with reason code `guardrail:length_exceeded`
3. **Given** an empty query, **When** submitted, **Then** the API returns HTTP 400 with reason code `guardrail:empty_question`

---

### User Story 4 — Every Interaction Is Logged and Auditable (Priority: P1)

A compliance officer can review the complete history of queries and responses, including which documents were retrieved, quality scores, and guardrail events — with PII automatically masked.

**Why this priority**: Traceability is a core architectural principle and a key evaluation criterion for this use case.

**Independent Test**: Can be tested by submitting queries (including rejected ones) and verifying GET /api/logs returns complete log entries with masked PII.

**Acceptance Scenarios**:

1. **Given** any query (accepted or rejected), **When** processed, **Then** a log entry is created with: masked question, retrieved chunk IDs, answer, confidence score, latency, and guardrail status
2. **Given** a query containing an email address, **When** logged, **Then** the email is replaced with `[EMAIL]` in the stored log
3. **Given** GET /api/logs is called, **Then** entries are returned in reverse chronological order

---

### User Story 5 — Run Automated Quality Evaluation and Get a Report (Priority: P2)

A technical lead can trigger an automated evaluation of the RAG system against a reference question set and retrieve quality metrics without manual testing.

**Why this priority**: Quality measurement is important but the system delivers value without it. Secondary to core query/ingest/guardrail features.

**Independent Test**: Can be tested by running the evaluation endpoint and verifying a structured report file is created with metrics.

**Acceptance Scenarios**:

1. **Given** the corpus is ingested, **When** the evaluation endpoint is called, **Then** the system evaluates 15 reference Q&A pairs and returns aggregate scores for faithfulness, answer relevancy, and context recall
2. **Given** evaluation completes, **Then** a human-readable Markdown report is created at `reports/eval.md`

---

### User Story 6 — View Query History in the UI (Priority: P2)

A user or administrator can view recent query history, quality scores, and guardrail events in a dedicated UI view without accessing the API directly.

**Why this priority**: Useful for transparency and demo purposes, but secondary to core query/ingest functionality.

**Independent Test**: Can be tested independently by verifying the /logs route displays data from the logs endpoint.

**Acceptance Scenarios**:

1. **Given** the logs view is open, **When** it loads, **Then** the 20 most recent queries are displayed with question text, confidence score, latency, and guardrail status
2. **Given** a rejected query exists, **When** displayed, **Then** it is visually distinguished with the rejection reason shown

---

### Edge Cases

- What happens when the AI model is unavailable? → API returns HTTP 503 with "AI provider unavailable"
- What happens when the vector store is empty and a query is submitted? → System returns "no information available" with confidence 0.0, not an error
- What happens when ChromaDB data directory is corrupted? → API returns 500, system does not crash silently

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept document ingestion via text body and document name through a REST endpoint
- **FR-002**: Ingested documents MUST be split into chunks of approximately 500 characters with 50-character overlap
- **FR-003**: Chunks MUST be stored in a vector store with embeddings generated from a local AI model
- **FR-004**: System MUST retrieve the top-4 most semantically similar chunks for any given query
- **FR-005**: Retrieved chunks MUST be used as context in a structured prompt sent to a local language model
- **FR-006**: Every query response MUST include: answer text, source document references with similarity scores, and a confidence score
- **FR-007**: System MUST reject queries exceeding 500 characters with error code `guardrail:length_exceeded`
- **FR-008**: System MUST detect and reject prompt injection patterns with error code `guardrail:prompt_injection`
- **FR-009**: System MUST reject empty queries with error code `guardrail:empty_question`
- **FR-010**: Every query (accepted and rejected) MUST produce a log entry in persistent storage
- **FR-011**: Log entries MUST have email addresses and phone numbers replaced with placeholder tokens before storage
- **FR-012**: System MUST expose a reference evaluation dataset of 15 question/answer pairs
- **FR-013**: System MUST compute quality metrics (faithfulness, answer relevancy, context recall) when evaluation is triggered
- **FR-014**: Evaluation MUST produce a human-readable Markdown report at `reports/eval.md`
- **FR-015**: The AI provider MUST be swappable via configuration without code changes
- **FR-016**: Frontend MUST provide three views: Chat, Ingest, and Logs

### Key Entities

- **Document**: Represents an ingested source file (name, origin, chunk count, ingestion timestamp)
- **Chunk**: A segment of a document stored with its embedding in the vector store (references parent document)
- **QueryLog**: A record of one query interaction (masked question, retrieved chunks, answer, scores, latency, guardrail status)
- **EvaluationResult**: A stored outcome of one evaluation run (aggregate scores, per-question breakdown, timestamp)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All P1 user stories pass their acceptance scenarios in a live demo
- **SC-002**: Faithfulness score of 0.70 or above on the 15-question reference evaluation dataset
- **SC-003**: Answer relevancy score of 0.65 or above on the reference evaluation dataset
- **SC-004**: All guardrail test cases return the correct HTTP 400 with the correct reason code
- **SC-005**: Query response time is under 10 seconds at the 95th percentile on the local AI stack
- **SC-006**: Complete setup from clean checkout to working demo takes under 5 minutes following the README
- **SC-007**: All log entries for queries containing email addresses store `[EMAIL]` instead of the raw address

## Assumptions

- Ollama is pre-installed and running locally before the demo
- Language models are pulled into Ollama before the demo
- The corpus is a static set of 15 documents ingested before the demo
- Single-user, single-tenant use case — no authentication required
- Evaluation is a synchronous operation acceptable for a demo context

## Constraints & Dependencies

- All AI inference MUST run locally — no calls to external AI APIs
- The Gen-e2 provider MUST be mockable via an abstraction layer without code changes to the pipeline
- Backend: Python 3.12+, FastAPI, LangChain, vector store library, SQL persistence layer
- Frontend: Angular 21 with standalone components, signals, OnPush change detection
- No Docker or container runtime required for the demo environment
