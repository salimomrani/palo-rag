# Research: Frontend Unit Testing — Angular 21 + Vitest

## Decision 1: Test runner — native @angular/build:unit-test

**Decision**: Use the `@angular/build:unit-test` builder with `runner: "vitest"` (native Angular 21)
**Rationale**: Angular 21 supports Vitest natively via `@angular/build`. No need for `@analogjs/vitest-angular` or a separate `vitest.config.ts`. The `tsconfig.spec.json` with `vitest/globals` is already in place. The only addition in `angular.json` is `"runner": "vitest"` under the `test` target.
**Rejected alternatives**: `@analogjs/vitest-angular` (unnecessary overhead), Karma (deprecated since Angular 16), Jest (not aligned with Angular CLI tooling)

## Decision 2: HTTP mocking — provideHttpClientTesting

**Decision**: `provideHttpClientTesting()` + `HttpTestingController` from `@angular/common/http/testing`
**Rationale**: Official Angular solution, compatible with `inject()`, intercepts all HTTP calls without additional configuration.
**Rejected alternatives**: `vi.fn()` on HttpClient (fragile, couples tests to implementation)

## Decision 3: Service mocking — vi.fn() + useValue

**Decision**: `{ provide: RagApiService, useValue: mockService }` with `vi.fn()` for methods
**Rationale**: Components use `inject(RagApiService)` — provider override via `TestBed.configureTestingModule` is the only clean way to substitute the service.

## Decision 4: Signals and change detection

**Decision**: `fixture.detectChanges()` after each mutation, `TestBed.flushEffects()` for signal effects
**Rationale**: Angular 21 in OnPush mode does not automatically trigger detection. `flushEffects()` is required to propagate signal effects in tests.

## Decision 5: No new npm packages required

**Decision**: 0 new dependencies — `vitest@4.0.8` and `jsdom@27` already installed, `@angular/build` includes Vitest support.
**Rationale**: The project is already correctly equipped. Only additions: `angular.json` config + `*.spec.ts` files.

## Confirmed compatibility

- Angular 21 + `@angular/build:unit-test` + Vitest ✓
- `tsconfig.spec.json` with `"types": ["vitest/globals"]` already present ✓
- `jsdom@27` already installed ✓
- `ng test` will launch Vitest once `runner: "vitest"` is added ✓
