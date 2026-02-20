# PALO RAG — Project Instructions

## Stack

- **Backend**: Python 3.12, FastAPI, LangChain 0.3, ChromaDB (embedded), SQLAlchemy 2, PostgreSQL 16
- **AI**: Ollama local (`qwen2.5:7b` + `mxbai-embed-large`) — `AIProvider` interface swappable
- **Frontend**: Angular 21, standalone components, signals, OnPush, 2-space indent

## Workflow Skills (mandatory)

### Spécification & planification

- **Feature ou gros changement** → toujours passer par speckit : `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`
- **Petit fix** (typo, label, 1-2 lignes) → modif directe sans spec
- Ne jamais coder une feature sans spec et plan validés
- **Interdiction** d'utiliser `superpowers:writing-plans` ou `superpowers:executing-plans` — speckit remplace ces skills sur ce projet

### Frontend

- Utiliser le skill **`frontend-design`** pour TOUT travail UI (composants, pages, layouts)
- Angular 21 strict : `input()`/`output()`, `inject()`, `@if`/`@for`, OnPush obligatoire
  composants standalone par défaut, signals pour la réactivité
- Vérifier les APIs Angular/PrimeNG avec **Context7** avant d'implémenter

### Documentation

- Vérifier les docs avec **Context7** (`mcp__context7__resolve-library-id` + `mcp__context7__query-docs`) pour : FastAPI, LangChain, ChromaDB, Angular, SQLAlchemy

## Architecture Constraints (constitution.md)

1. **Local-first** : aucune donnée ne quitte la machine, Ollama uniquement
2. **Tracabilité** : chaque query → log entry (question PII-masquée, context IDs, score, latence)
3. **Fail transparent** : jamais de réponse hallucinée, guardrail refusal = succès
4. **Séparation des concerns** : RAG / guardrails / eval = modules indépendants
5. **Reproductible** : 3 commandes depuis checkout propre
6. **DB** : PostgreSQL 16 via `docker-compose up -d` (dévier de la spec "no Docker" — décision volontaire)

## Python Conventions

- Type hints partout, Pydantic v2 pour les schémas
- `pytest` + `pytest-asyncio` pour les tests, TDD obligatoire
- `ruff` pour le linting
- Variables d'env via `.env` (jamais de secrets commitées)

## Task Tracking (obligatoire)

- Après chaque tâche complétée : mettre à jour `specs/001-rag-assistant/tasks.md` (status `[x]`)
- Marquer `in_progress` avant de commencer, `done` dès que terminé et testé

## Git

- Branches : `feature/`, `fix/`, `chore/`
- Conventional commits obligatoires
- Tests verts avant tout commit

## Source de vérité

- **Code > plan.md > tasks.md** : en cas de divergence, le code fait foi
- Avant tout fix de "mismatch" : lire le fichier réel, pas le plan
- Paths et prefixes : vérifier avec `find`/`grep` sur le repo avant d'écrire

## Key Files

- `specs/001-rag-assistant/spec.md` — source de vérité fonctionnelle
- `specs/001-rag-assistant/plan.md` — plan d'implémentation
- `specs/001-rag-assistant/tasks.md` — 61 tâches T001–T061
- `.specify/memory/constitution.md` — 5 principes architecturaux
- `DECISIONS.md` — tout écart à la spec documenté ici
- `reports/costs.md` — `/cost` en fin de session
