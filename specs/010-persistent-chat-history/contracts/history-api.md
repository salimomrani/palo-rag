# API Contract: Chat History

**Feature**: 010-persistent-chat-history
**Base URL**: `http://localhost:8000/api/v1`
**Date**: 2026-02-27

---

## Modified Endpoint: POST /query/stream

### Request Body (updated)

```json
{
  "question": "string (required)",
  "history": [
    { "role": "user", "content": "string" }
  ],
  "session_id": "string (optional UUID, e.g. '550e8400-e29b-41d4-a716-446655440000')"
}
```

**Change**: `session_id` field is optional. Existing requests without it continue to work unchanged.

---

## New Endpoints: GET /history

### Request

```
GET /api/v1/history?limit=50&offset=0
```

| Parameter | Type | Required | Default | Notes |
|---|---|---|---|---|
| `limit` | integer | No | 50 | Max conversations returned |
| `offset` | integer | No | 0 | Pagination offset |

### Response 200 OK

```json
[
  {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "started_at": "2026-02-27T14:30:00.000Z",
    "first_question": "Comment contacter le support tech...",
    "exchange_count": 4
  },
  {
    "session_id": "661f9511-f30c-52e5-b827-557766551111",
    "started_at": "2026-02-26T09:15:00.000Z",
    "first_question": "Quelles sont les étapes d'onboard...",
    "exchange_count": 2
  }
]
```

- Ordered by `started_at` DESC (most recent first)
- Only sessions with at least one `query_logs` row with a non-null `session_id`
- `first_question` is the `question_masked` of the earliest query in the session, truncated to 80 chars

### Response — Empty History

```json
[]
```

---

## New Endpoint: GET /history/{session_id}

### Request

```
GET /api/v1/history/550e8400-e29b-41d4-a716-446655440000
```

### Response 200 OK

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "exchanges": [
    {
      "id": "a1b2c3d4-1234-5678-abcd-ef0123456789",
      "timestamp": "2026-02-27T14:30:00.000Z",
      "question_masked": "Comment contacter le support technique ?",
      "answer": "Vous pouvez contacter le support via l'email support@example.com...",
      "guardrail_triggered": null,
      "rejected": false
    },
    {
      "id": "b2c3d4e5-2345-6789-bcde-f01234567890",
      "timestamp": "2026-02-27T14:31:00.000Z",
      "question_masked": "Et par téléphone ?",
      "answer": "Le numéro de support téléphonique est...",
      "guardrail_triggered": null,
      "rejected": false
    }
  ]
}
```

- Ordered by `timestamp` ASC (chronological order)
- `rejected: true` when `guardrail_triggered` is non-null

### Response 404 Not Found

```json
{ "detail": "Session not found" }
```

---

## New Endpoint: DELETE /history/{session_id}

### Request

```
DELETE /api/v1/history/550e8400-e29b-41d4-a716-446655440000
```

### Response 204 No Content

Empty body.

### Response 404 Not Found

```json
{ "detail": "Session not found" }
```

---

## Error Codes Summary

| Status | Meaning |
|---|---|
| 200 | Success with body |
| 204 | Success, no body (DELETE) |
| 404 | Session not found |
| 422 | Validation error (invalid UUID format) |
