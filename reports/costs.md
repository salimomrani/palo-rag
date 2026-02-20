# Rapport de coûts — PALO RAG Knowledge Assistant

> **À mettre à jour à la fin de chaque session de travail.**
> Utiliser `/cost` dans Claude Code pour obtenir le coût de la session courante.

---

## Coûts d'inférence AI (runtime du produit)

| Composant | Coût unitaire | Volume estimé (demo) | Total |
|-----------|--------------|----------------------|-------|
| Ollama — LLM (`llama3.2`) | 0€ (local) | ~30 requêtes demo | **0€** |
| Ollama — Embeddings (`nomic-embed-text`) | 0€ (local) | ~200 embeddings (ingestion + requêtes) | **0€** |
| Gen-e2 (si activé en prod) | À définir | — | — |

**Total inférence AI : 0€** (stack 100% local)

---

## Coûts de développement (Claude Code)

| Session | Date | Tokens input | Tokens output | Coût estimé |
|---------|------|-------------|--------------|-------------|
| Session 1 — Design, spec-kit, planning | 2026-02-19 | _(à remplir)_ | _(à remplir)_ | _(à remplir)_ |
| Session 2 — Implementation Phase 1-2 | — | — | — | — |
| Session 3 — Implementation Phase 3-6 | — | — | — | — |
| Session 4 — Implementation Phase 7-9 | — | — | — | — |
| **TOTAL** | | | | **_(à calculer)_** |

> 💡 Pour récupérer le coût d'une session Claude Code : `/cost` dans le terminal Claude Code.

---

## Coûts infrastructure (demo locale)

| Composant | Coût |
|-----------|------|
| Serveur | 0€ (MacBook local) |
| PostgreSQL / ChromaDB | 0€ (embedded, local) |
| Ollama | 0€ (open source) |
| Angular CLI | 0€ (open source) |
| **Total infrastructure** | **0€** |

---

## Coût total du projet (MVP demo)

| Catégorie | Coût |
|-----------|------|
| AI runtime (Ollama, local) | 0€ |
| AI development (Claude Code) | _(à compléter)_ |
| Infrastructure | 0€ |
| **TOTAL** | **_(à compléter)_** |

---

## Projection : coût en production (Gen-e2 / cloud)

> Estimations pour 100 utilisateurs, 500 requêtes/jour

| Composant | Prix indicatif | Volume/mois | Coût/mois estimé |
|-----------|---------------|-------------|-----------------|
| Embeddings (Gen-e2 / OpenAI) | ~0.02€ / 1M tokens | ~5M tokens | ~0.10€ |
| LLM génération (Gen-e2 / GPT-4o-mini) | ~0.15€ / 1M tokens | ~50M tokens | ~7.50€ |
| Vector DB (Weaviate Cloud / Pinecone) | ~25€/mois (Starter) | — | ~25€ |
| Hébergement API (Cloud Run / Fly.io) | ~15€/mois | — | ~15€ |
| **Total production (100 users)** | | | **~48€/mois** |

---

## Analyse coût/valeur

**Pour la demo (poc local) :**
- Coût runtime : **0€** — tout tourne en local avec Ollama
- Coût dev : quelques euros de Claude Code — à remplir après chaque session

**Pour la production :**
- < 50€/mois pour 100 utilisateurs = ROI quasi immédiat vs recherche manuelle dans des docs
- Gen-e2 interne pourrait réduire les coûts LLM à 0€ si infrastructure partagée

---

## Instructions pour mettre à jour ce fichier

1. À la fin de chaque session Claude Code, lancer `/cost` dans le terminal
2. Copier les valeurs tokens/coût dans le tableau "Coûts de développement"
3. Mettre à jour le total
4. Committer : `git add reports/costs.md && git commit -m "chore: update costs report — session N"`
