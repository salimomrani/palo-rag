# Feature Specification: CI/CD Pipelines — Lint & Tests

**Feature Branch**: `006-cicd-lint-tests`
**Created**: 2026-02-22
**Status**: Draft
**Input**: CI/CD pipelines minimaux pour tests et lint — GitHub Actions avec path filtering : si seul le frontend change, seuls les jobs frontend (ESLint + vitest) tournent ; si seul le backend change, seuls les jobs backend (ruff + pytest) tournent. Pas de déploiement.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Backend change triggers only backend checks (Priority: P1)

Un développeur modifie un fichier Python dans `backend/`. La pipeline détecte le changement, exécute uniquement le lint et les tests backend, et bloque la PR si l'un d'eux échoue.

**Why this priority**: Cas le plus fréquent en développement backend ; bloquer les commits cassés est la valeur principale du CI.

**Independent Test**: Ouvrir une PR avec un seul fichier `backend/` modifié — seuls les jobs backend apparaissent dans l'onglet Actions.

**Acceptance Scenarios**:

1. **Given** une PR avec des modifications uniquement dans `backend/`, **When** la PR est ouverte ou mise à jour, **Then** seuls les jobs `lint` et `test` du backend s'exécutent.
2. **Given** un fichier Python contenant une erreur de style, **When** le job lint s'exécute, **Then** la pipeline échoue et bloque le merge.
3. **Given** un test backend en échec, **When** le job test s'exécute, **Then** la pipeline échoue et bloque le merge.

---

### User Story 2 - Frontend change triggers only frontend checks (Priority: P1)

Un développeur modifie un composant Angular dans `frontend/`. Seuls le lint et les tests frontend tournent ; les jobs backend ne sont pas déclenchés.

**Why this priority**: Même priorité que P1 backend — le path filtering est le coeur de la feature.

**Independent Test**: Ouvrir une PR avec un seul fichier `frontend/` modifié — seuls les jobs frontend apparaissent dans l'onglet Actions.

**Acceptance Scenarios**:

1. **Given** une PR avec des modifications uniquement dans `frontend/`, **When** la PR est ouverte ou mise à jour, **Then** seuls les jobs `lint` et `test` du frontend s'exécutent.
2. **Given** une violation de règle ESLint dans le code frontend, **When** le job lint s'exécute, **Then** la pipeline échoue et bloque le merge.
3. **Given** un test vitest en échec, **When** le job test s'exécute, **Then** la pipeline échoue et bloque le merge.

---

### User Story 3 - Full-stack change triggers both pipelines (Priority: P2)

Un développeur modifie à la fois `backend/` et `frontend/` dans une même PR. Les deux pipelines s'exécutent en parallèle.

**Why this priority**: Cas moins fréquent mais nécessaire pour garantir la cohérence complète du projet.

**Independent Test**: Ouvrir une PR touchant les deux dossiers — quatre jobs (backend lint, backend test, frontend lint, frontend test) apparaissent simultanément.

**Acceptance Scenarios**:

1. **Given** une PR modifiant `backend/` et `frontend/`, **When** la PR est ouverte, **Then** les quatre jobs s'exécutent en parallèle.

---

### Edge Cases

- Que se passe-t-il si seuls les fichiers de configuration CI (`.github/workflows/`) sont modifiés ? → Les deux workflows sont déclenchés (les fichiers workflow eux-mêmes font partie des paths surveillés).
- Que se passe-t-il si la base de données de test est indisponible ? → Le job test backend échoue explicitement avec un message d'erreur lisible.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT déclencher uniquement les jobs backend lorsque des fichiers sous `backend/` sont modifiés.
- **FR-002**: Le système DOIT déclencher uniquement les jobs frontend lorsque des fichiers sous `frontend/` sont modifiés.
- **FR-003**: Le système DOIT exécuter le lint et les tests comme deux jobs séparés pour chaque périmètre (backend et frontend).
- **FR-004**: Le système DOIT bloquer le merge d'une PR si au moins un job échoue.
- **FR-005**: Le système DOIT mettre en cache les dépendances pour réduire la durée d'exécution des pipelines.
- **FR-006**: Le système NE DOIT PAS inclure d'étape de déploiement.
- **FR-007**: Le système DOIT fournir des messages d'erreur lisibles en cas d'échec (lint ou test).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Une PR ne touchant que le frontend ne déclenche aucun job backend (et vice-versa) — vérifiable dans l'historique Actions.
- **SC-002**: Un commit cassant un test ou une règle de style est bloqué avant merge dans 100% des cas.
- **SC-003**: La durée totale d'une pipeline complète (lint + tests) ne dépasse pas 5 minutes grâce au cache des dépendances.
- **SC-004**: Les quatre jobs (backend lint, backend test, frontend lint, frontend test) s'exécutent en parallèle lorsque les deux périmètres sont touchés.
