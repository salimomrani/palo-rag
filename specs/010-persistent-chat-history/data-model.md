# Data Model: Persistent Chat History

**Feature**: 010-persistent-chat-history
**Date**: 2026-02-27

---

## Backend Changes

### Modified Table: `query_logs`

Extend the existing `QueryLog` ORM model with one new nullable column.

| Column | Type | Nullable | Default | Notes |
|---|---|---|---|---|
| `id` | VARCHAR (UUID) | NO | uuid4() | Existing — primary key |
| `timestamp` | DATETIME | NO | now(UTC) | Existing |
| `question_masked` | TEXT | NO | — | Existing — PII-masked question |
| `retrieved_sources` | JSON | NO | [] | Existing |
| `similarity_scores` | JSON | NO | [] | Existing |
| `answer` | TEXT | NO | — | Existing |
| `faithfulness_score` | FLOAT | NO | 0.0 | Existing |
| `latency_ms` | INTEGER | NO | 0 | Existing |
| `guardrail_triggered` | VARCHAR | YES | NULL | Existing |
| `session_id` | VARCHAR (UUID) | YES | NULL | **NEW** — groups queries into conversations |

**Migration**: `ALTER TABLE query_logs ADD COLUMN IF NOT EXISTS session_id VARCHAR;`
Run once at startup inside `get_engine()` in `dependencies.py`. Idempotent.

**Backward compatibility**: Existing rows without `session_id` will have `NULL`. The history API excludes `NULL` session_id rows (old logs before this feature).

---

### New ORM Field (`backend/models/db.py`)

```python
session_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
```

Add a DB index on `session_id` to make `GROUP BY session_id` and `WHERE session_id = ?` queries efficient.

---

### Modified: `QueryRequest` (`backend/api/v1/query.py`)

Add optional `session_id` field:

```python
class QueryRequest(BaseModel):
    question: str
    history: list[HistoryEntry] = []
    session_id: str | None = None
```

---

### Modified: `LogStore.save()` (`backend/logging_service/store.py`)

Accept optional `session_id` parameter:

```python
def save(self, ..., session_id: str | None = None) -> QueryLog:
```

Pass `session_id` to `QueryLog(...)` constructor.

---

## API Response Shapes

### `GET /api/v1/history` — Conversation List

```json
[
  {
    "session_id": "a1b2c3d4-...",
    "started_at": "2026-02-27T14:30:00Z",
    "first_question": "Comment contacter le support tech...",
    "exchange_count": 4
  }
]
```

**Grouping query** (SQLAlchemy equivalent):
```sql
SELECT
  session_id,
  MIN(timestamp) AS started_at,
  (SELECT question_masked FROM query_logs q2
   WHERE q2.session_id = q1.session_id
   ORDER BY timestamp ASC LIMIT 1) AS first_question,
  COUNT(*) AS exchange_count
FROM query_logs q1
WHERE session_id IS NOT NULL
GROUP BY session_id
ORDER BY started_at DESC
LIMIT 50 OFFSET 0
```

### `GET /api/v1/history/{session_id}` — Conversation Detail

```json
{
  "session_id": "a1b2c3d4-...",
  "exchanges": [
    {
      "id": "uuid",
      "timestamp": "2026-02-27T14:30:00Z",
      "question_masked": "Comment contacter le support ?",
      "answer": "Vous pouvez contacter le support via...",
      "guardrail_triggered": null,
      "rejected": false
    }
  ]
}
```

### `DELETE /api/v1/history/{session_id}` — Delete Conversation

Returns `204 No Content` on success. Returns `404` if the `session_id` has no entries.

---

## Frontend Types (`frontend/src/app/services/rag-api.service.ts`)

```typescript
export interface ConversationSummary {
  session_id: string;
  started_at: string;
  first_question: string;
  exchange_count: number;
}

export interface ConversationExchange {
  id: string;
  timestamp: string;
  question_masked: string;
  answer: string;
  guardrail_triggered: string | null;
  rejected: boolean;
}

export interface ConversationDetail {
  session_id: string;
  exchanges: ConversationExchange[];
}
```

---

## Frontend: `ConversationService` (`frontend/src/app/services/conversation.service.ts`)

New service with:

```typescript
@Injectable({ providedIn: 'root' })
export class ConversationService {
  readonly sessionId: string;                    // UUID from sessionStorage
  readonly conversations = signal<ConversationSummary[]>([]);
  readonly selectedConversation = signal<ConversationDetail | null>(null);
  readonly historyOpen = signal(false);

  constructor() { /* init sessionId from sessionStorage */ }

  loadHistory(limit = 50, offset = 0): void { /* GET /api/v1/history */ }
  loadConversation(sessionId: string): void { /* GET /api/v1/history/{id} */ }
  deleteConversation(sessionId: string): void { /* DELETE /api/v1/history/{id} */ }
  toggleHistory(): void { /* toggle historyOpen signal */ }
}
```

---

## New Files

### Backend
- `backend/api/v1/history.py` — new router with 3 endpoints
- DB migration: inline in `dependencies.py` (no new file)

### Frontend
- `frontend/src/app/services/conversation.service.ts` — new service
- `frontend/src/app/components/chat/history-panel/history-panel.ts` — new component
- `frontend/src/app/components/chat/history-panel/history-panel.html`
- `frontend/src/app/components/chat/history-panel/history-panel.scss`

### Modified Files

#### Backend
- `backend/models/db.py` — add `session_id` field to `QueryLog`
- `backend/dependencies.py` — add startup DDL migration
- `backend/api/v1/query.py` — add `session_id` to `QueryRequest`, pass to `LogStore.save()`
- `backend/logging_service/store.py` — add `session_id` param to `save()`
- `backend/api/__init__.py` — register new history router

#### Frontend
- `frontend/src/app/services/rag-api.service.ts` — add 3 new HTTP methods + new types
- `frontend/src/app/components/chat/chat.ts` — inject `ConversationService`, pass `session_id` in `sendMessage()`
- `frontend/src/app/components/chat/chat.html` — add history toggle button + `<app-history-panel>`
- `frontend/src/app/components/chat/chat.scss` — styles for panel overlay
