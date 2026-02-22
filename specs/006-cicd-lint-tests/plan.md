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
    ci.yml   # single file — changes job + 4 conditional jobs
```

## Decisions

- Single `ci.yml`: one CI entry point, readable at a glance
- `changes` job (dorny/paths-filter@v3): detects which scopes changed
- Backend jobs (`backend-lint`, `backend-test`): `if: needs.changes.outputs.backend == 'true'`
- Frontend jobs (`frontend-lint`, `frontend-test`): `if: needs.changes.outputs.frontend == 'true'`
- Lint and tests as separate jobs (fail fast, clear visibility)
- Dependency caching enabled (pip + npm)
- PostgreSQL 16 service container for backend tests
- No deployment
