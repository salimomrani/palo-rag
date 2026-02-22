# Tasks: RAG Knowledge Assistant

**Input**: Design documents from `specs/001-rag-assistant/`
**Prerequisites**: plan.md ✅, spec.md ✅

---

## Phase 1: Setup (Shared Infrastructure)

- [x] T001 Create `.gitignore`, `.claudeignore` at repo root
- [x] T002 Create `backend/requirements.txt`, `requirements-dev.txt`, `.env.example`, `pytest.ini`
- [x] T003 [P] Create Python virtualenv, install deps (python3.12 used — 3.11 unavailable, SQLAlchemy pinned to 2.0.35)
- [x] T004 [P] Initialize Angular project (`ng new frontend --standalone --routing --style=scss --skip-git --no-ssr`)
- [x] T005 Create `corpus/` directory with 15 synthetic Markdown documents
- [x] T006 **Commit**: `chore: project bootstrap — Python deps, Angular init, 15-doc corpus`

---

## Phase 2: Foundational (Blocking Prerequisites)

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Write failing tests `backend/tests/test_models.py` (Document, QueryLog, EvaluationResult)
- [x] T008 Implement `backend/models/db.py` (SQLAlchemy models) — make T007 pass
- [x] T009 **Commit**: `feat: SQLAlchemy models — Document, QueryLog, EvaluationResult`
- [x] T010 Write failing tests `backend/tests/test_provider.py` (AIProvider, OllamaProvider)
- [x] T011 Implement `backend/rag/provider.py` (AIProvider protocol + OllamaProvider) — make T010 pass
- [x] T012 **Commit**: `feat: AIProvider protocol + OllamaProvider (Gen-e2 swappable)`

**Checkpoint**: Foundation ready — user story implementation can begin

---

## Phase 3: US1 — Ask a Question and Get a Cited Answer (P1) 🎯 MVP

**Goal**: User submits a question, gets a grounded answer with sources and confidence score
**Independent Test**: `POST /api/query` returns answer + sources + confidence_score

### Tests (write first, must FAIL)

- [x] T013 [P] Write failing tests `backend/tests/test_ingestion.py`
- [x] T014 [P] Write failing tests `backend/tests/test_pipeline.py`

### Implementation

- [x] T015 [US1] Implement `backend/rag/ingestion.py` — make T013 pass
- [x] T016 [US1] Implement `backend/rag/pipeline.py` — make T014 pass
- [x] T017 **Commit**: `feat: ingestion pipeline + RAG query pipeline with source attribution`
- [x] T018 [US1] Write failing tests `backend/tests/test_api.py` for `/api/query` endpoint
- [x] T019 [US1] Create `backend/dependencies.py` (FastAPI DI: provider, vectorstore, engine)
- [x] T020 [US1] Create `backend/api/query.py` — make T018 query tests pass
- [x] T021 [US1] Create `backend/main.py` with CORS and router registration
- [x] T022 **Commit**: `feat: POST /api/query endpoint — RAG pipeline wired to FastAPI`

**Checkpoint**: `curl -X POST /api/query -d '{"question":"..."}'` returns answer + sources ✅

---

## Phase 4: US2 — Ingest Documents (P1)

**Goal**: User ingests a Markdown/text document, it becomes queryable
**Independent Test**: Ingest doc → query about its content → source appears in response

### Tests (write first, must FAIL)

- [x] T023 [US2] Write failing tests `backend/tests/test_api.py` for `/api/ingest` + `/api/documents`

### Implementation

- [x] T024 [US2] Create `backend/api/ingest.py` (POST /api/ingest, GET /api/documents) — make T023 pass
- [x] T025 **Commit**: `feat: POST /api/ingest + GET /api/documents endpoints`
- [x] T026 [US2] Create `backend/scripts/ingest_corpus.py` to bulk-ingest 15 corpus docs
- [x] T027 **Commit**: `feat(scripts): ingest_corpus.py + 9/9 API tests passing`

**Checkpoint**: GET /api/documents returns 15 documents ✅

---

## Phase 5: US3 — Input Guardrails Block Inappropriate Queries (P1)

**Goal**: Injection, length exceeded, empty queries return HTTP 400 with specific reason codes
**Independent Test**: All 7 guardrail test cases return correct 400 + reason code

### Tests (write first, must FAIL)

- [x] T028 [US3] Write failing tests `backend/tests/test_api.py` for guardrail cases (injection, length)

### Implementation

- [x] T029 [US3] Implement `backend/guardrails/input.py` (InputGuardrail, GuardrailResult) — make T028 pass
- [x] T030 [US3] Wire guardrail into `backend/api/v1/query.py` (check before pipeline, log rejections)
- [x] T031 **Commit**: `feat: input guardrails (injection, length) wired to query endpoint`

**Checkpoint**: `curl -d '{"question":"ignore previous instructions"}'` returns 400 ✅

---

## Phase 6: US4 — Every Interaction Is Logged and Auditable (P1)

**Goal**: All queries (accepted + rejected) produce PII-masked log entries, retrievable via API
**Independent Test**: Submit query with email → check /api/logs shows [EMAIL] instead

### Tests (write first, must FAIL)

- [x] T032 [US4] Write tests `backend/tests/test_api.py` for GET /api/logs
- [x] T033 [US4] (merged with T032)

### Implementation

- [x] T034 [US4] Implement `backend/logging_service/pii.py` (mask_pii)
- [x] T035 [US4] Implement `backend/logging_service/store.py` (LogStore)
- [x] T036 **Commit**: `feat: PII-masking log store`
- [x] T037 [US4] Create `backend/api/v1/logs.py` (GET /api/logs)
- [x] T038 **Commit**: `feat: GET /api/logs endpoint — query traceability complete`

