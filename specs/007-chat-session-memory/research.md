# Research: Chat Session Memory

**Date**: 2026-02-23 | **Feature**: 007-chat-session-memory

## Decision 1 — History format in prompt

**Decision**: Plain-text labeled format — `Utilisateur: ...\nAssistant: ...` per turn

**Rationale**: The existing pipeline uses simple `str.format()` (not LangChain LCEL). Labeled plain-text is directly compatible, avoids any dependency on `ChatPromptTemplate` / `MessagesPlaceholder`, and is well-understood by Qwen 2.5 7B (the target model supports this natively in its chat template).

**Alternatives considered**:
- JSON array: More structured, but adds complexity and is not needed here
- LangChain `MessagesPlaceholder`: Would require migrating `OllamaProvider.generate()` to handle message lists — out of scope and breaking

---

## Decision 2 — History placement in prompt

**Decision**: History goes **before** retrieved context

**Rationale**: Placing history before context gives the LLM conversational grounding before it reads the document chunks. This improves coreference resolution ("Where was *he* born?" → the LLM knows who "he" is before it reads the retrieved passages). History after context would risk the model confusing previous answers with retrieved facts.

**Prompt structure**:
```
[System rules]
Historique de la conversation :
Utilisateur: Q1
Assistant: A1
...

Contexte :
[doc chunks]

Question : [current question]

Réponse :
```

---

## Decision 3 — History window

**Decision**: Cap at **last 6 turns** (12 messages) sent from frontend; backend accepts up to 10 turns per spec

**Rationale**: Qwen 2.5 7B has an ~8k token context window. Token budget breakdown:
- System prompt + template overhead: ~300 tokens
- Retrieved context (top-4 chunks, ~500 chars each): ~500 tokens × 4 = ~2,000 tokens
- Current question: ~200 tokens
- Available for history: ~5,500 tokens → safely fits 6 turns (~100 tokens/turn average)

Research shows 7B models degrade after 6k tokens due to "lost in the middle" effect. 6 turns is a practical sweet spot between context richness and quality.

The spec cap of 10 is the hard maximum; the frontend default sends 6 most recent turns. This is documented as a deviation in DECISIONS.md.

**Alternatives considered**:
- 10 turns (spec default): Acceptable but risks quality degradation; reserved as configurable max
- 2-4 turns: Conservative but may miss useful context for multi-step questions

---

## Decision 4 — Guardrail-rejected messages in history

**Decision**: **Exclude** rejected exchanges from the history sent to the assistant

**Rationale**: Rejected messages (guardrail triggered) should not pollute the conversational context. Including them could reintroduce injection patterns or offensive content indirectly. The frontend filters `messages` by excluding any message that triggered an error (HTTP 400 responses are never added to the `messages` signal — current code already does this).

**Implementation**: No extra backend logic needed. The frontend only adds a message to `messages` after a successful response. Failed requests result in an error state, not a message pair.

---

## Decision 5 — No server-side state / no DB changes

**Decision**: History is entirely **client-side** (Angular `messages` signal), sent in the request body per query

**Rationale**: Per spec and constitution: session-only, no persistence, no DB schema changes. This keeps the implementation minimal and compliant with the Local-First principle (data stays on client, passed over loopback only).

**Alternatives considered**:
- Server-side session store: Would require session IDs, DB table, authentication (out of scope)
- `ConversationChain` with `InMemoryHistory`: Server-side state between requests — violates stateless API design and adds complexity without benefit for single-user local demo
