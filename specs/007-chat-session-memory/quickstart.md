# Quickstart: Chat Session Memory

**Date**: 2026-02-23 | **Feature**: 007-chat-session-memory

## Prerequisites

No new dependencies. All existing prerequisites apply:
- Docker running: `docker-compose up -d` (PostgreSQL)
- Ollama running with models: `qwen2.5:7b` and `mxbai-embed-large`

## Running the feature

```bash
# Backend
cd backend && .venv/bin/uvicorn main:app --reload --port 8000

# Frontend
cd frontend && npm start
```

## Manual test: multi-turn conversation

1. Open http://localhost:4200
2. Ask: **"Quelles sont les étapes d'onboarding pour un nouveau client ?"**
3. Wait for the answer
4. Ask: **"Qui est responsable de la première étape ?"**
5. Verify: the assistant references the onboarding steps from the previous answer without the user repeating the topic

## Manual test: clear history

1. Have a conversation (2+ exchanges)
2. Click the **"Effacer"** button
3. Ask: **"Répète ce que tu viens de dire"**
4. Verify: the assistant has no memory of previous exchanges

## Verifying history is passed

In browser DevTools → Network → XHR, look at the `POST /api/v1/query/stream` request body:

```json
{
  "question": "Qui est responsable de la première étape ?",
  "history": [
    { "role": "user", "content": "Quelles sont les étapes d'onboarding ?" },
    { "role": "assistant", "content": "Les étapes sont : ..." }
  ]
}
```

## Running tests

```bash
# Backend (all tests including new history tests)
cd backend && .venv/bin/pytest tests/ -v

# Backend lint
cd backend && .venv/bin/ruff check .

# Frontend
cd frontend && npm test -- --watch=false

# Frontend lint
cd frontend && npm run lint
```
