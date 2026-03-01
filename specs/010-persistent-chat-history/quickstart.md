# Quickstart: Persistent Chat History

**Feature**: 010-persistent-chat-history

---

## Prerequisites

- Docker PostgreSQL running: `docker-compose up -d`
- Backend venv: `backend/.venv/bin/`
- Backend started: `cd backend && .venv/bin/uvicorn main:app --reload --port 8000`
- Frontend started: `cd frontend && npm start`

---

## Manual Verification Steps

### Step 1 — Verify DB Migration

After starting the backend, confirm the new column exists:

```bash
docker exec -it palo-db-1 psql -U palo -d palo -c "\d query_logs"
# Look for: session_id | character varying | | |
```

### Step 2 — Send Queries with session_id

Open two browser tabs to `http://localhost:4200/chat`.

**Tab A** — ask 2 questions and note the network request includes `session_id`.

In DevTools → Network → `query/stream` → Payload, confirm:
```json
{ "question": "...", "history": [], "session_id": "some-uuid" }
```

**Tab B** — ask 1 different question (different `session_id` since it's a new tab).

### Step 3 — Verify History Panel

1. Reload Tab A
2. Click the "Historique" toggle button in the chat header
3. History panel slides in from the left
4. You should see at least 2 conversation entries (Tab A session + Tab B session)

### Step 4 — View Conversation Detail

Click on the Tab A conversation entry.
- All 2 exchanges appear, ordered chronologically
- Questions appear as masked if PII was detected

### Step 5 — Delete a Conversation

Click the delete icon on the Tab B conversation.
- Confirmation prompt appears
- After confirmation, the entry disappears from the list

Reload the page and re-open history — Tab B conversation does not reappear.

### Step 6 — Verify Guardrail Entries in History

Send a query that triggers a guardrail (e.g., very short: "a").
Open history — the conversation appears. Click to expand — the rejected exchange shows the refusal message.

---

## Regression Checks

```bash
# Backend tests — all green
cd backend && .venv/bin/pytest tests/ -v && .venv/bin/ruff check .

# Frontend tests — all green
cd frontend && npm test -- --watch=false && npm run lint
```

---

## API Quick Test

```bash
# List conversations
curl http://localhost:8000/api/v1/history

# Get conversation detail
curl http://localhost:8000/api/v1/history/<session_id>

# Delete a conversation
curl -X DELETE http://localhost:8000/api/v1/history/<session_id>
```
