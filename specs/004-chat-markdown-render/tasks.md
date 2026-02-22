# Tasks: Markdown Rendering in Chat

**Input**: Design documents from `/specs/004-chat-markdown-render/`
**Branch**: `004-chat-markdown-render`
**Tests**: Not requested — no test tasks generated

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2)

---

## Phase 1: Foundational (Blocking Prerequisite)

**Purpose**: Register the ngx-markdown provider globally — required by both user stories

**⚠️ CRITICAL**: Must be complete before any user story work begins

- [x] T001 Add `provideMarkdown()` to providers in `frontend/src/app/app.config.ts` — import from `ngx-markdown`

**Checkpoint**: Provider registered, ngx-markdown usable in all components

---

## Phase 2: User Story 1 — Markdown Rendering of Assistant Messages (P1) 🎯 MVP

**Goal**: Assistant responses display with rich formatting (lists, code, headings, bold)

**Independent Test**: Ask a question that generates a list or a code block → verify HTML rendering instead of raw symbols

### Implementation

- [x] T002 [US1] Import `MarkdownComponent` and add to `imports[]` in `frontend/src/app/components/chat/chat.ts`
- [x] T003 [US1] Replace assistant message content in `frontend/src/app/components/chat/chat.html` — wrap in `@if (msg.role === 'assistant')` block using `<markdown [data]="msg.content">`, user messages keep `{{ msg.content }}`
- [x] T004 [P] [US1] Add markdown content styles in `frontend/src/app/components/chat/chat.scss` — scope under `.message.assistant` : code blocks (`pre`, `code`), lists (`ul`, `ol`, `li`), headings (`h1`–`h3`), links (`a`), horizontal rules

**Checkpoint**: Assistant responses rendered as rich HTML — US1 fully functional

---

## Phase 3: User Story 2 — User Messages Unaffected (P2)

**Goal**: User messages remain plain text, no Markdown symbol is interpreted

**Independent Test**: Send `*hello*` → the displayed message must show `*hello*` literally

### Implementation

- [x] T005 [US2] Verify in `frontend/src/app/components/chat/chat.html` that user messages use `{{ msg.content }}` without `<markdown>` — no code change required if T003 correctly conditionalizes on `msg.role`

**Checkpoint**: User bubbles displayed as plain text — US2 fully functional

---

## Phase 4: Polish

**Purpose**: Final validation

- [x] T006 [P] Verify lint passes: `cd frontend && npm run lint`
- [x] T007 [P] Manual test: ask a question with expected formatting (e.g. "What API endpoints are available?") → verify lists and code are rendered correctly

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Foundational)**: No dependencies — start immediately
- **Phase 2 (US1)**: Depends on Phase 1 completion
- **Phase 3 (US2)**: Depends on T003 from Phase 2 (same HTML file)
- **Phase 4 (Polish)**: Depends on Phase 2 + 3

### Parallel Opportunities

- T004 (SCSS) can run in parallel with T002+T003 (different files)
- T006, T007 (polish) can run in parallel

---

## Implementation Strategy

### MVP (Phase 1 + Phase 2 only)

1. Complete Phase 1 — register provider
2. Complete Phase 2 — markdown rendering
3. **STOP and validate**: assistant responses visually rendered
4. Continue Phase 3 → Phase 4

### Full delivery (~7 tasks)

| Phase          | Tasks     | Files touched                 |
| -------------- | --------- | ----------------------------- |
| 1 Foundational | T001      | app.config.ts                 |
| 2 US1          | T002–T004 | chat.ts, chat.html, chat.scss |
| 3 US2          | T005      | chat.html (verify)            |
| 4 Polish       | T006–T007 | —                             |

**Total: 7 tasks — 4 files — pure frontend**

---

## Notes

- No backend changes required
- No new npm dependencies (ngx-markdown already installed)
- `MarkdownComponent` is a standalone component — no module to import
- `[data]` binding on `<markdown>` accepts a string and renders it as HTML
- Scope markdown styles under `.message.assistant` to avoid side-effects on user bubbles
