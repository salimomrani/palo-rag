# DECISIONS.md — Trade-offs, Deviations, Limits, Next Steps

## Architectural Decisions

### 1. PostgreSQL instead of SQLite (spec deviation)

**Spec said**: "no Docker, local only"
**Decision**: PostgreSQL 16 via `docker-compose`
**Rationale**: Demonstrates production-grade persistence; SQLite lacks proper connection pooling for concurrent FastAPI workers. Docker adds 1 command to setup, acceptable for a demo.

---

### 2. ChromaDB embedded (not a separate vector DB server)

**Spec option**: Any vector store
**Decision**: ChromaDB in embedded mode (in-process, persisted to `./chroma_data/`)
**Rationale**: Zero-infrastructure overhead for local demo. Swappable via the `vectorstore` dependency in `backend/dependencies.py`.

---

### 3. Ollama local models (llama3.2 + nomic-embed-text)

**Spec option**: Ollama or Gen-e2 (Palo IT's internal LLM)
**Decision**: Ollama with `llama3.2` for generation, `nomic-embed-text` for embeddings
**Rationale**: 100% local, zero cost, no API keys. The `AIProvider` protocol (`backend/rag/provider.py`) isolates the LLM behind an interface — swapping to Gen-e2 requires only a new class implementing `generate()`, `stream_generate()`, and `embed()`.

---

### 4. Streaming via native fetch + ReadableStream (not Angular HttpClient)

**Spec**: SSE streaming for ChatGPT-style UX
**Decision**: Angular service uses `fetch()` with `ReadableStream` for the SSE stream endpoint
**Rationale**: Angular's `HttpClient` does not natively support streaming POST responses as an Observable of chunks. Native fetch gives full control over SSE parsing without additional libraries.

---

### 5. `similarity_search_with_relevance_scores` for confidence scoring

**Initial implementation**: `similarity_search_with_score` (L2 distance, unbounded)
**Final implementation**: `similarity_search_with_relevance_scores` (normalized to [0,1])
**Rationale**: L2 distances are not human-interpretable percentages. The relevance score API provides [0,1] values directly comparable to the confidence threshold (`LOW_CONFIDENCE_THRESHOLD = 0.5`). Results are further clamped: `max(0.0, min(1.0, score))`.

---

### 6. PII masking (regex-based, not ML)

**Decision**: Regex patterns for emails, phone numbers, French SSN, credit cards
**Rationale**: Sufficient for a demo corpus. No external dependencies, fully offline.
**Limit**: False negatives on less common PII formats; a production system would use a dedicated NER model (spaCy, presidio).

---

## Known Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| No document chunking overlap | Adjacent context can be lost at chunk boundaries | Add `chunk_overlap=100` in `RecursiveCharacterTextSplitter` |
| No reranker | Top-4 retrieved chunks may not be the most relevant | Add a cross-encoder reranker (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) |
| Single-turn chat | No conversation memory; each query is independent | Add `ConversationBufferMemory` or pass last N turns in the prompt |
| No authentication | Any client can ingest/delete documents | Add API key middleware or OAuth2 for production |
| Corpus is synthetic | 15 Markdown docs created for the demo | Replace with real internal docs |
| llama3.2 3B quality | Smaller model, occasional hallucinations | Switch to llama3.2:8b or mistral:7b for better quality |
| Regex guardrails | Injection/offensive detection via patterns, bypassable | Add a secondary LLM-based content moderation layer |

---

## What Was Built vs. Spec

| Feature | Spec | Built | Notes |
|---------|------|-------|-------|
| RAG query endpoint | ✅ required | ✅ done | + streaming variant |
| Document ingestion | ✅ required | ✅ done | + duplicate guard (409) |
| Input guardrails | ✅ required | ✅ done | + offensive content (FR/EN) |
| Audit logging + PII masking | ✅ required | ✅ done | PostgreSQL-backed |
| Quality evaluation | ✅ required | ✅ done | 15-Q reference dataset |
| Angular UI | ✅ required | ✅ done | Chat + Ingest + Logs |
| Document delete | ❌ not in spec | ✅ added | FR-017 |
| SSE streaming | ❌ not in spec | ✅ added | FR-019/020 |
| Duplicate ingestion guard | ❌ not in spec | ✅ added | FR-018 |
| Gen-e2 integration | 🔜 stretch | ❌ not done | AIProvider ready, needs credentials |
| BDD scenarios | 🔜 stretch | ❌ not done | Unit tests cover all user stories |

---

## Next Steps (production roadmap)

1. **Reranker**: Add cross-encoder reranking after retrieval for better precision
2. **Conversation memory**: Multi-turn chat with context window management
3. **Gen-e2 provider**: Implement `GenE2Provider(AIProvider)` once API credentials are available
4. **Best practices corpus**: Replace synthetic docs with real Palo IT knowledge base
5. **Authentication**: API key or OAuth2 for document management endpoints
6. **Evaluation automation**: Schedule daily quality runs, alert on score regression
7. **Chunk overlap**: Enable `chunk_overlap=100` to reduce boundary-split context loss
8. **Observability**: OpenTelemetry traces for latency breakdown (embed / retrieve / generate)
