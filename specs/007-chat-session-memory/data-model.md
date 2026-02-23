# Data Model: Chat Session Memory

**Date**: 2026-02-23 | **Feature**: 007-chat-session-memory

## No New Persistent Entities

This feature introduces **no database schema changes**. All history is ephemeral and lives in the Angular `messages` signal on the client side.

---

## Request Shape (new field in existing model)

### `QueryRequest` — extended

```
QueryRequest
├── question: str              (existing, required)
└── history: list[HistoryEntry] (new, optional, default=[])

HistoryEntry
├── role: "user" | "assistant"  (required)
└── content: str                (required)
```

**Constraints**:
- `history` is optional — default empty list preserves backward compatibility
- Maximum accepted length: 10 entries (5 turns = 10 messages) per request
- `role` must be `"user"` or `"assistant"` — enforced by Pydantic `Literal`
- `content` must be non-empty string

---

## Client-Side Data (Angular)

### `Message` — existing interface (no changes)

```
Message
├── id: string
├── role: 'user' | 'assistant'
├── content: string
├── sources?: Source[]
├── confidence?: number
├── lowConfidence?: boolean
└── streaming?: boolean
```

### `HistoryEntry` — new interface (frontend only)

```
HistoryEntry
├── role: 'user' | 'assistant'
└── content: string
```

**Build rule**: Built from `messages` signal before each `sendMessage()`:
- Exclude the last 2 entries (current user message + streaming placeholder)
- Exclude messages with `streaming: true`
- Take last 12 entries (6 turns)
- Map each `Message` to `HistoryEntry` with `{ role, content }`

---

## Prompt Augmentation (internal, no API surface)

When `history` is non-empty, a new prompt template is used:

```
RAG_PROMPT_WITH_HISTORY
├── {history} — formatted as "Utilisateur: ...\nAssistant: ..." per turn
├── {context} — retrieved document chunks (unchanged)
└── {question} — current question (unchanged)
```

When `history` is empty, the existing `RAG_PROMPT` is used unchanged.
