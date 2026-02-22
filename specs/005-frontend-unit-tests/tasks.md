# Tasks: Frontend Unit Tests

**Input**: Design documents from `/specs/005-frontend-unit-tests/`
**Branch**: `005-frontend-unit-tests`
**Tests**: Yes — this feature IS the tests (the spec files are the output)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)

---

## Phase 1: Foundational (Blocking Prerequisite)

**Purpose**: Enable Vitest via the Angular CLI builder — required by all user stories

**⚠️ CRITICAL**: Must be complete before any spec file can be run

- [x] T001 Add `"runner": "vitest"` and `"tsConfig": "tsconfig.spec.json"` to the `test` architect options in `frontend/angular.json`
- [x] T002 Verify `ng test` runs without error (empty suite) in `frontend/` — `cd frontend && npm test -- --run 2>&1 | head -20`

**Checkpoint**: `npm test` starts Vitest and shows "0 tests" without config error

---

## Phase 2: User Story 1 — Operational Test Suite (P1) 🎯 MVP

**Goal**: The `npm test` command works and detects `.spec.ts` files

**Independent Test**: Create a trivial spec `true === true` → passes on first run

### Implementation

- [x] T003 [US1] Create smoke test `frontend/src/app/app.spec.ts` — single `it('should be true', () => expect(true).toBe(true))` to validate runner works end-to-end

**Checkpoint**: `npm test` passes with 1 green test

---

## Phase 3: User Story 2 — Chat Component Tests (P2)

**Goal**: Chat behaviours covered: suggestion chips, message sending, canSend, selectSuggestion

**Independent Test**: `npm test -- --run src/app/components/chat/chat.spec.ts` → all tests pass

### Implementation

- [x] T004 [US2] Create `frontend/src/app/components/chat/chat.spec.ts` with:
  - `beforeEach`: configure `TestBed` with `Chat` component + `{ provide: RagApiService, useValue: mockApi }` where `mockApi = { streamQuery: vi.fn().mockReturnValue(NEVER), getDocuments: vi.fn().mockReturnValue(of([])), deleteDocument: vi.fn().mockReturnValue(of(null)) }`
  - **Test 1** — chips visible when conversation empty: `expect(fixture.nativeElement.querySelectorAll('.suggestion-chip').length).toBeGreaterThan(0)`
  - **Test 2** — chips hidden after send: after `component.messages.set([{ id:'1', role:'user', content:'q' }])` + `detectChanges()`, `expect(chips.length).toBe(0)`
  - **Test 3** — `canSend` false if prompt empty: `expect(component.canSend()).toBe(false)`
  - **Test 4** — `canSend` false if `isLoading` true: `component.prompt.set('test'); component.isLoading.set(true); expect(component.canSend()).toBe(false)`
  - **Test 5** — `sendMessage()` calls `streamQuery` with the correct prompt: `component.prompt.set('hello'); component.sendMessage(); expect(mockApi.streamQuery).toHaveBeenCalledWith('hello')`

**Checkpoint**: 5 Chat tests pass

---

## Phase 4: User Story 3 — Ingest Component Tests (P3)

**Goal**: Bulk selection logic covered: selectedIds, computed signals, toggleAll

**Independent Test**: `npm test -- --run src/app/components/ingest/ingest.spec.ts` → all tests pass

### Implementation

- [x] T005 [US3] Create `frontend/src/app/components/ingest/ingest.spec.ts` with:
  - `beforeEach`: configure `TestBed` with `Ingest` + `{ provide: RagApiService, useValue: mockApi }` where `mockApi.getDocuments` returns `of([{ id: 'a', name: 'doc-a.md', chunk_count: 2 }, { id: 'b', name: 'doc-b.md', chunk_count: 1 }])`
  - **Test 1** — `toggleSelection` adds an ID: `component.toggleSelection('a'); expect(component.selectedIds().has('a')).toBe(true)`
  - **Test 2** — `toggleSelection` twice removes the ID: `component.toggleSelection('a'); component.toggleSelection('a'); expect(component.selectedIds().has('a')).toBe(false)`
  - **Test 3** — `noneSelected` true by default: `expect(component.noneSelected()).toBe(true)`
  - **Test 4** — `allSelected` true if all selected: `component.selectedIds.set(new Set(['a','b'])); expect(component.allSelected()).toBe(true)`
  - **Test 5** — `someSelected` true for partial selection: `component.selectedIds.set(new Set(['a'])); expect(component.someSelected()).toBe(true); expect(component.allSelected()).toBe(false)`
  - **Test 6** — `toggleAll` selects all, second call clears: `component.toggleAll(); expect(component.allSelected()).toBe(true); component.toggleAll(); expect(component.noneSelected()).toBe(true)`

**Checkpoint**: 6 Ingest tests pass

---

## Phase 5: Polish

- [x] T006 [P] Keep smoke test `frontend/src/app/app.spec.ts` (useful — kept)
- [x] T007 [P] Verify full suite → 16/16 pass, 0 failures
- [x] T008 [P] Verify lint still passes → 0 errors (1 pre-existing warning)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Foundational)**: No dependencies — start immediately
- **Phase 2 (US1)**: Depends on Phase 1
- **Phase 3 (US2)**: Depends on Phase 1 — can run in parallel with Phase 4
- **Phase 4 (US3)**: Depends on Phase 1 — can run in parallel with Phase 3
- **Phase 5 (Polish)**: Depends on Phase 3 + 4

### Parallel Opportunities

- T004 (chat.spec.ts) and T005 (ingest.spec.ts) are in different files → parallelisable
- T006, T007, T008 (polish) → all parallelisable

---

## Implementation Strategy

### MVP (Phase 1 + 2)

1. Enable Vitest in `angular.json`
2. Smoke test to validate the runner
3. **STOP and validate**: `npm test` green
4. Continue with Chat → Ingest → Polish

### Full delivery (~8 tasks)

| Phase | Tasks | Files |
|-------|-------|-------|
| 1 Foundational | T001–T002 | angular.json |
| 2 US1 | T003 | app.spec.ts |
| 3 US2 | T004 | chat.spec.ts |
| 4 US3 | T005 | ingest.spec.ts |
| 5 Polish | T006–T008 | — |

**Total: 8 tasks — 4 files — pure frontend**

---

## Notes

- Required imports in each spec: `{ TestBed, ComponentFixture } from '@angular/core/testing'`, `{ of, NEVER } from 'rxjs'`, `{ vi } from 'vitest'`
- `provideMarkdown()` required in `imports` of `chat.spec.ts` (otherwise ngx-markdown error)
- `fixture.detectChanges()` required after each signal mutation to trigger OnPush
- `component.documents.set([...])` directly on the signal to initialise Ingest tests without waiting for an HTTP call
