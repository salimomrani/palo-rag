# Research: Angular ESLint — Best Practices Rules

**Date**: 2026-02-19
**Branch**: `002-angular-eslint-rules`

---

## Observed Context

- Angular 21.1.0 / TypeScript 5.9.2 / RxJS 7.8.0
- No existing ESLint configuration (neither `eslint.config.*` nor a `lint` target in `angular.json`)
- ESLint v9 = flat config mandatory (`eslint.config.mjs`)

---

## Decision 1 — ESLint Packages

**Decision**: ESLint v9 flat config with the following packages:

| Package | Version | Role |
|---------|---------|------|
| `eslint` | `^9.0.0` | Core linter |
| `@angular-eslint/eslint-plugin` | `^21.0.0` | Angular rules |
| `@angular-eslint/eslint-plugin-template` | `^21.0.0` | HTML template rules |
| `@angular-eslint/builder` | `^21.0.0` | `ng lint` integration |
| `angular-eslint` | `^21.0.0` | Meta-package flat config |
| `typescript-eslint` | `^8.0.0` | TypeScript rules |
| `@eslint/js` | `^9.0.0` | Base JS rules |
| `eslint-plugin-rxjs-x` | `^0.5.0` | RxJS rules compatible with ESLint v9 |

**Rationale**: `@angular-eslint` v21 is aligned with Angular 21 and supports flat config. `typescript-eslint` v8 is required by `@angular-eslint` v18+. `eslint-plugin-rxjs-x` is the maintained fork compatible with ESLint v9 (the original `eslint-plugin-rxjs` depends on ESLint ^8).

**Rejected alternatives**:
- `eslint-plugin-rxjs`: incompatible with ESLint v9 (peer dep `eslint ^8.0.0`)
- `eslint-plugin-rxjs-angular-x`: Angular-only focus, less complete for base RxJS rules

---

## Decision 2 — `$` Convention for Observables

**Decision**: `@typescript-eslint/naming-convention` with selector `variable` + type `observable`

```js
{
  selector: 'variable',
  types: ['observable'],
  format: null,
  custom: { regex: '\\$$', match: true }
}
```

**Rationale**: `typescript-eslint` allows targeting Observable types via the `types: ['observable']` selector. The `rxjs-x/finnish` rule also covers this convention and is complementary.

**Rejected alternatives**: Custom ESLint rule = too much maintenance overhead for a demo.

---

## Decision 3 — `no-nested-subscribe` Rule

**Decision**: `rxjs-x/no-nested-subscribe` at `error` level

**Rationale**: The rule detects `subscribe(() => { ..subscribe() })` patterns in TypeScript code and reports an error with the file and line number.

---

## Decision 4 — Angular-Specific Rules

**Decision**: Enable via `@angular-eslint`:

| Rule | Level | Objective |
|------|-------|-----------|
| `@angular-eslint/prefer-on-push-component-change-detection` | `error` | OnPush mandatory |
| `@angular-eslint/prefer-inject` | `error` | inject() vs constructor |
| `@angular-eslint/no-empty-lifecycle-hook` | `error` | Empty lifecycle hooks |

**Note**: There is no official ESLint rule for unused standalone imports — Angular 19+ detects this at build time. We will combine `@typescript-eslint/no-unused-vars` + manual verification.

---

## Decision 5 — `npm run lint` Integration

**Decision**: Use `@angular-eslint/builder:lint` in `angular.json` and expose via `npm run lint` in `package.json`.

```json
"scripts": {
  "lint": "ng lint"
}
```

**Rationale**: `ng lint` uses the Angular builder which lints `.ts` and `.html` in a single command with a formatted report.

---

## Rules Excluded / Configured as Warn

| Rule | Decision | Reason |
|------|----------|--------|
| `@typescript-eslint/no-non-null-assertion` | `warn` | `@ViewChild` with `!` is sometimes necessary in Angular — set to warn to avoid too much noise on existing code |
| `no-console` | `warn` | Avoids blocking local dev, only blocks CI via `--max-warnings 0` |
| `complexity` | `warn` (max: 10) | Informational rather than blocking |

---

## Anticipated Violations in Existing Code

Quick analysis of current code:
- `chat.ts`: `@ViewChild('messagesEl') private messagesEl!` → `no-non-null-assertion` (warn)
- No nested subscribes identified (streaming via native Observable)
- No explicit `any` identified
- All components: OnPush ✅, `inject()` ✅
- Observable naming: `streamQuery()` returns `Observable<StreamEvent>` → must be `streamQuery$()` or renamed — to be fixed
