# Feature Specification: Angular ESLint — Best Practices Rules

**Feature Branch**: `002-angular-eslint-rules`
**Created**: 2026-02-19
**Status**: Draft
**Input**: User description: "Add ESLint with the best Angular rules to the frontend: ban on nested subscribes, $ convention for Observables, Angular-specific rules, strict TypeScript rules, general quality rules. Integrate into the CI workflow (npm run lint must pass with 0 errors)."

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Automatic Detection of Quality Violations (Priority: P1)

As a developer, when I write code that violates a quality rule (nested subscribe, use of `any`, Observable without `$`, etc.), I want to be immediately informed with the file, the line, and the rule concerned, so I can fix the problem before committing.

**Why this priority**: This is the core value of the feature. Without reliable violation detection, the other user stories make no sense.

**Independent Test**: Introduce a known violation (e.g. subscribe inside a subscribe) → run the lint command → verify the error is reported with file + line + description.

**Acceptance Scenarios**:

1. **Given** code containing a `subscribe()` nested inside another `subscribe()`, **When** the lint command is run, **Then** an error is reported indicating the file, the line, and the violated rule.
2. **Given** an Observable property named without the `$` suffix (e.g. `data` instead of `data$`), **When** the lint command is run, **Then** an error indicates the naming convention is not followed.
3. **Given** the use of the `any` type in a TypeScript file, **When** the lint command is run, **Then** an error is reported.
4. **Given** code that conforms to all rules, **When** the lint command is run, **Then** no errors are reported and the command exits successfully.

---

### User Story 2 — Zero Lint Errors on Existing Code (Priority: P1)

As a developer, I want the current Angular code of the project to comply with all defined rules, so that the baseline is clean and each new violation is clearly identifiable as a regression.

**Why this priority**: If existing code contains uncorrected violations, the lint command cannot serve as a CI gate and loses all value.

**Independent Test**: Run the lint command on the project — it must exit with code 0 and display "0 errors, 0 warnings".

**Acceptance Scenarios**:

1. **Given** the existing frontend project code, **When** the lint command is run after configuration and fixes, **Then** the result shows 0 errors and 0 warnings.
2. **Given** a partial fix of the code, **When** the lint command is run, **Then** only the remaining violations are reported (no false positives).

---

### User Story 3 — Integration into the CI Workflow (Priority: P2)

As a tech lead, I want the lint command to be integrated into the development workflow (script `npm run lint`) and to fail with a non-zero exit code on violation, so as to block commits or pipelines containing non-compliant code.

**Why this priority**: Without CI integration, compliance relies solely on individual discipline and is not guaranteed.

**Independent Test**: Introduce a violation → run `npm run lint` → verify the command returns a non-zero exit code (failure).

**Acceptance Scenarios**:

1. **Given** a configured `npm run lint` script, **When** code is compliant, **Then** the command returns exit code 0.
2. **Given** a configured `npm run lint` script, **When** a violation is present, **Then** the command returns a non-zero exit code and lists the violations.
3. **Given** the lint command, **When** it runs across the entire project, **Then** it completes in under 30 seconds.

---

### Edge Cases

- What happens if an auto-generated file (build, node_modules) contains violations? → These files must be automatically excluded from analysis.
- How to handle the rare legitimate cases where `any` is unavoidable (third-party library interop without types)? → A local exception directive must be available but visible in code review.
- What happens if a rule generates false positives on valid Angular code? → The rule must be configurable as a warning rather than an error, without disabling it entirely.
- Should an Observable returned by a method also carry the `$`? → Yes, the convention applies to properties and to methods whose return type is Observable.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST detect and report as an error any `subscribe()` called inside the callback of another `subscribe()`.
- **FR-002**: The system MUST enforce the `$` naming convention (dollar suffix) for all class properties whose type is `Observable<T>`.
- **FR-003**: The system MUST enforce the `$` naming convention for all methods whose return type is `Observable<T>`.
- **FR-004**: The system MUST forbid the use of the explicit `any` type in the application's TypeScript code.
- **FR-005**: The system MUST forbid the use of the non-null assertion operator `!` in TypeScript code.
- **FR-006**: The system MUST forbid calls to `console.log`, `console.warn`, and `console.error` in production code.
- **FR-007**: The system MUST report variables and parameters that are declared but never used.
- **FR-008**: The system MUST enforce the use of `ChangeDetectionStrategy.OnPush` for all Angular components.
- **FR-009**: The system MUST enforce the use of the `inject()` function for dependency injection, instead of constructor injection.
- **FR-010**: The system MUST detect imports declared in the `imports` array of a standalone component but never used in its template.
- **FR-011**: The system MUST report functions or methods whose cyclomatic complexity exceeds 10.
- **FR-012**: The lint command MUST be executable via `npm run lint` without additional parameters.
- **FR-013**: Generated directories (`dist/`, `node_modules/`, `.angular/`) MUST be automatically excluded from analysis.
- **FR-014**: The existing project code MUST be fixed to comply with all defined rules (zero violations at rollout).

### Assumptions

- The frontend is an Angular 21 standalone application with strict TypeScript already enabled.
- Developers use an ESLint-compatible editor (VS Code with the ESLint extension) to benefit from real-time feedback.
- Observable-related rules require a dedicated RxJS ESLint plugin.
- Angular-specific rules require a dedicated Angular ESLint plugin.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The lint command exits with 0 errors and 0 warnings on the existing code after configuration and fixes.
- **SC-002**: Any new violation introduced in the code is detected by the lint command with indication of the file, the line, and the rule.
- **SC-003**: The lint command runs in under 30 seconds across the entire frontend project.
- **SC-004**: A developer can identify and fix a violation by following only the reported error message, without external documentation.
- **SC-005**: Zero false positives on valid, idiomatic Angular 21 code (signals, inject(), OnPush, @if/@for).
