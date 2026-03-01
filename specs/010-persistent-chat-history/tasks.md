# Tasks: Persistent Chat History

**Input**: Design documents from `/specs/010-persistent-chat-history/`
**Prerequisites**: plan.md ✅ spec.md ✅ research.md ✅ data-model.md ✅ contracts/ ✅

**Tests**: TDD is mandatory per CLAUDE.md — every task includes failing tests BEFORE implementation (RED → GREEN → REFACTOR).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)

---

## Phase 1: Foundational (Shared Backend Changes)

**Purpose**: Schema change + data layer wiring that ALL user stories depend on. These are additive-only changes. Existing tests must still pass at the end of this phase.

**⚠️ CRITICAL**: Must complete before any user story implementation begins.

- [x] T001 Add `session_id: Mapped[str | None]` (nullable, indexed) field to `QueryLog` in `backend/models/db.py`
- [x] T002 [P] Add idempotent startup DDL migration (`ALTER TABLE query_logs ADD COLUMN IF NOT EXISTS session_id VARCHAR; CREATE INDEX IF NOT EXISTS ix_query_logs_session_id ON query_logs(session_id);`) inside `get_engine()` in `backend/dependencies.py`
- [x] T003 [P] Add `session_id: str | None = None` parameter to `LogStore.save()` and pass it to `QueryLog(...)` constructor in `backend/logging_service/store.py`
- [x] T004 Add `session_id: str | None = None` field to `QueryRequest` in `backend/api/v1/query.py` and pass `session_id=request.session_id` to both `log_store.save()` calls (query and stream handlers)

**Checkpoint**: `cd backend && .venv/bin/pytest tests/ -v` — all existing tests still green. No new behavior yet.

---

## Phase 2: User Story 1 — View Past Conversations After Page Reload (Priority: P1) 🎯 MVP

**Goal**: After a page reload, the user can open a history panel and see their past conversations, then click one to read all its exchanges.

**Independent Test**: Ask 2 questions, reload the page, click "Historique", verify the session appears with 2 exchanges visible.

### Tests for User Story 1 — Write First, Ensure They FAIL ⚠️

- [x] T005 [P] [US1] Add failing test `test_query_endpoint_persists_session_id` — POST `/api/v1/query/stream` with `session_id` verifies DB row has that `session_id` in `backend/tests/test_api.py`
- [x] T006 [P] [US1] Add failing test `test_query_without_session_id_still_works` — POST without `session_id` returns 200, backward compatibility in `backend/tests/test_api.py`
- [x] T007 [P] [US1] Add failing test `test_get_history_empty` — `GET /api/v1/history` returns `[]` when no sessions exist in `backend/tests/test_api.py`
- [x] T008 [P] [US1] Add failing test `test_get_history_returns_session_summary` — after saving 2 logs with same `session_id`, `GET /api/v1/history` returns 1 summary with correct `session_id`, `started_at`, `first_question`, `exchange_count=2` in `backend/tests/test_api.py`
- [x] T009 [P] [US1] Add failing test `test_get_conversation_detail` — `GET /api/v1/history/{session_id}` returns `session_id` + ordered `exchanges` list in `backend/tests/test_api.py`
- [x] T010 [P] [US1] Add failing test `test_get_conversation_not_found` — `GET /api/v1/history/unknown-uuid` returns 404 in `backend/tests/test_api.py`

### Implementation for User Story 1 — Make Tests GREEN

