# Implementation Plan: Bulk Document Delete

**Branch**: `003-bulk-delete-docs` | **Date**: 2026-02-20 | **Spec**: [spec.md](./spec.md)

## Summary

Add checkbox-based multi-selection and bulk delete actions (delete selected, delete all) to the Angular 21 ingest component. Pure frontend change — no new backend endpoints. Deletions executed as sequential calls to the existing `DELETE /documents/{id}`.

## Technical Context

**Language/Version**: TypeScript 5.9, Angular 21
**Primary Dependencies**: Angular signals, RagApiService (existing)
**Storage**: N/A (frontend only)
**Testing**: Vitest
**Target Platform**: Browser SPA
**Performance Goals**: UI updates instantly; sequential deletes complete within 1s per document
**Constraints**: No new backend endpoints; no new npm dependencies
**Scale/Scope**: 1 component (ingest), 1 service (rag-api.service.ts — no changes needed)

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Local-First | ✅ | Pure frontend, no data leaves machine |
| II. Traceability | ✅ | Not affected by this feature |
| III. Fail Transparently | ✅ | Partial failure shows error, table refreshes |
| IV. Separation of Concerns | ✅ | Frontend-only; backend RAG unchanged |
| V. Demo-Ready Reproducibility | ✅ | No new dependencies or infrastructure |

## Project Structure

### Documentation (this feature)

```text
specs/003-bulk-delete-docs/
├── plan.md              ← this file
├── research.md          ← Phase 0 output
├── data-model.md        ← Phase 1 output
├── quickstart.md        ← Phase 1 output
└── tasks.md             ← Phase 2 output (/speckit.tasks)
```

### Source Code

```text
frontend/src/app/
├── components/ingest/
│   ├── ingest.ts        ← add selection signals + bulk delete methods
│   ├── ingest.html      ← add checkboxes, toolbar buttons
│   └── ingest.scss      ← checkbox + toolbar styles
└── services/
    └── rag-api.service.ts  ← no changes needed
```

**Structure Decision**: Single frontend project, Option 2 (web app). Backend untouched.
