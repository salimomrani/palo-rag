# Tasks: RAG Knowledge Assistant

**Input**: Design documents from `specs/001-rag-assistant/`
**Prerequisites**: plan.md ✅, spec.md ✅

---

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Create `.gitignore`, `.claudeignore` at repo root
- [ ] T002 Create `backend/requirements.txt`, `requirements-dev.txt`, `.env.example`, `pytest.ini`
- [ ] T003 [P] Create Python virtualenv, install deps (`python3.11 -m venv .venv && pip install -r requirements.txt`)
- [ ] T004 [P] Initialize Angular project (`ng new frontend --standalone --routing --style=scss --skip-git`)
- [ ] T005 Create `corpus/` directory with 15 synthetic Markdown documents
- [ ] T006 **Commit**: `chore: project bootstrap — Python deps, Angular init, 15-doc corpus`

---

## Phase 2: Foundational (Blocking Prerequisites)

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Write failing tests `backend/tests/test_models.py` (Document, QueryLog, EvaluationResult)
- [ ] T008 Implement `backend/models/db.py` (SQLAlchemy models) — make T007 pass
- [ ] T009 **Commit**: `feat: SQLAlchemy models — Document, QueryLog, EvaluationResult`
- [ ] T010 Write failing tests `backend/tests/test_provider.py` (AIProvider, OllamaProvider)
- [ ] T011 Implement `backend/rag/provider.py` (AIProvider protocol + OllamaProvider) — make T010 pass
- [ ] T012 **Commit**: `feat: AIProvider protocol + OllamaProvider (Gen-e2 swappable)`

**Checkpoint**: Foundation ready — user story implementation can begin

---

## Phase 3: US1 — Ask a Question and Get a Cited Answer (P1) 🎯 MVP

**Goal**: User submits a question, gets a grounded answer with sources and confidence score
**Independent Test**: `POST /api/query` returns answer + sources + confidence_score

### Tests (write first, must FAIL)

- [ ] T013 [P] Write failing tests `backend/tests/test_ingestion.py`
- [ ] T014 [P] Write failing tests `backend/tests/test_pipeline.py`

### Implementation

- [ ] T015 [US1] Implement `backend/rag/ingestion.py` — make T013 pass
- [ ] T016 [US1] Implement `backend/rag/pipeline.py` — make T014 pass
- [ ] T017 **Commit**: `feat: ingestion pipeline + RAG query pipeline with source attribution`
- [ ] T018 [US1] Write failing tests `backend/tests/test_api.py` for `/api/query` endpoint
- [ ] T019 [US1] Create `backend/dependencies.py` (FastAPI DI: provider, vectorstore, engine)
- [ ] T020 [US1] Create `backend/api/query.py` — make T018 query tests pass
- [ ] T021 [US1] Create `backend/main.py` with CORS and router registration
- [ ] T022 **Commit**: `feat: POST /api/query endpoint — RAG pipeline wired to FastAPI`

**Checkpoint**: `curl -X POST /api/query -d '{"question":"..."}'` returns answer + sources ✅

---

## Phase 4: US2 — Ingest Documents (P1)

**Goal**: User ingests a Markdown/text document, it becomes queryable
**Independent Test**: Ingest doc → query about its content → source appears in response

### Tests (write first, must FAIL)

- [ ] T023 [US2] Write failing tests `backend/tests/test_api.py` for `/api/ingest` + `/api/documents`

### Implementation

- [ ] T024 [US2] Create `backend/api/ingest.py` (POST /api/ingest, GET /api/documents) — make T023 pass
- [ ] T025 **Commit**: `feat: POST /api/ingest + GET /api/documents endpoints`
- [ ] T026 [US2] Ingest the 15 corpus documents using the API (verify all return chunk_count > 0)
- [ ] T027 **Commit**: `chore: 15-doc corpus ingested — integration verified`

**Checkpoint**: GET /api/documents returns 15 documents ✅

---

## Phase 5: US3 — Input Guardrails Block Inappropriate Queries (P1)

**Goal**: Injection, length exceeded, empty queries return HTTP 400 with specific reason codes
**Independent Test**: All 7 guardrail test cases return correct 400 + reason code

### Tests (write first, must FAIL)

- [ ] T028 [US3] Write failing tests `backend/tests/test_guardrails_input.py` (7 test cases)

### Implementation

