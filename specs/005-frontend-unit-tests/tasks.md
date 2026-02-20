# Tasks: Tests Unitaires Frontend

**Input**: Design documents from `/specs/005-frontend-unit-tests/`
**Branch**: `005-frontend-unit-tests`
**Tests**: Oui — cette feature EST les tests (les spec files sont l'output)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)

---

## Phase 1: Foundational (Blocking Prerequisite)

**Purpose**: Activer Vitest via le builder Angular CLI — requis par toutes les user stories

**⚠️ CRITICAL**: Must be complete before any spec file can be run

- [x] T001 Add `"runner": "vitest"` and `"tsConfig": "tsconfig.spec.json"` to the `test` architect options in `frontend/angular.json`
- [x] T002 Verify `ng test` runs without error (empty suite) in `frontend/` — `cd frontend && npm test -- --run 2>&1 | head -20`

**Checkpoint**: `npm test` démarre Vitest et affiche "0 tests" sans erreur de config

---

## Phase 2: User Story 1 — Suite de tests opérationnelle (P1) 🎯 MVP

**Goal**: La commande `npm test` fonctionne et détecte les fichiers `.spec.ts`

**Independent Test**: Créer un spec trivial `true === true` → passe au premier run

### Implementation

- [x] T003 [US1] Create smoke test `frontend/src/app/app.spec.ts` — single `it('should be true', () => expect(true).toBe(true))` to validate runner works end-to-end

**Checkpoint**: `npm test` passe avec 1 test vert

---

## Phase 3: User Story 2 — Tests du composant Chat (P2)

**Goal**: Comportements Chat couverts : chips de suggestion, envoi de message, canSend, selectSuggestion

**Independent Test**: `npm test -- --run src/app/components/chat/chat.spec.ts` → tous les tests passent

### Implementation

- [x] T004 [US2] Create `frontend/src/app/components/chat/chat.spec.ts` with:
  - `beforeEach`: configure `TestBed` with `Chat` component + `{ provide: RagApiService, useValue: mockApi }` where `mockApi = { streamQuery: vi.fn().mockReturnValue(NEVER), getDocuments: vi.fn().mockReturnValue(of([])), deleteDocument: vi.fn().mockReturnValue(of(null)) }`
  - **Test 1** — chips visibles quand conversation vide : `expect(fixture.nativeElement.querySelectorAll('.suggestion-chip').length).toBeGreaterThan(0)`
  - **Test 2** — chips cachés après envoi : after `component.messages.set([{ id:'1', role:'user', content:'q' }])` + `detectChanges()`, `expect(chips.length).toBe(0)`
  - **Test 3** — `canSend` faux si prompt vide : `expect(component.canSend()).toBe(false)`
  - **Test 4** — `canSend` faux si `isLoading` vrai : `component.prompt.set('test'); component.isLoading.set(true); expect(component.canSend()).toBe(false)`
  - **Test 5** — `sendMessage()` appelle `streamQuery` avec le bon prompt : `component.prompt.set('hello'); component.sendMessage(); expect(mockApi.streamQuery).toHaveBeenCalledWith('hello')`

**Checkpoint**: 5 tests Chat passent

---

## Phase 4: User Story 3 — Tests du composant Ingest (P3)

**Goal**: Logique de sélection groupée couverte : selectedIds, computed signals, toggleAll

**Independent Test**: `npm test -- --run src/app/components/ingest/ingest.spec.ts` → tous les tests passent

### Implementation

- [x] T005 [US3] Create `frontend/src/app/components/ingest/ingest.spec.ts` with:
  - `beforeEach`: configure `TestBed` with `Ingest` + `{ provide: RagApiService, useValue: mockApi }` where `mockApi.getDocuments` returns `of([{ id: 'a', name: 'doc-a.md', chunk_count: 2 }, { id: 'b', name: 'doc-b.md', chunk_count: 1 }])`
  - **Test 1** — `toggleSelection` ajoute un ID : `component.toggleSelection('a'); expect(component.selectedIds().has('a')).toBe(true)`
  - **Test 2** — `toggleSelection` deux fois retire l'ID : `component.toggleSelection('a'); component.toggleSelection('a'); expect(component.selectedIds().has('a')).toBe(false)`
  - **Test 3** — `noneSelected` vrai par défaut : `expect(component.noneSelected()).toBe(true)`
  - **Test 4** — `allSelected` vrai si tous sélectionnés : `component.selectedIds.set(new Set(['a','b'])); expect(component.allSelected()).toBe(true)`
  - **Test 5** — `someSelected` vrai pour sélection partielle : `component.selectedIds.set(new Set(['a'])); expect(component.someSelected()).toBe(true); expect(component.allSelected()).toBe(false)`
  - **Test 6** — `toggleAll` sélectionne tout, second appel vide : `component.toggleAll(); expect(component.allSelected()).toBe(true); component.toggleAll(); expect(component.noneSelected()).toBe(true)`

**Checkpoint**: 6 tests Ingest passent

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

- T004 (chat.spec.ts) et T005 (ingest.spec.ts) sont dans des fichiers différents → parallélisables
- T006, T007, T008 (polish) → tous parallélisables

---

## Implementation Strategy

### MVP (Phase 1 + 2)

1. Activer Vitest dans `angular.json`
2. Smoke test pour valider le runner
3. **STOP et valider** : `npm test` vert
4. Continuer avec Chat → Ingest → Polish

### Full delivery (~8 tasks)

| Phase | Tasks | Files |
|-------|-------|-------|
| 1 Foundational | T001–T002 | angular.json |
| 2 US1 | T003 | app.spec.ts |
| 3 US2 | T004 | chat.spec.ts |
| 4 US3 | T005 | ingest.spec.ts |
| 5 Polish | T006–T008 | — |

**Total: 8 tasks — 4 fichiers — pure frontend**

---

## Notes

- Imports nécessaires dans chaque spec : `{ TestBed, ComponentFixture } from '@angular/core/testing'`, `{ of, NEVER } from 'rxjs'`, `{ vi } from 'vitest'`
- `provideMarkdown()` requis dans `imports` de `chat.spec.ts` (sinon erreur ngx-markdown)
- `fixture.detectChanges()` requis après chaque mutation de signal pour déclencher OnPush
- `component.documents.set([...])` directement sur le signal pour initialiser les tests Ingest sans attendre l'appel HTTP
