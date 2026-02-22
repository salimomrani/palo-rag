# PALO RAG — Project Instructions

## Stack

- **Backend**: Python 3.12, FastAPI, LangChain 0.3, ChromaDB (embedded), SQLAlchemy 2, PostgreSQL 16
- **AI**: Ollama local (`qwen2.5:7b` + `mxbai-embed-large`) — `AIProvider` interface swappable
- **Frontend**: Angular 21, PrimeNG v21

## TDD (mandatory — frontend and backend)

**Iron law: no production code without a failing test first.**

Cycle: **RED** → **GREEN** → **REFACTOR**

- Backend: `cd backend && .venv/bin/pytest tests/ -v`
- Frontend: `cd frontend && npx ng test`
- Invoke skill: `superpowers:test-driven-development`

## Workflow Skills (mandatory)

### Spec & planning

- **Feature or large change** → speckit: `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`
- **Small fix** (typo, label, 1-2 lines) → direct edit, no spec
- **Forbidden**: `superpowers:writing-plans` and `superpowers:executing-plans` — speckit replaces them on this project

### Frontend

- Use skill **`frontend-design`** for ALL UI work (components, pages, layouts)
- **Subscriptions**: prefer `toSignal()`; if `subscribe()` unavoidable → `takeUntilDestroyed()`
- Check Angular/PrimeNG APIs with **Context7** before implementing

### Documentation

- Use Context7 for: FastAPI, LangChain, ChromaDB, Angular, SQLAlchemy

## Architecture Constraints (constitution.md)

1. **Local-first**: no data leaves the machine, Ollama only
2. **Traceability**: each query → log entry (PII-masked question, context IDs, score, latency)
3. **Transparent failure**: no hallucinated answers, guardrail refusal = success
4. **Separation of concerns**: RAG / guardrails / eval = independent modules
5. **Reproducible**: 3 commands from a clean checkout
6. **DB**: PostgreSQL 16 via `docker-compose up -d`

## Python Conventions

- Type hints everywhere, Pydantic v2 for schemas
- `pytest` + `pytest-asyncio`, `ruff` for linting
- Env vars via `.env`

## Task Tracking (mandatory)

- Update `specs/<feature>/tasks.md` after each task (`in_progress` → `done`)

## Git

- **Never push directly to `master`** — always open a PR
- Tests must pass before any commit

## Source of Truth

- **Code > plan.md > tasks.md**: code wins on any divergence
- Before any fix: read the actual file, not the plan
- Paths: verify with `find`/`grep` on the repo before writing

## Key Files

- `specs/001-rag-assistant/` — RAG core (spec, plan, tasks)
- `specs/002-angular-eslint-rules/` — Angular ESLint rules
- `specs/003-bulk-delete-docs/` — bulk document deletion
- `specs/004-chat-markdown-render/` — markdown rendering in chat
- `specs/005-frontend-unit-tests/` — frontend unit tests
- `specs/006-cicd-lint-tests/` — GitHub Actions CI pipeline (path filtering)
- `.github/workflows/ci.yml` — 5-job CI: changes + lint + test (backend & frontend)
- `.specify/memory/constitution.md` — 5 architectural principles
- `DECISIONS.md` — all deviations from spec documented here
- `reports/costs.md` — run `/cost` at end of each session
