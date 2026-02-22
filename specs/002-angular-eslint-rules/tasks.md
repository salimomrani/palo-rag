# Tasks: Angular ESLint — Best Practices Rules

**Input**: Design documents from `specs/002-angular-eslint-rules/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅

---

## Phase 1: Setup (Dependency Installation)

**Purpose**: Install ESLint packages and configure the structure

- [x] T001 Install ESLint devDependencies in `frontend/package.json`: `eslint ^9`, `@angular-eslint/eslint-plugin ^21`, `@angular-eslint/eslint-plugin-template ^21`, `@angular-eslint/builder ^21`, `angular-eslint ^21`, `typescript-eslint ^8`, `@eslint/js ^9`, `eslint-plugin-rxjs-x ^0.5`
- [x] T002 Add the `"lint": "ng lint"` script to `frontend/package.json`
- [x] T003 Add the `lint` target with `@angular-eslint/builder:lint` to `frontend/angular.json` (lintFilePatterns: `src/**/*.ts`, `src/**/*.html`)

---

## Phase 2: Foundation (ESLint Configuration)

**Purpose**: Create the ESLint flat config — BLOCKS subsequent phases

**⚠️ CRITICAL**: Configuration must exist before any code fixes

- [x] T004 Create `frontend/eslint.config.mjs` with block 1 (global ignores: `dist/`, `node_modules/`, `.angular/`, `coverage/`)
- [x] T005 Add the TypeScript block (`**/*.ts`) to `frontend/eslint.config.mjs` with: `js.recommended`, `tseslint.recommended`, `angular.configs.tsRecommended`, `processor: angular.processInlineTemplates`
- [x] T006 Add TypeScript rules to the TS block of `frontend/eslint.config.mjs`: `@typescript-eslint/no-explicit-any: error`, `@typescript-eslint/no-non-null-assertion: warn`, `@typescript-eslint/no-unused-vars: error`
- [x] T007 Add Angular rules to the TS block of `frontend/eslint.config.mjs`: `@angular-eslint/prefer-on-push-component-change-detection: error`, `@angular-eslint/prefer-inject: error`, `@angular-eslint/no-empty-lifecycle-hook: error`
- [x] T008 Add RxJS rules to the TS block of `frontend/eslint.config.mjs`: `rxjs-x/no-nested-subscribe: error`, `rxjs-x/finnish: error` ($ suffix on Observable properties/variables)
- [x] T009 Add general rules to the TS block of `frontend/eslint.config.mjs`: `no-console: warn`, `complexity: ["warn", 10]`
- [x] T010 Add the HTML block (`**/*.html`) to `frontend/eslint.config.mjs` with: `angular.configs.templateRecommended`, `angular.configs.templateAccessibility`

**Checkpoint**: `npm run lint` from `frontend/` must run (may show errors on existing code) ✅

---

## Phase 3: US1 — Violation Detection + Zero Errors on Existing Code (Priority: P1) 🎯 MVP

**Goal**: The lint command runs and existing code is compliant (0 errors, 0 warnings)

**Independent Test**: `cd frontend && npm run lint` → exit code 0, "0 errors, 0 warnings"

- [x] T011 [US1] Run `npm run lint` from `frontend/` and capture all reported violations
- [x] T012 [P] [US1] Fix `@typescript-eslint/no-explicit-any` violations in `frontend/src/app/services/rag-api.service.ts` (replace with precise type instead of `unknown` where possible)
- [x] T013 [P] [US1] Fix `rxjs-x/finnish` violations in `frontend/src/app/services/rag-api.service.ts`: verify that Observable-typed properties/variables carry the `$` suffix
- [x] T014 [P] [US1] Fix `rxjs-x/finnish` violations in `frontend/src/app/components/chat/chat.ts`: verify Observable$ naming
- [x] T015 [P] [US1] Fix any violations in `frontend/src/app/components/ingest/ingest.ts`
- [x] T016 [P] [US1] Fix any violations in `frontend/src/app/components/logs/logs.ts`
- [x] T017 [P] [US1] Fix any violations in `frontend/src/app/components/eval/eval.ts`
- [x] T018 [US1] Re-run `npm run lint` and verify 0 errors — if violations remain, fix them iteratively until exit code 0
- [x] T019 [US1] **Commit**: `feat: eslint config + zero violations (US1 complete)`

**Checkpoint**: `npm run lint` → exit code 0, 0 errors, 0 warnings ✅

---

## Phase 4: US2 — CI Integration (Priority: P2)

**Goal**: `npm run lint` blocks CI on violation (non-zero exit code)

**Independent Test**: Introduce a deliberate violation → `npm run lint` → exit code 1 → fix → exit code 0

- [x] T020 [US2] Verify that `npm run lint` returns exit code 1 in the presence of an artificial violation (temporarily add `const x: any = 1` to a file, lint, verify failure, then remove)
- [x] T021 [US2] Document the CI command in `README.md` (Tests section): `cd frontend && npm run lint`
- [x] T022 [US2] **Commit**: `docs: add lint step to README CI section`

**Checkpoint**: CI pipeline simulated via `npm run lint` — blocks on violation ✅

---

## Phase 5: Polish & Final Validation

- [x] T023 Verify lint runs in under 30 seconds (measure with `time npm run lint`) — 2.35s ✅
- [x] T024 [P] Verify that no files in `dist/`, `node_modules/`, `.angular/` are analyzed (inspect lint output) ✅
- [x] T025 Update `specs/002-angular-eslint-rules/tasks.md` (this file) with final statuses
- [x] T026 **Commit**: `chore: eslint final validation — lint < 30s, exclusions verified`

---

## Dependencies & Execution Order

- **Phase 1** (Setup): No dependencies — start immediately
- **Phase 2** (Config): Depends on Phase 1 — BLOCKS subsequent phases
- **Phase 3** (US1 — zero errors): Depends on Phase 2 — can start once T010 is validated
- **Phase 4** (US2 — CI): Depends on Phase 3 — `npm run lint` must pass with 0 errors
- **Phase 5** (Polish): Depends on Phase 4

### Parallelisation Opportunities

- T012–T017: fixes in different files → can run in parallel
- T023–T024: independent verifications → parallelisable

---

## Notes

- [P] = different files, no dependency between tasks
- Violation fixes (T012–T017) depend on actual errors reported in T011 — adjust if other files are affected
- `no-non-null-assertion` is configured as `warn` (not `error`) to preserve valid `@ViewChild` patterns in Angular
- If `eslint-plugin-rxjs-x` is not available at the desired version, use `eslint-plugin-rxjs-angular-x` as an alternative
