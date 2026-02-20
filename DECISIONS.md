# DECISIONS.md — Trade-offs, Deviations, Limits, Next Steps

## Architectural Decisions

### 1. PostgreSQL 16 via Docker

**Decision**: PostgreSQL 16 via `docker-compose`
**Rationale**: Production-grade persistence with proper connection pooling for concurrent FastAPI workers.

---

### 2. ChromaDB embedded (not a separate vector DB server)

**Spec option**: Any vector store
**Decision**: ChromaDB in embedded mode (in-process, persisted to `./chroma_data/`)
**Rationale**: Zero-infrastructure overhead for local demo. Swappable via the `vectorstore` dependency in `backend/dependencies.py`.

---

### 3. Ollama local models (qwen2.5:7b + mxbai-embed-large)

**Spec option**: Ollama or Gen-e2 (Palo IT's internal LLM)
**Decision**: Ollama with `qwen2.5:7b` for generation, `mxbai-embed-large` for embeddings
**Rationale**: 100% local, zero cost, no API keys. `qwen2.5:7b` offers strong multilingual support (29 languages including French) and 128K context window vs `llama3.2` 3B. `mxbai-embed-large` scores +5pts retrieval on MTEB (54.39 vs 49.01) vs `nomic-embed-text`. The `AIProvider` protocol (`backend/rag/provider.py`) isolates the LLM behind an interface — swapping to Gen-e2 requires only a new class implementing `generate()`, `stream_generate()`, and `embed()`.

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

### 7. LLM temperature = 0.1

**Default**: Ollama default ~0.8 (creative)
**Decision**: `llm_temperature=0.1` (configurable via `LLM_TEMPERATURE` env var)
**Rationale**: RAG requires deterministic, factual answers. High temperature increases hallucination risk. 0.1 gives quasi-deterministic output while preserving minimal paraphrasing variety. Configurable to allow A/B testing without code changes.

---

### 8. `keep_alive=-1` on ChatOllama (LLM stays in GPU)

**Default**: Ollama evicts models after ~5 min of inactivity
**Decision**: `keep_alive=-1` on `ChatOllama` only (model stays loaded indefinitely while the backend runs)
**Rationale**: Without this, the LLM is unloaded from GPU between requests → 20–45s cold-start latency per query, unacceptable for a demo. `OllamaEmbeddings` does not support `keep_alive` in the installed LangChain version; the embed model (762 MB) reloads quickly enough to be acceptable.

---

## Known Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| No document chunking overlap | Adjacent context can be lost at chunk boundaries | Add `chunk_overlap=100` in `RecursiveCharacterTextSplitter` |
| No reranker | Top-4 retrieved chunks may not be the most relevant | Add a cross-encoder reranker (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) |
| Single-turn chat | No conversation memory; each query is independent | Add `ConversationBufferMemory` or pass last N turns in the prompt |
| No authentication | Any client can ingest/delete documents | Add API key middleware or OAuth2 for production |
| Corpus is synthetic | 15 Markdown docs created for the demo | Replace with real internal docs |
| mxbai-embed-large context limit | 512-token context window (vs 8192 nomic) | Ensure chunk_size ≤ 400 tokens in ingestion |
| Regex guardrails | Injection/offensive detection via patterns, bypassable | Add a secondary LLM-based content moderation layer |

---

## What Was Built vs. Spec

| Feature | Status | Notes |
|---------|--------|-------|
| RAG query endpoint | ✅ done | + streaming variant |
| Document ingestion | ✅ done | + duplicate guard (409) |
| Input guardrails | ✅ done | + offensive content (FR/EN) |
| Audit logging + PII masking | ✅ done | PostgreSQL-backed |
| Quality evaluation | ✅ done | 15-Q reference dataset |
| Angular UI | ✅ done | Chat + Ingest + Logs |
| Document delete | ✅ added | FR-017 |
| SSE streaming | ✅ added | FR-019/020 |
| Duplicate ingestion guard | ✅ added | FR-018 |
| Gen-e2 integration | 🔜 stretch | AIProvider ready, needs credentials |
| BDD scenarios | ✅ done | pytest unit tests cover all user stories (no Gherkin format) |

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
