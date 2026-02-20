# Data Model: Bulk Document Delete

**Date**: 2026-02-20

## Existing Entity (unchanged)

### Document (from rag-api.service.ts)

```typescript
export interface Document {
  id: string;
  name: string;
  chunk_count: number;
  ingested_at: string;
}
```

## New Component State (ingest.ts signals)

| Signal | Type | Description |
|--------|------|-------------|
| `selectedIds` | `signal<Set<string>>` | IDs of currently checked documents |
| `isDeleting` | `signal<boolean>` | True while bulk delete in progress |

## Derived (computed)

| Computed | Logic | Usage |
|----------|-------|-------|
| `allSelected` | `selectedIds().size === documents().length && documents().length > 0` | Header checkbox checked state |
| `someSelected` | `selectedIds().size > 0 && !allSelected()` | Header checkbox indeterminate state |
| `noneSelected` | `selectedIds().size === 0` | Disable "Supprimer la sélection" button |

## State Transitions

```
Initial → user ticks row       → selectedIds grows
         user unticks row      → selectedIds shrinks
         user ticks header     → selectedIds = all IDs
         user unticks header   → selectedIds = empty Set
         delete selected/all   → isDeleting=true → API calls → refresh → selectedIds reset → isDeleting=false
```