- [x] T011 [US1] Create `backend/api/v1/history.py` with `GET /history` router (group `query_logs` by `session_id` WHERE `session_id IS NOT NULL`, return summaries ordered by `MIN(timestamp) DESC`, limit/offset support) (depends on T001, T003)
- [x] T012 [US1] Add `GET /history/{session_id}` to `backend/api/v1/history.py` — return all rows for that session ordered by `timestamp ASC`; raise 404 if no rows found (depends on T011)
- [x] T013 [US1] Register `history_router` from `backend/api/v1/history.py` in `backend/api/__init__.py`
- [x] T014 [P] [US1] Add `ConversationSummary`, `ConversationExchange`, `ConversationDetail` TypeScript interfaces and `getHistory(limit?, offset?)`, `getConversation(sessionId)` HTTP methods to `frontend/src/app/services/rag-api.service.ts` (parallel — different file from backend)
- [x] T015 [P] [US1] Add failing tests for `ConversationService` — `should generate sessionId at construction`, `should reuse sessionId from sessionStorage`, `should call getHistory on loadHistory()`, `should call getConversation on loadConversation()` in `frontend/src/app/services/conversation.service.spec.ts`
- [x] T016 [US1] Create `frontend/src/app/services/conversation.service.ts` with: `sessionId` (read from `sessionStorage['palo_session_id']` or `crypto.randomUUID()` then store), `historyOpen = signal(false)`, `conversations = signal<ConversationSummary[]>([])`, `selectedConversation = signal<ConversationDetail | null>(null)`, `loadHistory()`, `loadConversation(id)`, `toggleHistory()` (depends on T014, T015)
- [x] T017 [US1] Add failing test `should pass sessionId to streamQuery in sendMessage()` in `frontend/src/app/components/chat/chat.spec.ts`
- [x] T018 [US1] Inject `ConversationService` into `Chat` in `frontend/src/app/components/chat/chat.ts`; update `sendMessage()` to pass `session_id: this.conversationService.sessionId` as third arg to `api.streamQuery()`; update `streamQuery` signature in `rag-api.service.ts` to accept optional `session_id` param in the POST body (depends on T016, T017)
- [x] T019 [US1] Create `frontend/src/app/components/chat/history-panel/history-panel.ts` — standalone component, inject `ConversationService`, expose list/detail views via signal, call `loadHistory()` on open (depends on T016)
- [x] T020 [US1] Create `frontend/src/app/components/chat/history-panel/history-panel.html` — list view: `@for` over `conversations()`, summary card with `started_at` + `first_question` + `exchange_count`; detail view: `@if selectedConversation()` with exchange list (question + answer pairs); empty state message when no conversations (depends on T019)
- [x] T021 [US1] Create `frontend/src/app/components/chat/history-panel/history-panel.scss` — slide-in left drawer, `.history-panel` with `transform: translateX(-100%)` when closed / `translateX(0)` when open, `.history-overlay` backdrop (depends on T019)
- [x] T022 [US1] Add "Historique" toggle button to `frontend/src/app/components/chat/chat.html` that calls `conversationService.toggleHistory()` and include `<app-history-panel>` with slide-in conditional class; add overlay backdrop styles to `frontend/src/app/components/chat/chat.scss` (depends on T019, T020, T021)

**Checkpoint**: `cd backend && .venv/bin/pytest tests/ -v && .venv/bin/ruff check .` — T005–T010 all green. `cd frontend && npm test -- --watch=false` — T015, T017 green. Send 2 queries, reload, open history panel, see previous session with both exchanges.

---

## Phase 3: User Story 2 — Conversations Grouped Automatically by Session (Priority: P2)

**Goal**: Queries from the same browser session appear as one conversation; a page reload starts a new group. No explicit save action required.

**Independent Test**: Send 3 questions in Tab A, reload, send 2 more — history shows exactly 2 conversations, not 5 individual entries.

### Tests for User Story 2 — Write First, Ensure They FAIL ⚠️

- [x] T023 [P] [US2] Add failing test `test_get_history_groups_multiple_queries_same_session` — save 3 logs with same `session_id` → `GET /history` returns 1 entry with `exchange_count=3` in `backend/tests/test_api.py`
- [x] T024 [P] [US2] Add failing test `test_get_history_separates_different_sessions` — save 2 logs with session A + 1 log with session B → `GET /history` returns 2 entries in `backend/tests/test_api.py`
- [x] T025 [P] [US2] Add failing test `test_get_history_ordered_most_recent_first` — session B started after session A → session B appears first in list in `backend/tests/test_api.py`
- [x] T026 [P] [US2] Add failing frontend test `should show current session in history list` — after `sendMessage()`, `loadHistory()` is called and current session appears in `conversations()` signal in `frontend/src/app/components/chat/chat.spec.ts`

