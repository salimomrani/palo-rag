# Feature Specification: CI/CD Pipelines — Lint & Tests

**Feature Branch**: `006-cicd-lint-tests`
**Created**: 2026-02-22
**Status**: Draft
**Input**: Minimal CI/CD pipelines for tests and lint — GitHub Actions with path filtering: if only the frontend changes, only frontend jobs (ESLint + vitest) run; if only the backend changes, only backend jobs (ruff + pytest) run. No deployment.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Backend change triggers only backend checks (Priority: P1)

A developer modifies a Python file in `backend/`. The pipeline detects the change, runs only the backend lint and tests, and blocks the PR if either fails.

**Why this priority**: Most common case in backend development; blocking broken commits is the core value of CI.

**Independent Test**: Open a PR with only `backend/` files changed — only the backend jobs appear in the Actions tab.

**Acceptance Scenarios**:

1. **Given** a PR with changes only in `backend/`, **When** the PR is opened or updated, **Then** only `backend-lint` and `backend-test` jobs run.
2. **Given** a Python file with a style violation, **When** the lint job runs, **Then** the pipeline fails and blocks the merge.
3. **Given** a failing backend test, **When** the test job runs, **Then** the pipeline fails and blocks the merge.

---

### User Story 2 - Frontend change triggers only frontend checks (Priority: P1)

A developer modifies an Angular component in `frontend/`. Only the frontend lint and tests run; backend jobs are not triggered.

**Why this priority**: Same priority as backend P1 — path filtering is the core of this feature.

**Independent Test**: Open a PR with only `frontend/` files changed — only the frontend jobs appear in the Actions tab.

**Acceptance Scenarios**:

1. **Given** a PR with changes only in `frontend/`, **When** the PR is opened or updated, **Then** only `frontend-lint` and `frontend-test` jobs run.
2. **Given** an ESLint rule violation in the frontend code, **When** the lint job runs, **Then** the pipeline fails and blocks the merge.
3. **Given** a failing vitest test, **When** the test job runs, **Then** the pipeline fails and blocks the merge.

---

### User Story 3 - Full-stack change triggers both pipelines (Priority: P2)

A developer modifies both `backend/` and `frontend/` in the same PR. All four blocking jobs run in parallel.

**Why this priority**: Less frequent but necessary to ensure full project consistency.

**Independent Test**: Open a PR touching both directories — four jobs (backend-lint, backend-test, frontend-lint, frontend-test) appear simultaneously in the Actions tab.

**Acceptance Scenarios**:

1. **Given** a PR modifying both `backend/` and `frontend/`, **When** the PR is opened, **Then** all four blocking jobs run in parallel.

---

### User Story 4 - Non-blocking code review runs on every push (Priority: P2)

On every push touching `backend/` or `frontend/`, an extended analysis job runs with a broader rule set. It reports findings as GitHub annotations but never blocks the merge.

**Why this priority**: Developers get actionable feedback without CI becoming a gate that slows down iteration.

**Independent Test**: Introduce a complexity violation — the review job appears as a warning in the Actions tab, the PR remains mergeable.

**Acceptance Scenarios**:

1. **Given** a push with backend changes, **When** the pipeline runs, **Then** `backend-review` executes and its result (pass or fail) does not affect mergeability.
2. **Given** a push with frontend changes, **When** the pipeline runs, **Then** `frontend-review` executes and its result does not affect mergeability.
3. **Given** a code quality issue detected by the review job, **When** the job completes, **Then** findings appear as inline annotations in the PR diff.

---

### Edge Cases

- What happens if only CI config files (`.github/workflows/`) are modified? → The `changes` job runs but no path filter matches, so no downstream jobs execute.
- What happens if the test database is unavailable? → The `backend-test` job fails explicitly with a readable error message.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST trigger only backend jobs when files under `backend/` are modified.
- **FR-002**: The system MUST trigger only frontend jobs when files under `frontend/` are modified.
- **FR-003**: The system MUST run lint and tests as two separate jobs for each scope (backend and frontend).
- **FR-004**: The system MUST block PR merge if at least one blocking job fails.
- **FR-005**: The system MUST cache dependencies to reduce pipeline execution time.
- **FR-006**: The system MUST NOT include any deployment step.
- **FR-007**: The system MUST provide readable error messages on failure (lint or test).
- **FR-008**: The system MUST run a non-blocking code review job on every push that touches backend or frontend files.
- **FR-009**: The code review job MUST report findings as inline annotations in the PR but MUST NOT prevent merge.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A PR touching only the frontend triggers no backend jobs (and vice versa) — verifiable in the Actions history.
- **SC-002**: A commit breaking a test or a style rule is blocked before merge in 100% of cases.
- **SC-003**: Total pipeline duration (lint + tests) does not exceed 5 minutes with a warm dependency cache.
- **SC-004**: All four blocking jobs run in parallel when both scopes are modified.
- **SC-005**: The non-blocking review job never prevents a PR from being merged, even when it reports findings.
