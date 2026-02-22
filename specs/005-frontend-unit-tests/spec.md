# Feature Specification: Frontend Unit Tests

**Feature Branch**: `005-frontend-unit-tests`
**Created**: 2026-02-20
**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Test Suite Configuration and Execution (Priority: P1)

A developer can launch the test suite with a single command from the frontend folder and obtain a clear report showing which tests pass or fail.

**Why this priority**: Without a working test infrastructure, no test can be written or executed. This is the blocking prerequisite.

**Independent Test**: Run `npm test` in the frontend → the command runs without configuration error and displays a results report.

**Acceptance Scenarios**:

1. **Given** a freshly cloned repository, **When** the developer runs the test command, **Then** the suite starts without configuration error and a report is displayed
2. **Given** an intentionally failing test, **When** the suite runs, **Then** the failure is clearly identified with the test name and the cause

---

### User Story 2 — Chat Component Tests (Priority: P2)

The key behaviours of the Chat component are covered by tests: message sending, display of suggestion chips, and Markdown rendering of assistant responses.

**Why this priority**: Chat is the main component of the application — its regressions have the greatest user impact.

**Independent Test**: Run only the Chat tests → all pass, critical behaviours are verified without launching the application.

**Acceptance Scenarios**:

1. **Given** the Chat component initialised, **When** the conversation is empty, **Then** the suggestion chips are visible
2. **Given** chips visible, **When** the user clicks a chip, **Then** the message is sent and the chips disappear
3. **Given** the Chat component, **When** `sendMessage()` is called with an empty prompt, **Then** no message is added
4. **Given** an assistant response received, **When** the content is displayed, **Then** assistant messages use rich rendering and user messages remain plain text
5. **Given** the component in loading state, **When** `isLoading` is true, **Then** the send button is disabled

---

### User Story 3 — Ingest Component Tests (Priority: P3)

The selection and bulk-delete behaviours of the Ingest component are covered: individual selection, full selection, delete button state.

**Why this priority**: Ingest contains complex state logic (derived signals, mutable Set) — tests protect against regressions in this logic.

**Independent Test**: Run only the Ingest tests → selection and deletion scenarios pass without launching the API.

**Acceptance Scenarios**:

1. **Given** a list of documents, **When** the user checks a row, **Then** `selectedIds` contains that ID and `noneSelected` becomes false
2. **Given** all documents checked, **When** `allSelected` is evaluated, **Then** it returns true
3. **Given** a partial selection, **When** `someSelected` is evaluated, **Then** it returns true and `allSelected` returns false
4. **Given** no selection, **When** the state is evaluated, **Then** the "Delete Selection" button is disabled
5. **Given** an active selection, **When** `toggleAll()` is called, **Then** all documents are selected; a second call clears the selection

---

### Edge Cases

- What happens if a test depends on a real HTTP service? → HTTP calls must be intercepted/mocked, never actually executed
- What happens if a component uses `inject()`? → Dependency injection must work in the test context
- What happens if Angular signals do not update synchronously in tests? → Signal assertions must be made after change propagation

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The test suite MUST run with a single command without additional manual configuration
- **FR-002**: Tests MUST be isolated — no test must depend on the state of another test
- **FR-003**: Network calls (RAG API) MUST be intercepted and replaced with mock data in all tests
- **FR-004**: Chat component tests MUST cover: empty state (chips), message sending, empty prompt validation, assistant/user distinction, loading state
- **FR-005**: Ingest component tests MUST cover: individual selection, computed signals (`allSelected`, `someSelected`, `noneSelected`), `toggleAll()`, delete button state
- **FR-006**: Tests MUST run in under 30 seconds for the entire suite
- **FR-007**: A coverage report MUST be available on demand (separate command)

### Assumptions

- The test tool (Vitest) is already installed — only configuration is missing
- Components are standalone Angular 21 with signals and OnPush — test utilities must support this
- No database or real server is required for unit tests

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The test command runs in under 30 seconds on a standard developer workstation
- **SC-002**: 100% of the acceptance scenarios defined in the user stories are covered by at least one test
- **SC-003**: 0 real network calls made during test execution
- **SC-004**: Each test can be run independently and produces the same result
- **SC-005**: A failing test clearly identifies the component, the scenario, and the expected vs received value
