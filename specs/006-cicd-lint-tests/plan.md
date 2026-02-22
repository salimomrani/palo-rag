# Plan: CI/CD Pipelines — Lint & Tests

**Feature**: 006-cicd-lint-tests
**Created**: 2026-02-22

## Stack

- CI: GitHub Actions
- Backend checks: ruff (lint) + pytest (tests) + PostgreSQL 16 service
- Frontend checks: ESLint via ng lint + vitest via ng test
- Cache: pip (backend) + npm (frontend)

## Structure

```
.github/
  workflows/
    ci.yml   # fichier unique — changes job + 4 jobs conditionnels
```

## Decisions

- Fichier unique `ci.yml` : un seul point d'entrée CI, lisible en un coup d'œil
- Job `changes` (dorny/paths-filter@v3) : détecte quels périmètres ont changé
- Backend jobs (`backend-lint`, `backend-test`) : `if: needs.changes.outputs.backend == 'true'`
- Frontend jobs (`frontend-lint`, `frontend-test`) : `if: needs.changes.outputs.frontend == 'true'`
- Lint et tests = jobs séparés (fail fast, lisibilité)
- Cache dépendances activé (pip + npm)
- PostgreSQL 16 service container pour les tests backend
- Pas de déploiement
