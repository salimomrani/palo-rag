# Tasks: CI/CD Pipelines — Lint & Tests

**Input**: `specs/006-cicd-lint-tests/`
**Prerequisites**: spec.md ✓ plan.md ✓

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[US1]**: Backend change → backend checks only
- **[US2]**: Frontend change → frontend checks only
- **[US3]**: Full-stack change → both pipelines in parallel

---

## Phase 1: Setup

**Purpose**: Create GitHub Actions structure

- [x] T001 Create `.github/workflows/` directory

---

## Phase 2: User Story 1 — Backend change triggers only backend checks (P1) 🎯 MVP

**Goal**: A commit on `backend/` triggers ruff + pytest via the `changes` job, and nothing else.

**Independent Test**: Open a PR with only a `backend/` file changed — only `backend-lint` and `backend-test` run in the Actions tab.

- [x] T002 [US1] Create `.github/workflows/ci.yml` with `changes` job (dorny/paths-filter@v3) exposing `backend` and `frontend` outputs
- [x] T003 [US1] Add `backend-lint` job in `ci.yml`: `needs: changes`, `if: needs.changes.outputs.backend == 'true'`, `setup-python@v5` (Python 3.12, pip cache), `ruff check .`
- [x] T004 [US1] Add `backend-test` job in `ci.yml`: `needs: changes`, `if: needs.changes.outputs.backend == 'true'`, PostgreSQL 16 service, install deps, `pytest tests/ -v --tb=short`
- [x] T005 [US1] Add `backend/ruff.toml`: `target-version = "py312"`, E/F/I rules, exclude `chroma_data` and `scripts`

**Checkpoint**: Backend pipeline triggered and passing on a PR touching only `backend/`.

---

## Phase 3: User Story 2 — Frontend change triggers only frontend checks (P1)

**Goal**: A commit on `frontend/` triggers ESLint + vitest, and nothing else.

**Independent Test**: Open a PR with only a `frontend/` file changed — only `frontend-lint` and `frontend-test` run in the Actions tab.

- [x] T006 [US2] Add `frontend-lint` job in `ci.yml`: `needs: changes`, `if: needs.changes.outputs.frontend == 'true'`, `setup-node@v4` (Node 22, npm cache), `npm run lint`
- [x] T007 [US2] Add `frontend-test` job in `ci.yml`: `needs: changes`, `if: needs.changes.outputs.frontend == 'true'`, `setup-node@v4` (Node 22, npm cache), `npm test -- --watch=false`

**Checkpoint**: Frontend pipeline triggered and passing on a PR touching only `frontend/`.

---

## Phase 4: User Story 3 — Full-stack change triggers both pipelines (P2)

**Goal**: A commit touching both `backend/` and `frontend/` triggers all four jobs in parallel.

**Independent Test**: Open a PR modifying both directories — four jobs appear simultaneously in the Actions tab.

- [ ] T008 [US3] Empirically validate that all four jobs (`backend-lint`, `backend-test`, `frontend-lint`, `frontend-test`) run in parallel on a full-stack PR (verify in Actions tab after T009)

**Checkpoint**: All four jobs run simultaneously.

---

## Phase 5: Polish

- [ ] T009 [P] Open PR `006-cicd-lint-tests` → `master` to trigger CI validation
- [ ] T010 Validate SC-003: pipeline duration < 5 min (check in Actions history with warm cache)

---

## Dependencies & Execution Order

- **T001** → T002 → T003, T004, T005 (parallelizable after T002)
- **T002** → T003 → T004 (sequential within US1, same file)
- **T006, T007**: parallelizable (different jobs, same file)
- **T008** requires T004 + T007 (US1 + US2 complete)

### MVP

T001 → T002 → T003 → T004 → T005: backend pipeline operational.

---

## Notes

- `dorny/paths-filter@v3` is the standard approach for conditional path filtering in a single file.
- Backend tests use SQLite in-memory — the PostgreSQL service in CI exists for future integration tests but is not used by current tests.
- Ollama is not available in CI — all Ollama calls are mocked in tests (verified).
