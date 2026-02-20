# Implementation Plan: Angular ESLint — Best Practices Rules

**Branch**: `002-angular-eslint-rules` | **Date**: 2026-02-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/002-angular-eslint-rules/spec.md`

---

## Summary

Configurer ESLint v9 (flat config) sur le frontend Angular 21 avec un ensemble de règles couvrant : qualité TypeScript (`no-explicit-any`, `no-non-null-assertion`), bonnes pratiques Angular (`OnPush`, `inject()`), conventions RxJS (subscribe imbriqué interdit, suffixe `$` pour les Observables), et qualité générale (`no-console`, complexité). Le code existant sera corrigé pour atteindre 0 erreur. La commande `npm run lint` sera ajoutée et passera à 0 erreur/0 warning.

---

## Technical Context

**Language/Version**: TypeScript 5.9.2 / Angular 21.1.0 / Node.js 22 LTS
**Primary Dependencies**:
- `eslint ^9.0.0` — core linter (flat config)
- `@angular-eslint/eslint-plugin ^21.0.0` — règles Angular
- `@angular-eslint/eslint-plugin-template ^21.0.0` — règles templates HTML
- `@angular-eslint/builder ^21.0.0` — ng lint builder
- `angular-eslint ^21.0.0` — meta-package configs
- `typescript-eslint ^8.0.0` — règles TypeScript
- `@eslint/js ^9.0.0` — règles JS base
- `eslint-plugin-rxjs-x ^0.5.0` — règles RxJS (ESLint v9 compatible)

**Storage**: N/A — feature purement tooling, aucune persistance
**Testing**: Vérification via `npm run lint` (exit code 0)
**Target Platform**: macOS / Linux (local dev), Angular CLI 21
**Performance Goals**: Lint complet < 30 secondes
**Constraints**: Zéro erreur, zéro warning sur `npm run lint` après correction du code existant

---

## Constitution Check

| Principe | Impact | Statut |
|----------|--------|--------|
| I. Local-First | Aucun — tooling pur, aucune donnée traitée | ✅ N/A |
| II. Traceability | Aucun | ✅ N/A |
| III. Fail transparently | Aucun | ✅ N/A |
| IV. Separation of Concerns | Le linter est un outil de dev, pas un module applicatif | ✅ Conforme |
| V. Demo-Ready Reproducibility | `npm run lint` doit être reproductible depuis un clean checkout | ✅ Conforme — les deps seront en `devDependencies` |

**Gate**: ✅ PASS — aucune violation constitutionnelle.

---

## Project Structure

### Documentation (this feature)

```text
specs/002-angular-eslint-rules/
├── plan.md         ✅ (ce fichier)
├── research.md     ✅ (Phase 0)
└── tasks.md        (Phase 2 — /speckit.tasks)
```

### Source Code (fichiers modifiés/créés)

```text
frontend/
├── eslint.config.mjs          # NOUVEAU — configuration ESLint flat config
├── package.json               # Ajout deps + script "lint"
├── angular.json               # Ajout cible "lint" avec @angular-eslint/builder
└── src/app/
    ├── services/
    │   └── rag-api.service.ts # Fix: renommer méthodes Observable$ si nécessaire
    └── components/
        └── chat/
            └── chat.ts        # Fix: ViewChild ! → assertion typée si possible
```

**Structure Decision**: Frontend uniquement — aucun changement backend.

---

## Phase 0: Research ✅

Voir [research.md](./research.md).

**Décisions clés** :
- ESLint v9 flat config (`eslint.config.mjs`)
- `eslint-plugin-rxjs-x` pour les règles RxJS (compatible ESLint v9)
- `@angular-eslint/builder` pour `ng lint`
- `no-non-null-assertion` → `warn` (ViewChild pattern courant en Angular)
- `no-console` → `warn`

---

## Phase 1: Design

### Configuration ESLint (`frontend/eslint.config.mjs`)

Structure en 3 blocs :

```
Block 1 — Ignores globaux
  dist/, node_modules/, .angular/, coverage/

Block 2 — Fichiers TypeScript (*.ts)
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
      rxjs-x/finnish: error ($ suffix sur propriétés/variables Observable)
    Général:
      no-console: warn
      complexity: warn (max: 10)

Block 3 — Templates HTML (*.html)
  extends: angular.templateRecommended + angular.templateAccessibility
```

### Corrections du code existant anticipées

| Fichier | Violation | Correction |
|---------|-----------|------------|
| `chat.ts:34` | `messagesEl!` → `no-non-null-assertion` (warn) | Accepté en warn — pattern ViewChild valide |
| `rag-api.service.ts` | `streamQuery()` retourne `Observable<StreamEvent>` sans `$` | Renommer `streamQuery$()` **ou** exclure la règle sur les méthodes de service |

> **Note**: La règle `rxjs-x/finnish` s'applique aux variables/propriétés de classe. Les méthodes retournant un Observable dans un service Angular sont un cas-limite — à configurer en `warn` pour les méthodes de service Angular (`@Injectable`).

### `package.json` — script lint

```json
"scripts": {
  "lint": "ng lint"
}
```

### `angular.json` — cible lint

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

## Trade-offs documentés

| Décision | Avantage | Inconvénient |
|----------|----------|--------------|
| `no-non-null-assertion: warn` au lieu de `error` | Évite de casser `@ViewChild('el') el!` pattern | Moins strict |
| `no-console: warn` | Préserve la productivité dev local | Visible en CI seulement avec `--max-warnings 0` |
| `eslint-plugin-rxjs-x` au lieu de `eslint-plugin-rxjs` | Compatible ESLint v9 | Fork moins connu, dépend de la maintenance communautaire |
| Convention `$` sur variables seulement (pas méthodes de service) | Évite de casser les APIs publiques du service | Couverture partielle de la convention |

---

## Complexity Tracking

Aucune violation constitutionnelle. Section non applicable.
