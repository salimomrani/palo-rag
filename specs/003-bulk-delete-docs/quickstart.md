# Quickstart: Bulk Document Delete

## No new setup required

This feature is purely frontend. No backend changes, no new dependencies, no migration.

## Test manually

1. Start backend: `cd backend && .venv/bin/uvicorn main:app --reload --port 8000`
2. Start frontend: `cd frontend && npm start`
3. Navigate to **http://localhost:4200/ingest**
4. Ingest 2–3 test documents
5. Tick checkboxes → "Supprimer la sélection" becomes enabled
6. Tick header checkbox → all rows selected
7. Click "Tout supprimer" → confirm → table empties
