# Tasks: CI/CD Pipelines — Lint & Tests

**Input**: `specs/006-cicd-lint-tests/`
**Prerequisites**: spec.md ✓ plan.md ✓

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Peut tourner en parallèle
- **[US1]**: Backend change → backend checks only
- **[US2]**: Frontend change → frontend checks only
- **[US3]**: Full-stack change → les deux pipelines en parallèle

---

## Phase 1: Setup

**Purpose**: Créer la structure GitHub Actions

- [x] T001 Créer le répertoire `.github/workflows/`

---

## Phase 2: User Story 1 — Backend change triggers only backend checks (P1) 🎯 MVP

**Goal**: Un commit sur `backend/` déclenche ruff + pytest via le job `changes`, et rien d'autre.

**Independent Test**: Ouvrir une PR avec un seul fichier `backend/` modifié — seuls `backend-lint` et `backend-test` s'exécutent dans l'onglet Actions.

- [x] T002 [US1] Créer `.github/workflows/ci.yml` avec le job `changes` (dorny/paths-filter@v3) qui expose les outputs `backend` et `frontend`
- [x] T003 [US1] Ajouter le job `backend-lint` dans `ci.yml` : `needs: changes`, `if: needs.changes.outputs.backend == 'true'`, `setup-python@v5` (Python 3.12, cache pip), `ruff check .`
- [x] T004 [US1] Ajouter le job `backend-test` dans `ci.yml` : `needs: changes`, `if: needs.changes.outputs.backend == 'true'`, service PostgreSQL 16, install deps, `pytest tests/ -v --tb=short`
- [x] T005 [US1] Ajouter `backend/ruff.toml` : `target-version = "py312"`, règles E/F/I, exclure `chroma_data` et `scripts`

**Checkpoint**: Pipeline backend déclenchée et réussie sur une PR ne touchant que `backend/`.

---

## Phase 3: User Story 2 — Frontend change triggers only frontend checks (P1)

**Goal**: Un commit sur `frontend/` déclenche ESLint + vitest, et rien d'autre.

**Independent Test**: Ouvrir une PR avec un seul fichier `frontend/` modifié — seuls `frontend-lint` et `frontend-test` s'exécutent dans l'onglet Actions.

- [x] T006 [US2] Ajouter le job `frontend-lint` dans `ci.yml` : `needs: changes`, `if: needs.changes.outputs.frontend == 'true'`, `setup-node@v4` (Node 22, cache npm), `npm run lint`
- [x] T007 [US2] Ajouter le job `frontend-test` dans `ci.yml` : `needs: changes`, `if: needs.changes.outputs.frontend == 'true'`, `setup-node@v4` (Node 22, cache npm), `npm test -- --watch=false`

**Checkpoint**: Pipeline frontend déclenchée et réussie sur une PR ne touchant que `frontend/`.

---

## Phase 4: User Story 3 — Full-stack change triggers both pipelines (P2)

**Goal**: Un commit touchant `backend/` et `frontend/` déclenche les quatre jobs en parallèle.

**Independent Test**: Ouvrir une PR modifiant les deux dossiers — quatre jobs apparaissent simultanément dans l'onglet Actions.

- [ ] T008 [US3] Valider empiriquement que les quatre jobs (`backend-lint`, `backend-test`, `frontend-lint`, `frontend-test`) s'exécutent en parallèle sur une PR full-stack (validation dans l'onglet Actions après ouverture de la PR T009)

**Checkpoint**: Les quatre jobs s'exécutent simultanément.

---

## Phase 5: Polish

- [ ] T009 [P] Ouvrir la PR `006-cicd-lint-tests` → `master` pour déclencher la validation CI
- [ ] T010 Valider SC-003 : durée pipeline < 5 min (vérifier dans l'historique Actions après cache chaud)

---

## Dependencies & Execution Order

- **T001** → T002 → T003, T004, T005 (parallélisable après T002)
- **T002** → T003 → T004 (séquentiel dans US1 pour le même fichier)
- **T006, T007** : parallélisables entre eux (jobs différents dans le même fichier)
- **T008** nécessite T004 + T007 (US1 + US2 complets)

### MVP

T001 → T002 → T003 → T004 → T005 : pipeline backend opérationnelle.

---

## Notes

- `dorny/paths-filter@v3` est l'approche standard pour le path filtering conditionnel dans un fichier unique.
- Les tests backend utilisent SQLite in-memory — le service PostgreSQL en CI est présent pour les futurs tests d'intégration mais pas utilisé par les tests actuels.
- Ollama n'est pas disponible en CI — tous les appels Ollama sont mockés dans les tests (vérifié).
