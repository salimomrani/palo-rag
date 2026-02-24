# Spec 009 — Document Content Viewer

## Summary

Allow users to visualize the raw ingested text content of a document directly from the `/ingest` page.

## Problem

Currently, the ingest page displays external metadata (name, chunks, date) but users cannot see the actual text that the RAG assistant is querying against. Without this, users cannot:
- Verify that a file was parsed correctly
- See how the document was split into chunks `[source] chunk_content`
- Audit the knowledge base contents

## Solution

### Backend

Create a new endpoint `GET /api/v1/documents/{doc_id}/content` that returns the original document text.
Since PALO splits the document at ingestion time, it will query the ChromaDB vector store collection, fetch all chunks matching `doc_id`, sort them by their original `chunk_index`, and return the reconstructed document (either as an array of chunks or a unified string).

### Frontend

Add an "👁" (View) button next to the delete button in the Knowledge Base table rows.
Clicking it will:
1. Fetch the document content from the new API endpoint
2. Open a modal or an expanded view showing the title (filename) and the reconstructed text (in a scrollable `pre` or `markdown` block).
3. Include a "Close" button to dismiss the view.

## Scope

- **Backend**: `v1/ingest.py`, `tests/api/v1/test_ingest.py`.
- **Frontend**: `ingest.html` (add view button + modal), `ingest.ts` (API call and state management), `ingest.scss` (modal styles), `rag-api.service.ts` (new typed call).

## Acceptance Criteria

- [ ] Backend endpoint `/documents/{doc_id}/content` exists, returns 200 with text content or 404.
- [ ] Chunks are ordered correctly (ignoring similarity score, just structural order).
- [ ] Frontend table rows have a "View" button.
- [ ] Clicking "View" displays the document text natively in the browser without downloading.
- [ ] UI is responsive and clearly styled (modal overlay or similar).
- [ ] `npm run lint` and `ruff check .` pass.
- [ ] Tests pass in backend and frontend.
