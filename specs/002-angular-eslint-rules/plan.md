# Implementation Plan: Angular ESLint — Best Practices Rules

**Branch**: `002-angular-eslint-rules` | **Date**: 2026-02-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/002-angular-eslint-rules/spec.md`

---

## Summary

Configure ESLint v9 (flat config) on the Angular 21 frontend with a set of rules covering: TypeScript quality (`no-explicit-any`, `no-non-null-assertion`), Angular best practices (`OnPush`, `inject()`), RxJS conventions (nested subscribe banned, `$` suffix for Observables), and general quality (`no-console`, complexity). Existing code will be fixed to reach 0 errors. The `npm run lint` command will be added and will pass with 0 errors / 0 warnings.

---

## Technical Context

**Language/Version**: TypeScript 5.9.2 / Angular 21.1.0 / Node.js 22 LTS
**Primary Dependencies**:
- `eslint ^9.0.0` — core linter (flat config)
- `@angular-eslint/eslint-plugin ^21.0.0` — Angular rules
- `@angular-eslint/eslint-plugin-template ^21.0.0` — HTML template rules
- `@angular-eslint/builder ^21.0.0` — ng lint builder
- `angular-eslint ^21.0.0` — meta-package configs
- `typescript-eslint ^8.0.0` — TypeScript rules
- `@eslint/js ^9.0.0` — base JS rules
- `eslint-plugin-rxjs-x ^0.5.0` — RxJS rules (ESLint v9 compatible)

**Storage**: N/A — purely a tooling feature, no persistence
**Testing**: Verified via `npm run lint` (exit code 0)
**Target Platform**: macOS / Linux (local dev), Angular CLI 21
**Performance Goals**: Full lint < 30 seconds
**Constraints**: Zero errors, zero warnings on `npm run lint` after fixing existing code

---

## Constitution Check

| Principle | Impact | Status |
|-----------|--------|--------|
| I. Local-First | None — pure tooling, no data processed | ✅ N/A |
| II. Traceability | None | ✅ N/A |
| III. Fail transparently | None | ✅ N/A |
| IV. Separation of Concerns | The linter is a dev tool, not an application module | ✅ Compliant |
| V. Demo-Ready Reproducibility | `npm run lint` must be reproducible from a clean checkout | ✅ Compliant — deps will be in `devDependencies` |

**Gate**: ✅ PASS — no constitutional violation.

---

## Project Structure

### Documentation (this feature)

```text
specs/002-angular-eslint-rules/
├── plan.md         ✅ (this file)
├── research.md     ✅ (Phase 0)
└── tasks.md        (Phase 2 — /speckit.tasks)
```

### Source Code (files modified/created)

```text
frontend/
├── eslint.config.mjs          # NEW — ESLint flat config
├── package.json               # Add deps + "lint" script
├── angular.json               # Add "lint" target with @angular-eslint/builder
└── src/app/
    ├── services/
    │   └── rag-api.service.ts # Fix: rename Observable$ methods if needed
    └── components/
        └── chat/
            └── chat.ts        # Fix: ViewChild ! → typed assertion if possible
```

**Structure Decision**: Frontend only — no backend changes.

---

## Phase 0: Research ✅

See [research.md](./research.md).

**Key decisions**:
- ESLint v9 flat config (`eslint.config.mjs`)
- `eslint-plugin-rxjs-x` for RxJS rules (ESLint v9 compatible)
- `@angular-eslint/builder` for `ng lint`
- `no-non-null-assertion` → `warn` (ViewChild pattern common in Angular)
- `no-console` → `warn`

---

## Phase 1: Design

### ESLint Configuration (`frontend/eslint.config.mjs`)

Structure in 3 blocks:

```
Block 1 — Global ignores
  dist/, node_modules/, .angular/, coverage/

Block 2 — TypeScript files (*.ts)
  extends: js.recommended + tseslint.recommended + angular.tsRecommended
  processor: angular.processInlineTemplates
  rules:
    TypeScript:
      @typescript-eslint/no-explicit-any: error
      @typescript-eslint/no-non-null-assertion: warn
      @typescript-eslint/no-unused-vars: error
      @typescript-eslint/naming-convention: error (Observable $ suffix)
    Angular:
      @angular-eslint/prefer-on-push-component-change-detection: error
      @angular-eslint/prefer-inject: error
      @angular-eslint/no-empty-lifecycle-hook: error
    RxJS:
      rxjs-x/no-nested-subscribe: error
      rxjs-x/finnish: error ($ suffix on Observable properties/variables)
    General:
      no-console: warn
      complexity: warn (max: 10)

Block 3 — HTML templates (*.html)
  extends: angular.templateRecommended + angular.templateAccessibility
```

### Anticipated fixes on existing code

| File | Violation | Fix |
|------|-----------|-----|
| `chat.ts:34` | `messagesEl!` → `no-non-null-assertion` (warn) | Accepted as warn — valid ViewChild pattern |
| `rag-api.service.ts` | `streamQuery()` returns `Observable<StreamEvent>` without `$` | Rename to `streamQuery$()` **or** exclude rule for Angular service methods |

> **Note**: The `rxjs-x/finnish` rule applies to class variables/properties. Methods returning an Observable in an Angular service are an edge case — configure as `warn` for Angular service methods (`@Injectable`).

### `package.json` — lint script

```json
"scripts": {
  "lint": "ng lint"
}
```

### `angular.json` — lint target

```json
"lint": {
  "builder": "@angular-eslint/builder:lint",
  "options": {
    "lintFilePatterns": [
      "src/**/*.ts",
      "src/**/*.html"
    ]
  }
}
```

---

## Trade-offs documented

| Decision | Advantage | Disadvantage |
|----------|-----------|--------------|
| `no-non-null-assertion: warn` instead of `error` | Avoids breaking `@ViewChild('el') el!` pattern | Less strict |
| `no-console: warn` | Preserves local dev productivity | Only visible in CI with `--max-warnings 0` |
| `eslint-plugin-rxjs-x` instead of `eslint-plugin-rxjs` | Compatible with ESLint v9 | Less well-known fork, depends on community maintenance |
| `$` convention on variables only (not service methods) | Avoids breaking public service APIs | Partial coverage of the convention |

---

## Complexity Tracking

No constitutional violations. Section not applicable.