### Implementation for User Story 2 — Make Tests GREEN

- [x] T027 [US2] Verify grouping SQL in `GET /history` handler in `backend/api/v1/history.py` sorts by `MIN(timestamp) DESC` per session — adjust if T023/T024/T025 reveal bugs (depends on T011, T023–T025)
- [x] T028 [US2] Call `conversationService.loadHistory()` after each successful `sendMessage()` completion in `frontend/src/app/components/chat/chat.ts` so the in-progress session appears in the panel (depends on T018, T026)

**Checkpoint**: `cd backend && .venv/bin/pytest tests/ -v` — T023–T025 green. Open 2 browser tabs, make queries in each, open history panel — exactly 2 conversation groups appear.

---

## Phase 4: User Story 3 — Delete a Past Conversation (Priority: P3)

**Goal**: The user can permanently delete any conversation from the history panel after a confirmation step.

**Independent Test**: Create 2 conversations, delete one, reload — only 1 remains in history.

### Tests for User Story 3 — Write First, Ensure They FAIL ⚠️

- [x] T029 [P] [US3] Add failing test `test_delete_conversation_returns_204` — `DELETE /api/v1/history/{session_id}` with existing session returns 204 and rows are gone in `backend/tests/test_api.py`
- [x] T030 [P] [US3] Add failing test `test_delete_conversation_not_found` — `DELETE /api/v1/history/unknown-uuid` returns 404 in `backend/tests/test_api.py`
- [x] T031 [P] [US3] Add failing frontend test `should call deleteConversation and remove from conversations signal` in `frontend/src/app/services/conversation.service.spec.ts`

### Implementation for User Story 3 — Make Tests GREEN

- [x] T032 [US3] Add `DELETE /history/{session_id}` endpoint to `backend/api/v1/history.py` — delete all `query_logs` rows with matching `session_id`; return 204; raise 404 if none found (depends on T011, T029, T030)
- [x] T033 [P] [US3] Add `deleteConversation(sessionId)` HTTP method to `frontend/src/app/services/rag-api.service.ts` — `DELETE /api/v1/history/{sessionId}` (parallel — isolated addition)
- [x] T034 [US3] Add `deleteConversation(sessionId)` method to `ConversationService` in `frontend/src/app/services/conversation.service.ts` — call API, remove from `conversations` signal on success, clear `selectedConversation` if it matches (depends on T033, T031)
- [x] T035 [US3] Add delete button (trash icon or "Supprimer") to each conversation summary card in `frontend/src/app/components/chat/history-panel/history-panel.html`; wire to `deleteConversation()` behind `window.confirm('Supprimer cette conversation ?')` guard; selected conversation detail view gets a "Retour" button (depends on T034)

**Checkpoint**: `cd backend && .venv/bin/pytest tests/ -v` — T029, T030 green. Delete a conversation in the UI, confirm via prompt, verify it disappears and stays gone on reload.

---

## Phase 5: Polish & Cross-Cutting Concerns

