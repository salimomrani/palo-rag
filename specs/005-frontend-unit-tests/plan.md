# Implementation Plan: Frontend Unit Tests

**Branch**: `005-frontend-unit-tests` | **Date**: 2026-02-20 | **Spec**: [spec.md](./spec.md)

## Tech Stack

- **Test runner**: Vitest 4.x via `@angular/build:unit-test` (native Angular CLI builder, Angular 21)
- **DOM**: jsdom 27 (already installed)
- **HTTP mocking**: `provideHttpClientTesting` + `HttpTestingController`
- **Service mocking**: `vi.fn()` + `{ provide: X, useValue: mock }`
- **Framework**: Angular 21, standalone, signals, OnPush, `inject()`

## No new npm packages — 0 installs required

## Files to Create / Modify

| File | Action | Description |
|------|--------|-------------|
| `frontend/angular.json` | Modify | Add `"runner": "vitest"` to the `test` target |
| `frontend/src/app/components/chat/chat.spec.ts` | Create | Chat tests (US2) |
| `frontend/src/app/components/ingest/ingest.spec.ts` | Create | Ingest tests (US3) |

## angular.json configuration (test target)

```json
"test": {
  "builder": "@angular/build:unit-test",
  "options": {
    "tsConfig": "tsconfig.spec.json",
    "runner": "vitest"
  }
}
```

## Shared RagApiService mock

```typescript
import { of, NEVER } from 'rxjs';
import { vi } from 'vitest';

const mockApi = {
  streamQuery: vi.fn().mockReturnValue(NEVER),
  getDocuments: vi.fn().mockReturnValue(of([])),
  ingest: vi.fn().mockReturnValue(of({ chunk_count: 3 })),
  deleteDocument: vi.fn().mockReturnValue(of(null)),
};
```

## Chat — covered scenarios (US2)

1. Chips visible if `messages()` empty and not loading
2. `canSend` false if prompt empty or `isLoading` true
3. `sendMessage()` with valid prompt → `streamQuery()` called + user message added
4. `sendMessage()` with empty prompt → no call, no message
5. `selectSuggestion(q)` → prompt set + message sent

## Ingest — covered scenarios (US3)

1. `toggleSelection(id)` → adds then removes from `selectedIds`
2. `allSelected()` true when all docs checked
3. `someSelected()` true for partial selection, false if all/none
4. `noneSelected()` true if selection empty
5. `toggleAll()` → selects all; second call clears
6. `noneSelected()` → `deleteSelected()` does not trigger `streamQuery`

## Commands

```bash
cd frontend && npm test          # run once
cd frontend && npm test -- --watch  # watch mode
```

## Constitution Check

- **Local-first** ✓ — no real network calls (all mocked)
- **Separation of concerns** ✓ — frontend tests fully independent of backend
- **Reproducible** ✓ — `npm test` from clean checkout, 0 cloud dependencies
