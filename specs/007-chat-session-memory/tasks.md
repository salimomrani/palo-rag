# Tasks: Chat Session Memory

**Input**: Design documents from `/specs/007-chat-session-memory/`
**Prerequisites**: plan.md ✅ spec.md ✅ research.md ✅ data-model.md ✅ contracts/ ✅

**Tests**: TDD is mandatory per CLAUDE.md — every task includes failing tests BEFORE implementation (RED → GREEN → REFACTOR).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)

---

## Phase 1: Foundational (Shared Backend Changes)

**Purpose**: Shared data model and prompt changes that all user stories depend on. No tests needed here — these are additive-only changes with no logic yet.

**⚠️ CRITICAL**: Must complete before any user story implementation begins.

- [x] T001 [P] Add `HistoryEntry(BaseModel)` with `role: Literal["user","assistant"]` and `content: str`; extend `QueryRequest` with `history: list[HistoryEntry] = []` in `backend/api/v1/query.py`
- [x] T002 [P] Add `RAG_PROMPT_WITH_HISTORY` constant (identical rules as `RAG_PROMPT`, adds `Historique :\n{history}\n\n` block before `Contexte :`) in `backend/rag/prompts.py`

**Checkpoint**: Both files compile, existing tests still pass (`cd backend && .venv/bin/pytest tests/ -v`)

---

## Phase 2: User Story 1 — Multi-turn Conversation (Priority: P1) 🎯 MVP

**Goal**: Every query sent to the assistant includes the most recent session exchanges as context, enabling coherent follow-up questions.

**Independent Test**: Ask "Quelles sont les étapes d'onboarding ?", then ask "Qui est responsable de la première étape ?" — the assistant answers using context from the first exchange without the user repeating the topic.

### Tests for User Story 1 — Write First, Ensure They FAIL ⚠️

- [x] T003 [P] [US1] Add failing test `test_query_with_history_uses_history_prompt` — verifies `provider.generate()` is called with `RAG_PROMPT_WITH_HISTORY` (contains "Historique") when `history` is non-empty in `backend/tests/test_pipeline.py`
- [x] T004 [P] [US1] Add failing test `test_stream_query_with_history_uses_history_prompt` — verifies `provider.stream_generate()` is called with history-aware prompt in `backend/tests/test_pipeline.py`
- [x] T005 [P] [US1] Add failing test `test_query_endpoint_accepts_history` — POST `/api/v1/query` with `{"question": "...", "history": [{"role": "user", "content": "Q"}, {"role": "assistant", "content": "A"}]}` returns 200 in `backend/tests/test_api.py`
- [x] T006 [P] [US1] Add failing test `test_stream_endpoint_accepts_history` — POST `/api/v1/query/stream` with history payload returns SSE stream in `backend/tests/test_api.py`

### Implementation for User Story 1 — Make Tests GREEN

- [x] T007 [US1] Add `_format_history(history: list) -> str` helper (formats entries as `"Utilisateur : {content}"` / `"Assistant : {content}"` joined with `\n`) and `_build_prompt(context, question, history) -> str` helper (returns `RAG_PROMPT_WITH_HISTORY` if history non-empty, else `RAG_PROMPT`) in `backend/rag/pipeline.py`
- [x] T008 [US1] Update `query(self, question: str, history: list = []) -> QueryResult` and `stream_query(self, question: str, history: list = []) -> Generator` to call `_build_prompt()` instead of `RAG_PROMPT.format()` directly in `backend/rag/pipeline.py` (depends on T007)
- [x] T009 [US1] Pass `history=request.history` to `RAGPipeline.query()` and `RAGPipeline.stream_query()` calls in `backend/api/v1/query.py` (depends on T001, T008)
- [x] T010 [P] [US1] Add `export interface HistoryEntry { role: 'user' | 'assistant'; content: string; }` and update `streamQuery(question: string, history: HistoryEntry[] = [])` to include `history` in request body in `frontend/src/app/services/rag-api.service.ts`
- [x] T011 [US1] In `sendMessage()`, build `history` from `this.messages()` — filter out `streaming: true` entries, take `slice(-12)` (last 6 turns), map to `{role, content}` — and pass as second arg to `this.api.streamQuery(question, history)` in `frontend/src/app/components/chat/chat.ts` (depends on T010)

**Checkpoint**: `cd backend && .venv/bin/pytest tests/ -v` — all tests green including T003-T006. Send a follow-up question in the UI and verify history appears in the network request payload.

---

## Phase 3: User Story 2 — Clear Conversation (Priority: P2)

**Goal**: The user can explicitly reset the session history without reloading the page.

**Independent Test**: After a multi-turn exchange, click "Effacer", then send a follow-up — the request body contains `history: []` and the assistant shows no memory of previous exchanges.

### Tests for User Story 2 — Write First, Ensure They FAIL ⚠️

- [x] T012 [US2] Add failing test `should clear messages signal and send empty history on next query` — tests that `clearConversation()` sets `messages` to `[]` and next `sendMessage()` passes empty history in `frontend/src/app/components/chat/chat.spec.ts`

### Implementation for User Story 2 — Make Tests GREEN

- [x] T013 [US2] Add `clearConversation(): void` method that calls `this.messages.set([])` in `frontend/src/app/components/chat/chat.ts` (depends on T012)
- [x] T014 [US2] Add "Effacer" button in `frontend/src/app/components/chat/chat.html` — visible only when `messages().length > 0`, calls `clearConversation()` (depends on T013)

