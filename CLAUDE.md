# PALO RAG — Project Instructions

## Stack

- **Backend**: Python 3.12, FastAPI, LangChain 0.3, ChromaDB (embedded), SQLAlchemy 2, PostgreSQL 16
- **AI**: Ollama local (`qwen2.5:7b` + `mxbai-embed-large`) — `AIProvider` interface swappable
- **Frontend**: Angular 21, PrimeNG v21

## Workflow (mandatory)

- **Feature or large change** → see `.claude/skills/speckit-superpowers-workflow.md`
- **Frontend work** → see `.claude/skills/angular-conventions.md`
- **Python/backend** → see `.claude/skills/python-conventions.md`
- **Small fix** (typo, label, 1-2 lines) → direct edit, no spec

## TDD (mandatory)

**Iron law: no production code without a failing test first.** RED → GREEN → REFACTOR

- Backend: `cd backend && .venv/bin/pytest tests/ -v`
- Frontend: `cd frontend && npm test -- --watch=false`
- Skill: `superpowers:test-driven-development`

## Git

- Never push directly to `master` — always open a PR
- Tests must pass before any commit
- Update `specs/<feature>/tasks.md` after each task

## Architecture (see `.specify/memory/constitution.md` for full details)

1. Local-first — Ollama only, no data leaves the machine
2. Traceability — every query logged (PII-masked)
3. Transparent failure — no hallucinated answers
4. Separation of concerns — RAG / guardrails / eval = independent modules

## Source of Truth

- **Code > plan.md > tasks.md** — code wins on divergence
- Deviations from spec → document in `DECISIONS.md`
- Context7 for library docs (FastAPI, LangChain, Angular, SQLAlchemy, ChromaDB)
