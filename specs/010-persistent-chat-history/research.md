# Research: Persistent Chat History

**Feature**: 010-persistent-chat-history
**Date**: 2026-02-27

---

## Decision 1: Schema Change Strategy — Extend `query_logs` vs New Table

**Decision**: Extend existing `query_logs` table with a nullable `session_id VARCHAR` column.

**Rationale**:
- The spec assumption (and the simplest path) is to tag each `QueryLog` row with a `session_id`
- All query-level data already stored in `query_logs`: `question_masked`, `answer`, `timestamp`, `guardrail_triggered` — everything needed for history display
- A new `conversations` table would add join complexity with no added value for this read-only history feature
- Foreign key overhead is unnecessary; session_id is a client-generated UUID with no server-side lifecycle management

**Alternatives Considered**:
- New `conversations` + `conversation_messages` tables: richer model for future features (e.g., resume conversation, name a conversation), but overkill for read-only display in a single-user demo
- Reuse existing `query_logs` without schema change (infer session from timestamp proximity): brittle and unreliable across reloads

**Constraint**: `Base.metadata.create_all(engine)` only creates missing tables, not new columns on existing tables. A startup DDL migration (`ALTER TABLE query_logs ADD COLUMN IF NOT EXISTS session_id VARCHAR;`) is needed — idempotent, no Alembic required.

---

## Decision 2: Session Identity — Client-Generated UUID in sessionStorage

**Decision**: Generate a UUID v4 in the Angular app at page load, store it in `sessionStorage`, send it with every query as `session_id`.

**Rationale**:
- `sessionStorage` is per-tab, per-page-lifecycle — matches the spec's definition of "session" (page load → page unload)
- UUID generation is available natively via `crypto.randomUUID()` (already used in chat component)
- No server-side session management required (no auth in scope)
- The session_id travels from frontend → `QueryRequest` → `LogStore.save()` → DB

**Alternatives Considered**:
- Server-generated session_id: requires an extra API call at app init — adds latency, unnecessary complexity
- `localStorage`: would persist across tabs/reloads and blur conversation boundaries

---

## Decision 3: History API Shape — Grouped Sessions

**Decision**: Two new endpoints:
1. `GET /api/v1/history` — returns a list of conversation summaries (one per `session_id`), each with: `session_id`, `started_at` (first query timestamp), `first_question` (truncated), `exchange_count`
2. `GET /api/v1/history/{session_id}` — returns all exchanges for one session ordered by timestamp ASC
3. `DELETE /api/v1/history/{session_id}` — removes all `query_logs` rows for a given `session_id`

**Rationale**:
- Separation between "list" and "detail" is standard REST and matches the two-step UX: list → click → expand
- Grouping on the backend avoids sending all raw log rows to the frontend and doing expensive client-side grouping
- SQLAlchemy subquery + GROUP BY is sufficient for the demo scale (no need for a materialized view)

**Alternatives Considered**:
- Single endpoint returning all logs grouped by session_id: too much data transferred upfront
- GraphQL: overkill for this feature

---

## Decision 4: Frontend UI — Slide-in History Panel in Chat View

**Decision**: Add a slide-in sidebar panel within the `/chat` route. A toggle button ("Historique") is added to the chat header. The panel overlays from the left when open.

**Rationale**:
- The nav already has 4 tabs (Chat, Ingest, Logs, Éval); a 5th top-nav item for history would clutter the nav
- History is contextual to chat — it makes sense to access it within the chat view
- A slide-in sidebar (the "drawer" pattern) is a well-understood UX pattern, commonly used in chat apps (e.g., ChatGPT sidebar)
- Keeps the routing table unchanged; no new route or lazy-loaded component needed
- No changes to `app.html` or `app.routes.ts`

**Alternatives Considered**:
- Dedicated `/history` route: clean separation but adds nav tab clutter and breaks chat context
- Inline expansion below chat: would push chat messages down — disorienting UX

---

## Decision 5: New Angular Service — `ConversationService`

**Decision**: Create a new `ConversationService` (injectable, `providedIn: 'root'`) responsible for:
1. Generating and persisting the current `sessionId` (via `sessionStorage`)
2. Fetching conversation list and detail from the API
3. Deleting a conversation

The `RagApiService` is extended with the three new HTTP methods. `ConversationService` wraps `RagApiService` calls and exposes signals for the history panel.

**Rationale**:
- `RagApiService` already owns all HTTP calls — consistent pattern to extend it
- `ConversationService` handles session lifecycle and state management for the history panel — clean separation per Principle IV
- Signals-based state (consistent with the existing chat component pattern)

---

## Decision 6: Guardrail-Rejected Queries in History

**Decision**: Include guardrail-rejected exchanges in the history display. The answer field for a rejected query will be the `guardrail_triggered` reason code, displayed as an error message in the UI.

**Rationale**: The spec (US1 Acceptance Scenario 4) explicitly requires rejected exchanges to appear in history. The `query_logs` table already stores rejected entries with `answer: ""` and `guardrail_triggered: "guardrail:xxx"`. The frontend history panel renders these with a visual distinction (e.g., red label).

---

## Decision 7: No Alembic — Startup DDL Migration

**Decision**: Add a startup migration function called once in `get_engine()` (in `dependencies.py`) that runs:
```sql
ALTER TABLE query_logs ADD COLUMN IF NOT EXISTS session_id VARCHAR;
```

**Rationale**: The project uses `Base.metadata.create_all()` rather than Alembic. Adding Alembic as a new dependency would exceed the scope of this feature. The `IF NOT EXISTS` guard makes the DDL safe to run on every startup.

**Risk**: If the DB engine doesn't support `IF NOT EXISTS` for `ADD COLUMN` (PostgreSQL 9.6+) — not a concern here since the project uses PostgreSQL 16.
