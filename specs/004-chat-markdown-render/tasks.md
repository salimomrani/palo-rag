# Tasks: Rendu Markdown dans le Chat

**Input**: Design documents from `/specs/004-chat-markdown-render/`
**Branch**: `004-chat-markdown-render`
**Tests**: Not requested — no test tasks generated

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2)

---

## Phase 1: Foundational (Blocking Prerequisite)

**Purpose**: Enregistrer le provider ngx-markdown globalement — requis par les deux user stories

**⚠️ CRITICAL**: Must be complete before any user story work begins

- [x] T001 Add `provideMarkdown()` to providers in `frontend/src/app/app.config.ts` — import from `ngx-markdown`

**Checkpoint**: Provider enregistré, ngx-markdown utilisable dans tous les composants

---

## Phase 2: User Story 1 — Rendu Markdown des messages assistant (P1) 🎯 MVP

**Goal**: Les réponses de l'assistant s'affichent avec le formatage riche (listes, code, titres, gras)

**Independent Test**: Poser une question qui génère une liste ou un bloc de code → vérifier le rendu HTML au lieu des symboles bruts

### Implementation

- [x] T002 [US1] Import `MarkdownComponent` and add to `imports[]` in `frontend/src/app/components/chat/chat.ts`
- [x] T003 [US1] Replace assistant message content in `frontend/src/app/components/chat/chat.html` — wrap in `@if (msg.role === 'assistant')` block using `<markdown [data]="msg.content">`, user messages keep `{{ msg.content }}`
- [x] T004 [P] [US1] Add markdown content styles in `frontend/src/app/components/chat/chat.scss` — scope under `.message.assistant` : code blocks (`pre`, `code`), lists (`ul`, `ol`, `li`), headings (`h1`–`h3`), links (`a`), horizontal rules

**Checkpoint**: Réponses assistant rendues en HTML riche — US1 fully functional

---

## Phase 3: User Story 2 — Messages utilisateur non affectés (P2)

**Goal**: Les messages utilisateur restent en texte brut, aucun symbole Markdown n'est interprété

**Independent Test**: Envoyer `*hello*` → le message affiché doit montrer `*hello*` littéralement

### Implementation

- [x] T005 [US2] Verify in `frontend/src/app/components/chat/chat.html` that user messages use `{{ msg.content }}` without `<markdown>` — no code change required if T003 correctly conditionalizes on `msg.role`

**Checkpoint**: Bulles utilisateur affichées en texte brut — US2 fully functional

---

## Phase 4: Polish

**Purpose**: Validation finale

- [x] T006 [P] Verify lint passes: `cd frontend && npm run lint`
- [x] T007 [P] Manual test: poser une question avec formatage attendu (ex. "Quels endpoints API sont disponibles ?") → vérifier listes et code rendus correctement

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Foundational)**: No dependencies — start immediately
- **Phase 2 (US1)**: Depends on Phase 1 completion
- **Phase 3 (US2)**: Depends on T003 from Phase 2 (même fichier HTML)
- **Phase 4 (Polish)**: Depends on Phase 2 + 3

### Parallel Opportunities

- T004 (SCSS) peut tourner en parallèle de T002+T003 (fichiers différents)
- T006, T007 (polish) peuvent tourner en parallèle

---

## Implementation Strategy

### MVP (Phase 1 + Phase 2 only)

1. Complete Phase 1 — register provider
2. Complete Phase 2 — markdown rendering
3. **STOP and validate**: réponses assistant rendues visuellement
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
- `MarkdownComponent` est un composant standalone — pas de module à importer
- `[data]` binding sur `<markdown>` accepte une string et la rend en HTML
- Scoper les styles markdown sous `.message.assistant` pour éviter les effets de bord sur les bulles utilisateur
