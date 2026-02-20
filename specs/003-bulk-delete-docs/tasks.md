# Tasks: Bulk Document Delete

**Input**: Design documents from `/specs/003-bulk-delete-docs/`
**Branch**: `003-bulk-delete-docs`
**Tests**: Not requested — no test tasks generated

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)

---

## Phase 1: Foundational (Blocking Prerequisite)

**Purpose**: Add selection state signals to the component — required by all user stories

**⚠️ CRITICAL**: Must be complete before any user story work begins

- [x] T001 Add `selectedIds` signal (`signal<Set<string>>(new Set())`) and `isDeleting` signal to `frontend/src/app/components/ingest/ingest.ts`
- [x] T002 Add computed signals `allSelected`, `someSelected`, `noneSelected` to `frontend/src/app/components/ingest/ingest.ts`
- [x] T003 Add `toggleSelection(id: string)` and `clearSelection()` helper methods to `frontend/src/app/components/ingest/ingest.ts`

**Checkpoint**: Selection state is reactive and computed signals reflect document list correctly

---

## Phase 2: User Story 1 — Select and Delete Multiple Documents (P1) 🎯 MVP

**Goal**: Checkbox per row + "Supprimer la sélection" button

**Independent Test**: Load page with 3 docs, tick 2, click button, confirm → 2 deleted, 1 remains

### Implementation

- [x] T004 [US1] Add checkbox column to document rows in `frontend/src/app/components/ingest/ingest.html` — bind to `selectedIds()` with `(change)="toggleSelection(doc.id)"`
- [x] T005 [US1] Add "Supprimer la sélection" toolbar button in `frontend/src/app/components/ingest/ingest.html` — disabled when `noneSelected()`
- [x] T006 [US1] Implement `deleteSelected()` method in `frontend/src/app/components/ingest/ingest.ts` — `forkJoin` on `deleteDocument()` calls for each selected ID, then `clearSelection()` + `loadDocuments()`
- [x] T007 [US1] Add error handling in `deleteSelected()`: surface failures via `error` signal in `frontend/src/app/components/ingest/ingest.ts`
- [x] T008 [P] [US1] Add checkbox and toolbar styles (`.checkbox-col`, `.toolbar`, `.btn-delete-selected`) to `frontend/src/app/components/ingest/ingest.scss`

**Checkpoint**: User can tick rows and delete selection — US1 fully functional

---

## Phase 3: User Story 2 — Delete All Documents (P2)

**Goal**: "Tout supprimer" button that wipes the entire knowledge base

**Independent Test**: Load page with docs, click "Tout supprimer", confirm → table empty

### Implementation

- [x] T009 [US2] Add "Tout supprimer" toolbar button in `frontend/src/app/components/ingest/ingest.html` — disabled when `documents().length === 0`
- [x] T010 [US2] Implement `deleteAll()` method in `frontend/src/app/components/ingest/ingest.ts` — `confirm()` dialog, then `forkJoin` on all document IDs, then `clearSelection()` + `loadDocuments()`
- [x] T011 [P] [US2] Style "Tout supprimer" button (`.btn-delete-all`, destructive red variant) in `frontend/src/app/components/ingest/ingest.scss`

**Checkpoint**: User can delete all documents in 2 interactions — US2 fully functional

---

## Phase 4: User Story 3 — Select All via Header Checkbox (P3)

**Goal**: Header checkbox with indeterminate state for select all / deselect all

**Independent Test**: Load page with 3 docs, tick header → all rows checked; untick header → all deselected; tick 1 row → header indeterminate

### Implementation

- [x] T012 [US3] Add header checkbox to document table in `frontend/src/app/components/ingest/ingest.html` — `[checked]="allSelected()"`, `[indeterminate]="someSelected()"`, `(change)="toggleAll()"`
- [x] T013 [US3] Implement `toggleAll()` method in `frontend/src/app/components/ingest/ingest.ts` — sets `selectedIds` to all IDs if not all selected, else clears
- [x] T014 [P] [US3] Add header checkbox column style (`.th-checkbox`) in `frontend/src/app/components/ingest/ingest.scss`

**Checkpoint**: Header checkbox controls all rows with correct indeterminate state — US3 fully functional

---

## Phase 5: Polish

**Purpose**: UX consistency and cleanup

- [x] T015 [P] Add `isDeleting` spinner/disabled state to both bulk delete buttons during operation in `frontend/src/app/components/ingest/ingest.html`
- [x] T016 Reset `selectedIds` on `loadDocuments()` success in `frontend/src/app/components/ingest/ingest.ts`
- [x] T017 [P] Verify lint passes: `cd frontend && npm run lint`
- [x] T018 [P] Manual test per `specs/003-bulk-delete-docs/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Foundational)**: No dependencies — start immediately
- **Phase 2 (US1)**: Depends on Phase 1 completion
- **Phase 3 (US2)**: Depends on Phase 1 — can run in parallel with Phase 2
- **Phase 4 (US3)**: Depends on Phase 1 — can run in parallel with Phase 2 & 3
- **Phase 5 (Polish)**: Depends on all story phases

### Parallel Opportunities

- T008, T011, T014 (SCSS tasks) can all run in parallel — different sections of the same file, or split into 1 pass
- T004+T005 (HTML row + toolbar) can be done in one pass
- Phase 2, 3, 4 can be tackled sequentially (single dev) in 20-30min total

---

## Implementation Strategy

### MVP (Phase 1 + Phase 2 only)

1. Complete Phase 1 — selection signals
2. Complete Phase 2 — checkboxes + delete selected
3. **STOP and validate**: tick rows, delete selection works
4. Continue with Phase 3 → Phase 4 → Phase 5

### Full delivery (all phases, ~18 tasks)

| Phase | Tasks | Files touched |
|-------|-------|---------------|
| 1 Foundational | T001–T003 | ingest.ts |
| 2 US1 | T004–T008 | ingest.ts, ingest.html, ingest.scss |
| 3 US2 | T009–T011 | ingest.ts, ingest.html, ingest.scss |
| 4 US3 | T012–T014 | ingest.ts, ingest.html, ingest.scss |
| 5 Polish | T015–T018 | ingest.ts, ingest.html |

**Total: 18 tasks — 3 files — pure frontend**

---

## Notes

- No backend changes required
- No new npm dependencies
- `forkJoin([])` on empty array completes immediately — safe if called with 0 items
- `[indeterminate]` is a DOM property binding (not attribute) — Angular supports it natively
