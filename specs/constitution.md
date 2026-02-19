# PALO-RAG Constitution

## Core Principles

### Local-First & Privacy by Design
All AI inference runs locally via Ollama. No user data, queries, or documents leave the machine. PII is masked before logging. This is a hard constraint, not a preference.

### Traceability Over Opacity
Every query must produce a traceable log entry: input, retrieved context, output, quality score, latency. The system must be auditable end-to-end with zero hidden state.

### Fail Transparently, Never Silently
When the system cannot answer confidently (low similarity score, guardrail triggered, LLM uncertainty), it says so explicitly rather than hallucinating a response. A guardrail refusal is a success, not a failure.

### Separation of Concerns
Backend (RAG pipeline, guardrails, eval) is decoupled from frontend (Angular). The API contract is the only shared interface. Changes to the AI stack do not require frontend changes.

### Demo-Ready Reproducibility
Any reviewer must be able to run the full stack in under 5 minutes using only `ollama serve`, `uvicorn`, and `ng serve`. No cloud dependencies, no API keys, no external services required.

## Scope

This project demonstrates production-grade RAG architecture patterns for an internal knowledge assistant. It is a proof-of-concept designed for a 45-minute technical debrief, not a production deployment.

### In Scope
- Document ingestion (Markdown/TXT/plain text)
- Semantic search and RAG-based Q&A
- Input/output guardrails
- Query traceability and structured logging
- Automated evaluation with RAGAS metrics
- Angular UI (chat, ingest, logs views)

### Out of Scope
- Authentication / user management
- Multi-tenancy
- Cloud deployment
- Streaming responses (v1)
- Reranking (noted as next-step)

## Governance

The spec (spec.md) is the source of truth for WHAT to build. The plan (plan.md) defines HOW. Any deviation from spec.md must be documented in DECISIONS.md with rationale.

**Version**: 1.0 | **Ratified**: 2026-02-19