**Checkpoint**: `cd frontend && npm test -- --watch=false` — T012 green. In the UI, clear button appears after first message and resets the conversation.

---

## Phase 4: User Story 3 — Long Conversation Cap (Priority: P3)

**Goal**: Conversations with more than 10 exchanges succeed without errors; only the most recent exchanges are used.

**Independent Test**: POST `/api/v1/query` with 11 history entries returns 200 (backend uses last 10); send 15+ messages in the UI — no error occurs, the 16th query succeeds normally.

### Tests for User Story 3 — Write First, Ensure They FAIL ⚠️

- [x] T015 [P] [US3] Add failing test `test_query_with_history_exceeding_cap_is_accepted` — POST `/api/v1/query` with 11 history entries returns 200 (not 422/400) in `backend/tests/test_api.py`
- [x] T016 [P] [US3] Add failing test `should send at most 12 history messages` — verifies `streamQuery` receives at most 12 entries regardless of `messages` length in `frontend/src/app/components/chat/chat.spec.ts`

### Implementation for User Story 3 — Make Tests GREEN

- [x] T017 [US3] In `RAGPipeline.query()` and `stream_query()`, truncate history to last 10 entries (`history = history[-10:]`) before calling `_build_prompt()` in `backend/rag/pipeline.py` (depends on T008)
- [x] T018 [US3] Confirm `slice(-12)` is already applied in `sendMessage()` (from T011); if not, add it explicitly in `frontend/src/app/components/chat/chat.ts`

**Checkpoint**: `cd backend && .venv/bin/pytest tests/ -v && .venv/bin/ruff check .` — all green. `cd frontend && npm test -- --watch=false && npm run lint` — all green.

---

## Phase 5: Polish & Cross-Cutting Concerns

- [x] T019 [P] Document deviation in `DECISIONS.md`: frontend default cap is 6 turns (12 messages) instead of 10 turns (20 messages) specified in spec — rationale: Qwen 2.5 7B 8k context budget
- [x] T020 [P] Run full backend validation: `cd backend && .venv/bin/pytest tests/ -v && .venv/bin/ruff check .` — confirm 0 failures, 0 lint errors
- [x] T021 [P] Run full frontend validation: `cd frontend && npm test -- --watch=false && npm run lint` — confirm 0 failures, 0 lint errors
- [x] T022 Perform manual end-to-end verification per `specs/007-chat-session-memory/quickstart.md` — multi-turn test, clear test, network payload inspection

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Foundational)**: No dependencies — start immediately; T001 and T002 are parallel
- **Phase 2 (US1)**: Depends on Phase 1 completion
  - Tests T003–T006: parallel, write immediately after Phase 1
  - T007–T009: sequential (pipeline logic → API wiring)
  - T010–T011: T010 parallel with T007, T011 depends on T010
- **Phase 3 (US2)**: Depends on Phase 2 completion; T012–T014 sequential
- **Phase 4 (US3)**: Depends on Phase 2 completion (can run in parallel with Phase 3)
- **Phase 5 (Polish)**: Depends on all user story phases

### User Story Dependencies

- **US1 (P1)**: Depends on Phase 1 — no dependencies on US2/US3
- **US2 (P2)**: Depends on US1 (clear button uses the same `messages` signal) — integrates but independently testable
- **US3 (P3)**: Depends on US1 (extends history logic) — can start after Phase 2; independent of US2

### Within Each User Story

1. Tests MUST be written and confirmed FAILING before implementation starts
2. Backend helpers (T007) before integration (T008 → T009)
3. Frontend service (T010) before component (T011)

### Parallel Opportunities

- T001 ‖ T002 (different files)
- T003 ‖ T004 ‖ T005 ‖ T006 (additive test additions, different test functions)
- T007 ‖ T010 (backend pipeline vs frontend service — different stacks)
- T015 ‖ T016 (different test files/stacks)
- T019 ‖ T020 ‖ T021 (independent validation tasks)

---

## Parallel Example: User Story 1

```bash
# Agent 1 — Backend pipeline tests (T003, T004) then implementation (T007 → T008 → T009)
# Agent 2 — Frontend service (T010) then component (T011)
# Agent 3 — Backend API tests (T005, T006) in parallel with T003/T004
```

---

## Implementation Strategy

### MVP (User Story 1 only — 11 tasks)

1. Complete Phase 1: T001, T002
2. Write failing tests: T003–T006
3. Implement: T007 → T008 → T009 (backend), T010 → T011 (frontend)
4. **STOP and VALIDATE**: multi-turn demo works, all tests green
5. Run T019–T022 polish

### Incremental Delivery

1. MVP (US1): multi-turn conversation → **demo-ready**
2. Add US2: clear button → improved UX
3. Add US3: long conversation cap → robustness edge case
4. Polish: docs + final validation

---

## Notes

- TDD is mandatory per CLAUDE.md — RED → GREEN → REFACTOR, no exceptions
- `[P]` = different files, no conflicting dependencies
- Backend tests use `MagicMock()` for provider and vectorstore (see existing `make_pipeline()` fixture)
- Frontend tests use Jasmine spies on `RagApiService`
- Run `cd backend && .venv/bin/ruff check .` after every backend change
- Never commit failing tests
