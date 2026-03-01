# Feature Specification: Persistent Chat History

**Feature Branch**: `010-persistent-chat-history`
**Created**: 2026-02-27
**Status**: Draft
**Input**: User description: "Ajouter la possibilité d'avoir un historique de chat persistant multi-sessions — les conversations sont sauvegardées en base de données PostgreSQL, accessibles après rechargement de page. Le frontend affiche un panneau listant les conversations passées avec possibilité de les relire."

## User Scenarios & Testing *(mandatory)*

### User Story 1 — View Past Conversations After Page Reload (Priority: P1)

A user who has closed or reloaded the page can open the chat history panel and see a chronological list of their past conversations, each showing the first question asked and the date/time of the session. They can expand any past conversation to read all the exchanges.

**Why this priority**: This is the core value of the feature — without it, "persistent" history doesn't exist. All other stories depend on conversations being saved and retrievable.

**Independent Test**: Can be tested by sending 2 questions, reloading the page, opening the history panel, and verifying the previous conversation appears with both exchanges visible.

**Acceptance Scenarios**:

1. **Given** a user has completed one or more queries in a previous session, **When** they reload the page and open the history panel, **Then** they see a list of past conversations ordered by most recent first
2. **Given** a past conversation is listed, **When** the user clicks on it, **Then** they see all the question-answer pairs from that session in chronological order
3. **Given** the user has no prior conversations, **When** they open the history panel, **Then** they see an empty state message ("No conversation history yet")
4. **Given** a guardrail-blocked query exists in a session, **When** the user views that conversation, **Then** the blocked exchange is visible with the refusal message shown

---

### User Story 2 — Conversations Grouped Automatically by Session (Priority: P2)

As a user sends queries during a session, they are automatically grouped into a single conversation entry — no explicit save action required. A new session (page load) starts a new conversation group.

**Why this priority**: Grouping by session makes history scannable. A flat list of individual queries is unusable at scale; conversation grouping gives meaning to "history".

**Independent Test**: Can be tested by asking 3 questions in one session, reloading, asking 2 more, then opening history — 2 distinct conversation groups must appear, not 5 individual items.

**Acceptance Scenarios**:

1. **Given** a user sends multiple queries in a single session, **When** they view the history, **Then** all those queries appear under a single conversation entry (not as separate items)
2. **Given** a user reloads the page, **When** they send new queries, **Then** those queries appear under a new, separate conversation entry
3. **Given** a conversation has just been created, **When** the user opens history mid-session, **Then** the current in-progress session also appears in the list with its exchanges so far

---

### User Story 3 — Delete a Past Conversation (Priority: P3)

A user who wants to clean up their history can delete a specific past conversation from the history panel. The conversation and all its exchanges are permanently removed from the list.

**Why this priority**: Privacy control. Users should be able to manage their local history. Lower priority than viewing, but important for a complete history experience.

**Independent Test**: Can be tested by having 2 conversations in history, deleting one, and verifying only 1 remains and does not reappear on reload.

**Acceptance Scenarios**:

1. **Given** a past conversation is listed, **When** the user clicks delete and confirms, **Then** the conversation is removed from the history panel immediately and does not reappear after reload
2. **Given** a user clicks delete, **When** a confirmation prompt is shown, **Then** the conversation is only removed after confirmation (not on accidental click)

---

### Edge Cases

- What happens when a session contains only guardrail-rejected queries? → The session still appears in history; rejected exchanges are shown with the refusal message
- What happens if many conversations accumulate over time? → History lists the 50 most recent sessions by default; a "load more" control is available for older sessions
- What happens to history when the database is reset? → History is empty; no error is shown; the empty state message is displayed
- What happens when a query is still streaming when the user opens history? → The in-progress exchange is omitted from the history view until it completes successfully

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST assign a unique session identifier to each browser session at page load; this identifier groups all queries from that session into a single conversation
- **FR-002**: Every query submitted during a session MUST be persisted with its session identifier, so it can be retrieved and grouped after page reload
- **FR-003**: The chat interface MUST provide a history panel (accessible via a toggle button) that lists past conversations without leaving the chat view
- **FR-004**: The history panel MUST display each conversation as a summary showing: session start date/time and the first question of the session (truncated to 80 characters)
- **FR-005**: Conversations MUST be ordered by most recent first in the history panel
- **FR-006**: Clicking a conversation in the history panel MUST show all question-answer pairs from that session in chronological order (read-only)
- **FR-007**: The history panel MUST display an empty state message when no prior conversations exist
- **FR-008**: The current in-progress session MUST appear in the history list alongside past sessions
- **FR-009**: The user MUST be able to delete a conversation from the history panel; deletion requires a confirmation step and permanently removes all associated exchanges from storage
- **FR-010**: The history panel MUST list at most 50 conversations by default; if more exist, a "load more" control must be available
- **FR-011**: All history data MUST remain local — no data is sent to external services (Principle I)
- **FR-012**: The history feature MUST NOT affect the behavior or performance of the existing query flow for users who do not interact with the history panel (Principle IV)

### Key Entities

- **Conversation**: A group of exchanges from a single browser session, identified by a session ID, with a start timestamp. Persisted on the backend.
- **Exchange**: A single question-answer pair within a conversation, preserving the masked question, the assistant's answer, and metadata (timestamp, guardrail status).
- **SessionId**: A UUID generated client-side at page load, passed with each query, used to group exchanges into a conversation on the backend. Not linked to any user identity.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A conversation from a previous browser session is visible in the history panel within 1 second of opening the panel
- **SC-002**: All queries sent during a session appear under a single conversation entry — verified across 10+ exchanges per session in 100% of test cases
- **SC-003**: History panel correctly lists up to 50 past conversations; users can load additional sessions without error
- **SC-004**: Deleting a conversation removes it permanently — it does not reappear after page reload in 100% of test cases
- **SC-005**: All existing query acceptance scenarios (from spec 001 and 007) continue to pass without regression

## Assumptions

- Session identity is client-side only (UUID in sessionStorage) — no user authentication is involved; history is local to the machine running the app
- The masked question (`question_masked`) is what is stored and displayed in history — users may see "[masked]" placeholders where PII was detected; this is acceptable and by design (Principle I)
- A "session" corresponds to one browser tab lifecycle (page load → page unload); multi-tab synchronization is out of scope
- History is read-only — users can view past conversations but cannot resume or edit them
- The 50-conversation limit is sufficient for the demo context; no archiving or export is required
- The existing `query_logs` table will be extended with a `session_id` column to link queries to conversations; no entirely new conversation-specific tables are introduced unless planning identifies a compelling reason
