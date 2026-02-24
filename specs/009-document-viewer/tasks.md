# Tasks — Document Content Viewer (009)

## Phase 1 — Spec & Plan
- [x] Explore backend capabilities for retrieving document content
- [x] Write spec.md
- [x] Write plan.md

## Phase 2 — Implementation (TDD)

### T001 — Backend Endpoint
- [x] Add `GET /documents/{doc_id}/content` in `v1/ingest.py`
- [x] Implement chunk extraction and sorting by `chunk_index`
- [x] Add test in `test_ingest.py`

### T002 — Frontend Service & State
- [x] Add `getDocumentContent` to `RagApiService`
- [x] Add `viewingDocument`, `isLoadingContent` signals in `ingest.ts`
- [x] Add `viewDocument(doc)` to fetch and show content

### T003 — Frontend UI
- [x] Add an "👁" button in `ingest.html`'s table
- [x] Add modal overlay in `ingest.html`
- [x] Add modal styles in `ingest.scss`

### T004 — Frontend Tests
- [x] Add mock `getDocumentContent` to `ingest.spec.ts`
- [x] Test that `viewDocument` calls API and opens modal
- [x] Test modal close interactions

## Phase 3 — Completion
- [x] `npm test -- --watch=false`
- [x] `pytest tests`
- [x] `npm run lint` & `ruff check .`
- [x] Browser visual verification
- [x] Commit on feature branch `feat/009-document-viewer`
- [x] Open PR