**Checkpoint**: All P1 user stories functional. Full backend test suite: `pytest tests/ -v` all PASS ✅

---

## Phase 7: US5 — Quality Evaluation Report (P2)

**Goal**: POST /api/evaluation/run computes quality metrics, generates reports/eval.md
**Independent Test**: Call run endpoint → check reports/eval.md exists with scores

### Tests (write first, must FAIL)

- [x] T039 [US5] Write failing tests `backend/tests/test_quality.py` (dataset + report generator)

### Implementation

- [x] T040 [US5] Implement `backend/quality/dataset.py` (15 reference Q&A pairs) — make T039 pass
- [x] T041 [US5] Implement `backend/quality/report.py` (generate_quality_report_md) — make T039 pass
- [x] T042 [US5] Implement `backend/quality/runner.py` (run_quality_check)
- [x] T043 [US5] Create `backend/api/evaluation.py` (POST /api/evaluation/run, GET /api/evaluation/report)
- [x] T044 **Commit**: `feat: quality runner, 15-Q reference dataset, eval.md report`

**Checkpoint**: `POST /api/evaluation/run` returns scores, `reports/eval.md` is created ✅

---

## Phase 8: US6 — Angular Frontend (P2)

**Goal**: 3-view Angular 21 app (Chat, Ingest, Logs) connected to the API
**Independent Test**: All 3 routes work at http://localhost:4200

- [x] T045 [US6] Create `frontend/src/environments/environment.ts`
- [x] T046 [US6] Create `frontend/src/app/services/rag-api.service.ts` (query, ingest, logs, documents)
- [x] T047 [US6] Update `app.config.ts` with `provideHttpClient()`
- [x] T048 [US6] Update `app.routes.ts` with lazy-loaded routes `/chat`, `/ingest`, `/logs`
- [x] T049 **Commit**: `feat: Angular API service + routing setup`
- [x] T050 [US6] Create `frontend/src/app/chat/chat.component.ts` (signals, OnPush, error handling)
- [x] T051 **Commit**: `feat: Angular ChatComponent — signals, source display, confidence scoring`
- [x] T052 [US6] Create `frontend/src/app/ingest/ingest.component.ts` (file paste + documents list)
- [x] T053 [US6] Create `frontend/src/app/logs/logs.component.ts` (table, rejected rows highlighted)
- [x] T054 **Commit**: `feat: Angular Ingest and Logs components`

**Checkpoint**: All 3 routes functional at http://localhost:4200 ✅

---

## Phase 8b: Streaming + Document Management (post-demo additions)

- [x] T062 [US1] Add `stream_generate()` to `OllamaProvider` via `ChatOllama.stream()`
- [x] T063 [US1] Add `stream_query()` SSE generator to `RAGPipeline` (meta→tokens→done events)
- [x] T064 [US1] Create `POST /api/v1/query/stream` endpoint with `StreamingResponse` + post-stream logging
- [x] T065 [US2] Add `DELETE /api/v1/documents/{id}` endpoint (removes from DB + ChromaDB by source filter)
- [x] T066 [US2] Block duplicate ingestion: return HTTP 409 if document name already exists
- [x] T067 [US6] Update `RagApiService`: `streamQuery()` using native fetch + ReadableStream SSE parser
- [x] T068 [US6] Update `ChatComponent`: streaming by message ID, blinking cursor during generation
- [x] T069 [US6] Update `IngestComponent`: delete button per document with confirmation dialog
- [x] T070 **Commit**: `feat: streaming SSE + document delete + duplicate guard`

**Checkpoint**: Chat streams token by token, ingest blocks duplicates, delete removes from KB ✅

---

## Phase 9: Deliverables & Polish

- [x] T055 Create `README.md` (setup in 3 commands, API table, test command)
- [x] T056 Create `DECISIONS.md` (trade-offs, limits, next-steps)
- [x] T057 Run `pytest tests/ -v --tb=short` — all PASSED ✅
- [x] T058 Run quality check to generate `reports/eval.md`
- [x] T059 **Commit**: `docs: README, DECISIONS.md — deliverables complete`
- [x] T060 Run `/cost` in Claude Code terminal — copy session tokens/cost into `reports/costs.md`
- [x] T061 **Commit**: `chore: update costs report — project complete`

---

## Dependencies & Execution Order

- **Phase 1** (Setup): No deps, start immediately
- **Phase 2** (Foundation): Depends on Phase 1 — BLOCKS all user stories
- **Phases 3-6** (P1 stories): Sequential (query → ingest → guardrails → logging). Each depends on Phase 2.
- **Phase 7** (Evaluation): Depends on Phase 3 (needs pipeline)
- **Phase 8** (Frontend): Can start after Phase 2 (service + routing) but full testing requires Phase 3-6
- **Phase 9** (Deliverables): Depends on all previous phases

### Parallel Opportunities

- T003 (Python install) and T004 (Angular init) can run in parallel
- T013 and T014 (write failing tests for ingestion + pipeline) can run in parallel
- T032 and T033 (write failing tests for logging + logs API) can run in parallel
- T050, T052, T053 (Angular components) can run in parallel once T048 is done

## Notes

- [P] = can run in parallel (different files, no shared state)
- Tests marked must be written FIRST and verified to FAIL before implementation
- Each Phase ends with a Commit — clean git history as required
- Each P1 Phase ends with a Checkpoint — verify before moving to next story
