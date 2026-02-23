# API Contract Changes: Chat Session Memory

**Date**: 2026-02-23 | **Feature**: 007-chat-session-memory

## Modified Endpoints

### POST /api/v1/query

**Change**: `history` field added to request body (optional, backward-compatible)

#### Request

```json
{
  "question": "string (required, 6-500 chars)",
  "history": [
    { "role": "user",      "content": "What is the onboarding process?" },
    { "role": "assistant", "content": "The onboarding process has 3 steps: ..." },
    { "role": "user",      "content": "Who is responsible for step 2?" }
  ]
}
```

**Notes**:
- `history` is optional — omitting it is equivalent to `[]`
- `history` entries are ordered oldest → newest
- Maximum 10 entries (5 user + 5 assistant turns) — entries beyond 10 are silently truncated on the backend
- Guardrails apply only to the current `question` field, not to history content
- An empty `history: []` produces identical behavior to the current system

#### Response

No change — response shape is identical to current:

```json
{
  "answer": "string",
  "sources": [{ "source": "string", "excerpt": "string", "score": number }],
  "confidence_score": number,
  "low_confidence": boolean,
  "latency_ms": number
}
```

---

### POST /api/v1/query/stream

**Change**: Same `history` field added (optional, backward-compatible)

#### Request

Identical to `POST /api/v1/query` above.

#### Response (SSE stream)

No change — SSE event types (`meta`, `token`, `done`) are unchanged.

---

## Unchanged Endpoints

All other endpoints (`POST /ingest`, `GET /documents`, `DELETE /documents/:id`, `GET /logs`, `POST /evaluation/run`, `GET /evaluation/report`) are unaffected by this feature.
