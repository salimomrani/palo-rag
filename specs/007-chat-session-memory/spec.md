# Feature Specification: Chat Session Memory

**Feature Branch**: `007-chat-session-memory`
**Created**: 2026-02-23
**Status**: Draft
**Input**: User description: "Chat Conversation History (session memory) — Le chat doit maintenir un historique des échanges de la session en cours. Chaque requête envoyée au LLM inclut les N derniers tours (user/assistant) comme contexte conversationnel. L'historique est réinitialisé au rechargement de page (pas de persistance). Backend : QueryRequest accepte un champ history optionnel (liste de {role, content}). RAGPipeline inclut l'historique dans le prompt quand présent. Frontend : le composant Chat construit l'historique depuis le signal messages et le passe à l'API. Cap : 10 derniers échanges (20 messages) maximum."

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Ask a Follow-up Question (Priority: P1)

A user who has already asked a question in the chat can ask a follow-up that refers to a previous answer — without repeating the context. The assistant understands the reference and gives a coherent, contextual answer.

**Why this priority**: This is the core value of session memory. Without it, every question is independent and multi-turn dialogue is impossible.

**Independent Test**: Can be tested by sending a first question ("What is the onboarding process?"), then a follow-up ("Who is responsible for step 2?") and verifying the assistant answers using context from the first exchange — without the user repeating the topic.

**Acceptance Scenarios**:

1. **Given** a user has asked a question and received an answer, **When** the user asks a follow-up referencing "the process above" or "step 2", **Then** the assistant's response is contextually relevant to the previous exchange
2. **Given** a user has had a multi-turn exchange, **When** they ask a new question on a completely different topic, **Then** the assistant answers the new topic without being confused by old context
3. **Given** a user starts a brand new session (page reload), **When** they ask a follow-up from a previous session, **Then** the assistant has no memory of the previous session and answers independently

---

### User Story 2 — Clear Conversation and Start Fresh (Priority: P2)

A user who wants to start a new, independent conversation can clear the current session history, resetting the context without reloading the page.

**Why this priority**: Provides explicit control over context. Useful when switching topics or wanting a clean slate without page reload.

**Independent Test**: Can be tested by having a conversation, clicking "Clear", then asking a follow-up from the previous exchange — the assistant should show no awareness of the previous messages.

**Acceptance Scenarios**:

1. **Given** an active conversation, **When** the user clicks the clear/reset button, **Then** all messages are removed from the chat view and subsequent queries are sent without any history
2. **Given** the chat has been cleared, **When** a new question is submitted, **Then** the assistant responds as if it is the first question of a new session

---

### User Story 3 — Long Conversations Are Handled Gracefully (Priority: P3)

A user engaged in a long conversation does not experience degraded performance or errors when the number of exchanges exceeds the memory window. The oldest exchanges are silently dropped while recent context is preserved.

**Why this priority**: Edge case that protects system stability. Without this, very long conversations could cause failures.

**Independent Test**: Can be tested by simulating a conversation with more than 10 exchanges and verifying the 11th query succeeds and references recent (not oldest) context correctly.

**Acceptance Scenarios**:

1. **Given** a conversation with more than 10 exchanges, **When** a new question is submitted, **Then** the request succeeds and only the most recent 10 exchanges are included as context
2. **Given** the history window is at capacity, **When** older messages are dropped, **Then** the user sees no error and the chat continues normally

---

### Edge Cases

- What happens when the conversation history contains a rejected query (guardrail triggered)? → Rejected exchanges are excluded from history sent to the assistant; only successful exchanges are included
- What happens if a page reload occurs mid-conversation? → All session history is lost; next query is treated as a first message with no prior context
- What happens when the combined history and current question would exceed input limits? → The oldest exchanges are dropped first until the request fits within acceptable bounds

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The chat interface MUST maintain an in-memory record of all user questions and assistant answers for the current browser session
- **FR-002**: Each query submitted to the assistant MUST include the most recent exchanges from the current session as conversational context
- **FR-003**: The number of exchanges included as context MUST be capped at 10 (20 messages: 10 user + 10 assistant) to limit context size; older exchanges MUST be dropped silently
- **FR-004**: Session history MUST be reset automatically when the user reloads or navigates away from the page
- **FR-005**: The chat interface MUST provide a way for users to explicitly clear the conversation history and start a fresh session without reloading the page
- **FR-006**: The history field in a query MUST be optional; a query with no history MUST behave identically to the current system
- **FR-007**: Exchanges where the assistant's response was blocked by a guardrail MUST NOT be included in the history sent to the assistant
- **FR-008**: The assistant MUST use the conversational history to produce contextually coherent follow-up answers

### Key Entities

- **ConversationTurn**: A single exchange in the session, composed of one user message and one assistant response; identified by role and content; ephemeral (session-scoped only)
- **SessionHistory**: An ordered, capped list of ConversationTurns maintained client-side for the duration of a browser session; discarded on page unload

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A follow-up question referencing the previous answer produces a contextually relevant response in 100% of test cases on a 2-turn conversation
- **SC-002**: Queries submitted with session history complete within the same response time bounds as queries without history (under 10 seconds at 95th percentile on the local stack)
- **SC-003**: A conversation with 15 consecutive exchanges produces no errors; only the 10 most recent exchanges are used as context
- **SC-004**: After clearing the conversation, the next query returns a response with no reference to previous exchanges
- **SC-005**: All existing query acceptance scenarios (from spec 001) continue to pass without regression

## Assumptions

- Session history is stored in client memory only — no server-side storage, no database changes
- Only successful assistant responses (non-rejected) are included in history
- The assistant's quality may vary depending on the LLM model's context window; the 10-exchange cap is a reasonable default for the target model
- Single-user, single-tab use case — no cross-tab synchronization is required