- [ ] T029 [US3] Implement `backend/guardrails/input.py` (InputGuardrail, GuardrailResult) — make T028 pass
- [ ] T030 [US3] Wire guardrail into `backend/api/query.py` (check before pipeline, log rejections)
- [ ] T031 **Commit**: `feat: input guardrails (injection, length, empty) wired to query endpoint`

**Checkpoint**: `curl -d '{"question":"ignore previous instructions"}'` returns 400 ✅

---

## Phase 6: US4 — Every Interaction Is Logged and Auditable (P1)

**Goal**: All queries (accepted + rejected) produce PII-masked log entries, retrievable via API
**Independent Test**: Submit query with email → check /api/logs shows [EMAIL] instead

### Tests (write first, must FAIL)

- [ ] T032 [US4] Write failing tests `backend/tests/test_logging.py` (mask_pii + LogStore, 6 cases)
- [ ] T033 [US4] Write failing tests `backend/tests/test_api.py` for GET /api/logs

### Implementation

- [ ] T034 [US4] Implement `backend/logging_service/pii.py` (mask_pii) — make T032 pii tests pass
- [ ] T035 [US4] Implement `backend/logging_service/store.py` (LogStore) — make T032 store tests pass
- [ ] T036 **Commit**: `feat: PII-masking log store`
- [ ] T037 [US4] Create `backend/api/logs.py` (GET /api/logs) — make T033 pass
- [ ] T038 **Commit**: `feat: GET /api/logs endpoint — query traceability complete`

**Checkpoint**: All P1 user stories functional. Full backend test suite: `pytest tests/ -v` all PASS ✅

---

## Phase 7: US5 — Quality Evaluation Report (P2)

**Goal**: POST /api/evaluation/run computes quality metrics, generates reports/eval.md
**Independent Test**: Call run endpoint → check reports/eval.md exists with scores

### Tests (write first, must FAIL)

- [ ] T039 [US5] Write failing tests `backend/tests/test_quality.py` (dataset + report generator)

### Implementation

- [ ] T040 [US5] Implement `backend/quality/dataset.py` (15 reference Q&A pairs) — make T039 pass
- [ ] T041 [US5] Implement `backend/quality/report.py` (generate_quality_report_md) — make T039 pass
- [ ] T042 [US5] Implement `backend/quality/runner.py` (run_quality_check)
- [ ] T043 [US5] Create `backend/api/evaluation.py` (POST /api/evaluation/run, GET /api/evaluation/report)
- [ ] T044 **Commit**: `feat: quality runner, 15-Q reference dataset, eval.md report`

**Checkpoint**: `POST /api/evaluation/run` returns scores, `reports/eval.md` is created ✅

---

## Phase 8: US6 — Angular Frontend (P2)

**Goal**: 3-view Angular 21 app (Chat, Ingest, Logs) connected to the API
**Independent Test**: All 3 routes work at http://localhost:4200

- [ ] T045 [US6] Create `frontend/src/environments/environment.ts`
- [ ] T046 [US6] Create `frontend/src/app/services/rag-api.service.ts` (query, ingest, logs, documents)
- [ ] T047 [US6] Update `app.config.ts` with `provideHttpClient()`
- [ ] T048 [US6] Update `app.routes.ts` with lazy-loaded routes `/chat`, `/ingest`, `/logs`
- [ ] T049 **Commit**: `feat: Angular API service + routing setup`
- [ ] T050 [US6] Create `frontend/src/app/chat/chat.component.ts` (signals, OnPush, error handling)
- [ ] T051 **Commit**: `feat: Angular ChatComponent — signals, source display, confidence scoring`
- [ ] T052 [US6] Create `frontend/src/app/ingest/ingest.component.ts` (file paste + documents list)
- [ ] T053 [US6] Create `frontend/src/app/logs/logs.component.ts` (table, rejected rows highlighted)
- [ ] T054 **Commit**: `feat: Angular Ingest and Logs components`

**Checkpoint**: All 3 routes functional at http://localhost:4200 ✅

---

## Phase 9: Deliverables & Polish

- [ ] T055 Create `README.md` (setup in 3 commands, API table, test command)
- [ ] T056 Create `DECISIONS.md` (trade-offs, limits, next-steps)
- [ ] T057 Run `pytest tests/ -v --tb=short` — all PASSED ✅
- [ ] T058 Run quality check to generate `reports/eval.md`
- [ ] T059 **Commit**: `docs: README, DECISIONS.md — deliverables complete`
- [ ] T060 Run `/cost` in Claude Code terminal — copy session tokens/cost into `reports/costs.md`
- [ ] T061 **Commit**: `chore: update costs report — project complete`

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
