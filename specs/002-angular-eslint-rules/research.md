# Research: Angular ESLint — Best Practices Rules

**Date**: 2026-02-19
**Branch**: `002-angular-eslint-rules`

---

## Context observé

- Angular 21.1.0 / TypeScript 5.9.2 / RxJS 7.8.0
- Pas de configuration ESLint existante (ni `eslint.config.*`, ni cible `lint` dans `angular.json`)
- ESLint v9 = flat config obligatoire (`eslint.config.mjs`)

---

## Decision 1 — Packages ESLint

**Decision**: ESLint v9 flat config avec les packages suivants :

| Package | Version | Rôle |
|---------|---------|------|
| `eslint` | `^9.0.0` | Core linter |
| `@angular-eslint/eslint-plugin` | `^21.0.0` | Règles Angular |
| `@angular-eslint/eslint-plugin-template` | `^21.0.0` | Règles templates HTML |
| `@angular-eslint/builder` | `^21.0.0` | Intégration `ng lint` |
| `angular-eslint` | `^21.0.0` | Meta-package flat config |
| `typescript-eslint` | `^8.0.0` | Règles TypeScript |
| `@eslint/js` | `^9.0.0` | Règles JS de base |
| `eslint-plugin-rxjs-x` | `^0.5.0` | Règles RxJS compatibles ESLint v9 |

**Rationale**: `@angular-eslint` v21 est aligné sur Angular 21 et supporte le flat config. `typescript-eslint` v8 est requis par `@angular-eslint` v18+. `eslint-plugin-rxjs-x` est le fork maintenu compatible ESLint v9 (le plugin original `eslint-plugin-rxjs` dépend de ESLint ^8).

**Alternatives rejetées**:
- `eslint-plugin-rxjs` : incompatible ESLint v9 (peer dep `eslint ^8.0.0`)
- `eslint-plugin-rxjs-angular-x` : focus Angular uniquement, moins complet pour les règles de base RxJS

---

## Decision 2 — Convention `$` pour les Observables

**Decision**: `@typescript-eslint/naming-convention` avec selector `variable` + type `observable`

```js
{
  selector: 'variable',
  types: ['observable'],
  format: null,
  custom: { regex: '\\$$', match: true }
}
```

**Rationale**: `typescript-eslint` permet de cibler les types Observable via le sélecteur `types: ['observable']`. La règle `rxjs-x/finnish` couvre également cette convention et est complémentaire.

**Alternatives rejetées**: Règle custom ESLint = maintenabilité trop lourde pour un demo.

---

## Decision 3 — Règle `no-nested-subscribe`

**Decision**: `rxjs-x/no-nested-subscribe` à niveau `error`

**Rationale**: La règle détecte les patterns `subscribe(() => { ..subscribe() })` dans le code TypeScript et signale une erreur avec le fichier et la ligne.

---

## Decision 4 — Règles Angular spécifiques

**Decision**: Activer via `@angular-eslint` :

| Règle | Niveau | Objectif |
|-------|--------|----------|
| `@angular-eslint/prefer-on-push-component-change-detection` | `error` | OnPush obligatoire |
| `@angular-eslint/prefer-inject` | `error` | inject() vs constructor |
| `@angular-eslint/no-empty-lifecycle-hook` | `error` | Lifecycle vides |

**Note**: Il n'existe pas de règle ESLint officielle pour les imports standalone inutilisés — Angular 19+ le détecte au build. On combinera `@typescript-eslint/no-unused-vars` + vérification manuelle.

---

## Decision 5 — Intégration `npm run lint`

**Decision**: Utiliser `@angular-eslint/builder:lint` dans `angular.json` et exposer via `npm run lint` dans `package.json`.

```json
"scripts": {
  "lint": "ng lint"
}
```

**Rationale**: `ng lint` utilise le builder Angular qui lint `.ts` et `.html` en une seule commande avec rapport formaté.

---

## Règles écartées / configurées en warn

| Règle | Décision | Raison |
|-------|----------|--------|
| `@typescript-eslint/no-non-null-assertion` | `warn` | ViewChild avec `!` est parfois nécessaire en Angular — passer en warn pour éviter trop de bruit sur le code existant |
| `no-console` | `warn` | Évite de bloquer le dev local, bloque seulement le CI via `--max-warnings 0` |
| `complexity` | `warn` (max: 10) | Informatif plutôt que bloquant |

---

## Violations anticipées dans le code existant

Analyse rapide du code actuel :
- `chat.ts` : `@ViewChild('messagesEl') private messagesEl!` → `no-non-null-assertion` (warn)
- Aucun subscribe imbriqué identifié (streaming via Observable natif)
- Aucun `any` explicite identifié
- Tous les composants : OnPush ✅, `inject()` ✅
- Nommage observables : `streamQuery()` retourne `Observable<StreamEvent>` → doit être `streamQuery$()` ou renommé — à corriger
