# Research: Frontend Unit Testing — Angular 21 + Vitest

## Decision 1: Test runner — @angular/build:unit-test natif

**Decision**: Utiliser le builder `@angular/build:unit-test` avec `runner: "vitest"` (natif Angular 21)
**Rationale**: Angular 21 supporte Vitest nativement via `@angular/build`. Pas besoin d'`@analogjs/vitest-angular` ni de `vitest.config.ts` séparé. Le `tsconfig.spec.json` avec `vitest/globals` est déjà en place. Seul ajout dans `angular.json` : `"runner": "vitest"` sous la cible `test`.
**Alternatives écartées**: `@analogjs/vitest-angular` (overhead inutile), Karma (obsolète depuis Angular 16), Jest (non aligné avec le tooling Angular CLI)

## Decision 2: Mocking HTTP — provideHttpClientTesting

**Decision**: `provideHttpClientTesting()` + `HttpTestingController` depuis `@angular/common/http/testing`
**Rationale**: Solution officielle Angular, compatible avec `inject()`, intercepte tous les appels HTTP sans configuration supplémentaire.
**Alternatives écartées**: `vi.fn()` sur HttpClient (fragile, couple les tests à l'implémentation)

## Decision 3: Mocking services — vi.fn() + useValue

**Decision**: `{ provide: RagApiService, useValue: mockService }` avec `vi.fn()` pour les méthodes
**Rationale**: Les composants utilisent `inject(RagApiService)` — le provider override via `TestBed.configureTestingModule` est le seul moyen propre de substituer le service.

## Decision 4: Signaux et détection de changements

**Decision**: `fixture.detectChanges()` après chaque mutation, `TestBed.flushEffects()` pour les effets de signaux
**Rationale**: Angular 21 en mode OnPush ne déclenche pas automatiquement la détection. `flushEffects()` est requis pour propager les effets de signaux dans les tests.

## Decision 5: Aucun nouveau package npm requis

**Decision**: 0 nouvelle dépendance — `vitest@4.0.8` et `jsdom@27` déjà installés, `@angular/build` inclut le support Vitest.
**Rationale**: Le projet est déjà correctement équipé. Seuls ajouts : config `angular.json` + fichiers `*.spec.ts`.

## Compatibilité confirmée

- Angular 21 + `@angular/build:unit-test` + Vitest ✓
- `tsconfig.spec.json` avec `"types": ["vitest/globals"]` déjà présent ✓
- `jsdom@27` déjà installé ✓
- `ng test` lancera Vitest une fois `runner: "vitest"` ajouté ✓