- [x] T036 [P] [US1] Add "load more" button to `frontend/src/app/components/chat/history-panel/history-panel.html` — visible only when `conversations().length === limit` (default 50); add `loadMore()` method to `ConversationService` in `frontend/src/app/services/conversation.service.ts` that fetches the next page (offset += limit) and appends results to the `conversations` signal (depends on T016, T020)
- [x] T037 [P] Run full backend validation: `cd backend && .venv/bin/pytest tests/ -v && .venv/bin/ruff check .` — confirm 0 failures, 0 lint errors
- [x] T038 [P] Run full frontend validation: `cd frontend && npm test -- --watch=false && npm run lint` — confirm 0 failures, 0 lint errors
- [x] T039 Perform manual end-to-end verification per `specs/010-persistent-chat-history/quickstart.md` — verify DB column, session grouping, panel UI, detail view, delete with confirmation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Foundational)**: No dependencies — start immediately; T001–T004 sequential (T002, T003 parallel with T001 once started)
- **Phase 2 (US1)**: Depends on Phase 1 completion
  - Tests T005–T010: parallel, write immediately after Phase 1
  - T011–T013: sequential (endpoint → register)
  - T014–T016: T014 parallel with backend, T015 parallel with T014, T016 depends on T014+T015
  - T017–T018: T017 first, T018 depends on T016+T017
  - T019–T022: sequential (component → template → styles → integration into chat)
- **Phase 3 (US2)**: Depends on Phase 2 completion; T023–T026 parallel, T027–T028 after tests
- **Phase 4 (US3)**: Depends on Phase 2 completion (can run parallel with Phase 3)
- **Phase 5 (Polish)**: Depends on all phases complete

### User Story Dependencies

- **US1 (P1)**: Depends on Phase 1 — no dependency on US2/US3
- **US2 (P2)**: Depends on US1 (verifies grouping logic already in place) — very little new code
- **US3 (P3)**: Depends on Phase 1 + US1 frontend panel — independent of US2

### Within Each User Story

1. Tests MUST be written and confirmed FAILING before implementation starts
2. Backend endpoints before frontend service wiring
3. Service before component
4. Component template before integration into chat view

### Parallel Opportunities

- T002 ‖ T003 (different files — both depend on T001)
- T005 ‖ T006 ‖ T007 ‖ T008 ‖ T009 ‖ T010 (all additive test additions)
- T014 ‖ T011 (frontend service types vs backend endpoint — different stacks)
- T015 ‖ T014 (test file vs service file)
- T023 ‖ T024 ‖ T025 ‖ T026 (different test files/assertions)
- T029 ‖ T030 ‖ T031 (different test files)
- T033 ‖ T029 (frontend API method vs backend test — different stacks)
- T036 ‖ T037 (backend vs frontend validation)

---

## Parallel Example: User Story 1 Backend vs Frontend

```bash
# Agent 1 — Backend: failing tests (T005–T010), then endpoints (T011 → T012 → T013)
# Agent 2 — Frontend: service types (T014), service tests (T015), service impl (T016)
# Agent 3 — Frontend: component (T019 → T020 → T021 → T022) after T016 complete
```

---

## Implementation Strategy

### MVP (User Story 1 only — 22 tasks)

1. Complete Phase 1: T001–T004
2. Write failing backend tests: T005–T010
3. Implement backend history endpoints: T011–T013
4. Write frontend service test: T015, then implement: T014, T016
5. Write chat sendMessage test: T017, then wire session_id: T018
6. Build history panel: T019 → T020 → T021 → T022
7. **STOP and VALIDATE**: history panel shows past sessions, clicks work, reload persists

### Incremental Delivery

1. Phase 1 + Phase 2 (US1): basic persistent history → **demo-ready**
2. Add Phase 3 (US2): verify grouping behavior with tests → improved confidence
3. Add Phase 4 (US3): delete conversation → complete UX
4. Phase 5: polish + final validation

---

## Notes

- TDD is mandatory per CLAUDE.md — RED → GREEN → REFACTOR, no exceptions
- `[P]` = different files, no conflicting dependencies
- Backend tests use the existing `test_client` fixture from `backend/tests/conftest.py`
- Frontend tests use Jasmine spies on `RagApiService` (existing pattern from chat.spec.ts)
- Run `cd backend && .venv/bin/ruff check .` after every backend change
- Never commit failing tests
- The DDL migration in T002 is idempotent — safe to run on every backend restart
