# Implementation Plan: Tests Unitaires Frontend

**Branch**: `005-frontend-unit-tests` | **Date**: 2026-02-20 | **Spec**: [spec.md](./spec.md)

## Tech Stack

- **Test runner**: Vitest 4.x via `@angular/build:unit-test` (builder Angular CLI natif, Angular 21)
- **DOM**: jsdom 27 (déjà installé)
- **Mocking HTTP**: `provideHttpClientTesting` + `HttpTestingController`
- **Mocking services**: `vi.fn()` + `{ provide: X, useValue: mock }`
- **Framework**: Angular 21, standalone, signals, OnPush, `inject()`

## Aucun nouveau package npm — 0 installation requise

## Files to Create / Modify

| File | Action | Description |
|------|--------|-------------|
| `frontend/angular.json` | Modify | Ajouter `"runner": "vitest"` dans la cible `test` |
| `frontend/src/app/components/chat/chat.spec.ts` | Create | Tests Chat (US2) |
| `frontend/src/app/components/ingest/ingest.spec.ts` | Create | Tests Ingest (US3) |

## Configuration angular.json (cible test)

```json
"test": {
  "builder": "@angular/build:unit-test",
  "options": {
    "tsConfig": "tsconfig.spec.json",
    "runner": "vitest"
  }
}
```

## Mock RagApiService partagé

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

## Chat — scénarios couverts (US2)

1. Chips visibles si `messages()` vide et non chargement
2. `canSend` faux si prompt vide ou `isLoading` vrai
3. `sendMessage()` avec prompt valide → `streamQuery()` appelé + message utilisateur ajouté
4. `sendMessage()` avec prompt vide → aucun appel, aucun message
5. `selectSuggestion(q)` → prompt défini + message envoyé

## Ingest — scénarios couverts (US3)

1. `toggleSelection(id)` → ajoute puis retire de `selectedIds`
2. `allSelected()` vrai quand tous les docs cochés
3. `someSelected()` vrai pour sélection partielle, faux si tous/aucun
4. `noneSelected()` vrai si sélection vide
5. `toggleAll()` → sélectionne tout ; second appel vide
6. `noneSelected()` → `deleteSelected()` ne déclenche pas `streamQuery`

## Commandes

```bash
cd frontend && npm test          # run once
cd frontend && npm test -- --watch  # watch mode
```

## Constitution Check

- **Local-first** ✓ — aucun appel réseau réel (tout mocké)
- **Séparation des concerns** ✓ — tests frontend totalement indépendants du backend
- **Reproductible** ✓ — `npm test` depuis checkout propre, 0 dépendance cloud
