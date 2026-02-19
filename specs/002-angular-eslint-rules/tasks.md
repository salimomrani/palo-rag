# Tasks: Angular ESLint — Best Practices Rules

**Input**: Design documents from `specs/002-angular-eslint-rules/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅

---

## Phase 1: Setup (Installation des dépendances)

**Purpose**: Installer les packages ESLint et configurer la structure

- [ ] T001 Installer les devDependencies ESLint dans `frontend/package.json` : `eslint ^9`, `@angular-eslint/eslint-plugin ^21`, `@angular-eslint/eslint-plugin-template ^21`, `@angular-eslint/builder ^21`, `angular-eslint ^21`, `typescript-eslint ^8`, `@eslint/js ^9`, `eslint-plugin-rxjs-x ^0.5`
- [ ] T002 Ajouter le script `"lint": "ng lint"` dans `frontend/package.json`
- [ ] T003 Ajouter la cible `lint` avec `@angular-eslint/builder:lint` dans `frontend/angular.json` (lintFilePatterns: `src/**/*.ts`, `src/**/*.html`)

---

## Phase 2: Fondation (Configuration ESLint)

**Purpose**: Créer la configuration ESLint flat config — BLOQUE les phases suivantes

**⚠️ CRITIQUE**: La configuration doit exister avant toute correction du code

- [ ] T004 Créer `frontend/eslint.config.mjs` avec le bloc 1 (ignores globaux : `dist/`, `node_modules/`, `.angular/`, `coverage/`)
- [ ] T005 Ajouter le bloc TypeScript (`**/*.ts`) dans `frontend/eslint.config.mjs` avec : `js.recommended`, `tseslint.recommended`, `angular.configs.tsRecommended`, `processor: angular.processInlineTemplates`
- [ ] T006 Ajouter les règles TypeScript dans le bloc TS de `frontend/eslint.config.mjs` : `@typescript-eslint/no-explicit-any: error`, `@typescript-eslint/no-non-null-assertion: warn`, `@typescript-eslint/no-unused-vars: error`
- [ ] T007 Ajouter les règles Angular dans le bloc TS de `frontend/eslint.config.mjs` : `@angular-eslint/prefer-on-push-component-change-detection: error`, `@angular-eslint/prefer-inject: error`, `@angular-eslint/no-empty-lifecycle-hook: error`
- [ ] T008 Ajouter les règles RxJS dans le bloc TS de `frontend/eslint.config.mjs` : `rxjs-x/no-nested-subscribe: error`, `rxjs-x/finnish: error` ($ suffix sur propriétés/variables Observable)
- [ ] T009 Ajouter les règles générales dans le bloc TS de `frontend/eslint.config.mjs` : `no-console: warn`, `complexity: ["warn", 10]`
- [ ] T010 Ajouter le bloc HTML (`**/*.html`) dans `frontend/eslint.config.mjs` avec : `angular.configs.templateRecommended`, `angular.configs.templateAccessibility`

**Checkpoint**: `npm run lint` depuis `frontend/` doit s'exécuter (peut afficher des erreurs sur le code existant) ✅

---

## Phase 3: US1 — Détection des violations + zéro erreur sur le code existant (Priority: P1) 🎯 MVP

**Goal**: La commande lint s'exécute et le code existant est conforme (0 erreur, 0 warning)

**Independent Test**: `cd frontend && npm run lint` → exit code 0, "0 errors, 0 warnings"

- [ ] T011 [US1] Exécuter `npm run lint` depuis `frontend/` et capturer toutes les violations rapportées
- [ ] T012 [P] [US1] Corriger les violations `@typescript-eslint/no-explicit-any` dans `frontend/src/app/services/rag-api.service.ts` (remplacer `unknown` par le type précis si possible)
- [ ] T013 [P] [US1] Corriger les violations `rxjs-x/finnish` dans `frontend/src/app/services/rag-api.service.ts` : vérifier que les propriétés/variables de type Observable portent le suffixe `$`
- [ ] T014 [P] [US1] Corriger les violations `rxjs-x/finnish` dans `frontend/src/app/components/chat/chat.ts` : vérifier nommage Observable$
- [ ] T015 [P] [US1] Corriger les violations éventuelles dans `frontend/src/app/components/ingest/ingest.ts`
- [ ] T016 [P] [US1] Corriger les violations éventuelles dans `frontend/src/app/components/logs/logs.ts`
- [ ] T017 [P] [US1] Corriger les violations éventuelles dans `frontend/src/app/components/eval/eval.ts`
- [ ] T018 [US1] Relancer `npm run lint` et vérifier 0 erreur — si violations restantes, les corriger itérativement jusqu'à exit code 0
- [ ] T019 [US1] **Commit**: `feat: eslint config + zero violations (US1 complete)`

**Checkpoint**: `npm run lint` → exit code 0, 0 errors, 0 warnings ✅

---

## Phase 4: US2 — Intégration CI (Priority: P2)

**Goal**: `npm run lint` bloque le CI en cas de violation (exit code non-nul)

**Independent Test**: Introduire une violation délibérée → `npm run lint` → exit code 1 → corriger → exit code 0

- [ ] T020 [US2] Vérifier que `npm run lint` retourne exit code 1 en présence d'une violation artificielle (ajouter temporairement `const x: any = 1` dans un fichier, linter, vérifier l'échec, puis retirer)
- [ ] T021 [US2] Documenter la commande CI dans `README.md` (section Tests) : `cd frontend && npm run lint`
- [ ] T022 [US2] **Commit**: `docs: add lint step to README CI section`

**Checkpoint**: Pipeline CI simulé via `npm run lint` — bloque en cas de violation ✅

---

## Phase 5: Polish & validation finale

- [ ] T023 Vérifier que le lint s'exécute en moins de 30 secondes (mesurer avec `time npm run lint`)
- [ ] T024 [P] Vérifier qu'aucun fichier dans `dist/`, `node_modules/`, `.angular/` n'est analysé (examiner la sortie du lint)
- [ ] T025 Mettre à jour `specs/002-angular-eslint-rules/tasks.md` (ce fichier) avec les statuts finaux
- [ ] T026 **Commit**: `chore: eslint final validation — lint < 30s, exclusions verified`

---

## Dependencies & Execution Order

- **Phase 1** (Setup) : Aucune dépendance — démarrer immédiatement
- **Phase 2** (Config) : Dépend de Phase 1 — BLOQUE les phases suivantes
- **Phase 3** (US1 — zéro erreur) : Dépend de Phase 2 — peut commencer dès T010 validé
- **Phase 4** (US2 — CI) : Dépend de Phase 3 — `npm run lint` doit passer à 0 erreur
- **Phase 5** (Polish) : Dépend de Phase 4

### Opportunités de parallélisation

- T012–T017 : corrections de fichiers différents → peuvent s'exécuter en parallèle
- T023–T024 : vérifications indépendantes → parallélisables

---

## Notes

- [P] = fichiers différents, aucune dépendance entre tâches
- La résolution des violations (T012–T017) dépend des erreurs réelles rapportées en T011 — ajuster si d'autres fichiers sont concernés
- `no-non-null-assertion` est configuré en `warn` (pas `error`) pour préserver les patterns `@ViewChild` valides en Angular
- Si `eslint-plugin-rxjs-x` n'est pas disponible à la version souhaitée, utiliser `eslint-plugin-rxjs-angular-x` comme alternative
