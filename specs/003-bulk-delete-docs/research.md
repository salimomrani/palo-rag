# Research: Bulk Document Delete

**Date**: 2026-02-20

## Decision 1 — Selection State Management

**Decision**: `signal<Set<string>>(new Set())` — Signal holding a Set of selected document IDs.
**Rationale**: Signals are the Angular 21 reactive primitive. Set gives O(1) add/delete/has. Computed signals derive `allSelected` and `someSelected` from the Set + documents list.
**Alternatives considered**:
- `signal<string[]>` — simpler but O(n) lookup; rejected for clarity.
- `Map<string, boolean>` — verbose; Set is cleaner for membership testing.

## Decision 2 — Bulk Delete Strategy

**Decision**: Sequential calls to existing `DELETE /documents/{id}` using `concat` + `forkJoin` pattern — or simpler: iterate and call, refresh once at end.
**Rationale**: No new backend endpoint needed. `forkJoin` on an array of Observables runs them in parallel; acceptable for ≤15 documents (demo corpus size). On error, collect failures and surface them.
**Alternatives considered**:
- New `DELETE /documents/batch` endpoint — rejected (out of scope, backend change not needed).
- Sequential `concat` — more complex Rx chain; parallel `forkJoin` is simpler for this scale.

## Decision 3 — Header Checkbox Indeterminate State

**Decision**: Set `indeterminate` property on the header `<input type="checkbox">` via Angular template reference + `computed()`.
**Rationale**: Native HTML `indeterminate` property (not attribute) cannot be set via `[attr.indeterminate]`. Must use `[indeterminate]` binding or a directive. Angular supports `[indeterminate]` property binding directly on `<input type="checkbox">` in Angular 15+.
**Alternatives considered**:
- Custom checkbox component — overkill for one use case.
- CSS-only indeterminate — not accessible; native property preferred.

## Decision 4 — Confirmation Dialog

**Decision**: Native `confirm()` — consistent with existing `deleteDocument()` method.
**Rationale**: Already used in the codebase. No extra dependency.

## Decision 5 — Selection Reset

**Decision**: Reset selection after each bulk operation (success or failure).
**Rationale**: After a delete, the document list changes. Stale selection IDs would be confusing.
