---
id: hindsight-entity-001
type: entity
title: "Hindsight — Self-Hosted Memory Provider"
created: 2026-04-18
updated: 2026-04-18
last_verified: 2026-04-18
review_after: 2026-07-18
stale_after: 2026-10-18
confidence: high
source_refs:
  - log-archives/log-2026-04-18-hindsight-migration.md
  - entities/honcho.md
status: active
tags:
  - memory-systems
  - llm-agents
  - self-hosted
  - devops
  - docker
related:
  - entities/honcho
  - concepts/agent-memory-taxonomy
  - analyses/memory-systems-comparison
  - entities/hermes-agent
---

## Overview

**Hindsight** is a self-hosted semantic memory system for AI agents, built by Vectorize.io. It provides persistent, compounding memory with multi-strategy retrieval — designed as a local alternative to cloud memory providers like Honcho.

**Status for x1n4te:** Evaluation completed 2026-04-18. Migration attempted and deferred. Currently staying on [[entities/honcho]] ($40 credits remaining). Hindsight migration queued for when Honcho credits exhaust.

---

## Benchmark Performance

Hindsight leads on LongMemEval benchmark ( episodic memory + retrieval ):

| System | LongMemEval Score | Type |
|---|---|---|
| **Hindsight** | **91.4–94.6%** | Self-hosted |
| Mastra | 94.87% (特定 model) | Cloud |
| MemMachine | 93.0% | Self-hosted |
| Mem0 | ~85% (estimated) | Cloud |
| Honcho | Not published | Cloud |

**Note:** Hindsight's benchmark numbers are the highest among self-hosted systems. Honcho does not publish benchmark scores.

---

## Architecture

```
hindsight CLI  →  http://localhost:8888  →  Hindsight Server (Docker)
                                            ├── pg0 (embedded PostgreSQL)
                                            ├── pgvector (vector search)
                                            ├── Local embeddings (BAAI/bge-base-en-v1.5)
                                            ├── Local reranker (cross-encoder/ms-marco-MiniLM-L-6-v2)
                                            └── LLM (Groq/Llama 3.3 70B for extraction)
```

**Deployment:** Single Docker container (`ghcr.io/vectorize-io/hindsight:latest`), ~9GB image.

**Image variants:**
- `latest` — Full image (~9GB). Embeddings + reranker built-in. Only LLM key needed. **Recommended.**
- `latest-slim` — Slim (~500MB). Requires external embedding provider.

---

## Retrieval Strategy

Four parallel retrieval strategies merged by cross-encoder reranker:

1. **Semantic** — Dense vector embeddings
2. **BM25** — Keyword/bm25 retrieval
3. **Graph traversal** — Entity-relationship traversal
4. **Temporal reasoning** — Time-aware retrieval

Result: RRF (Reciprocal Rank Fusion) merged and reranked before returning.

---

## Key Features

- **Self-hosted** — Zero cloud cost, full data control
- **Observation consolidation** — Auto-deduplicates related facts into durable observations with evidence chains
- **Mission/directives/disposition** — Configurable bank personality (skepticism, literalism, empathy)
- **Mental models** — Curated summaries for repeated high-traffic queries
- **REST API + CLI** — Both interfaces available
- **No embedding costs** — Local embeddings included in full image

---

## Critical Issue: Groq TPM Limit

**Problem discovered during evaluation:**

Hindsight's fact extraction (retain) sends: system prompt + bank mission + extraction schema + user content. The overhead alone is **~8,000 tokens before user content**.

- **Groq `gpt-oss-20b`**: 8,000 TPM limit → HTTP 413 on every retain → 0 facts extracted
- **Groq `llama-3.3-70b-versatile`**: 32,000 TPM limit → works correctly

**Fix:** Use `llama-3.3-70b-versatile` (or any model with >10k TPM) + `HINDSIGHT_API_RETAIN_MAX_COMPLETION_TOKENS=32000`.

Also requires: `HINDSIGHT_API_VECTOR_EXTENSION=pgvector` (not `pg0`).

---

## Migration Status

| Date | Event |
|---|---|
| 2026-04-18 AM | Honcho credits ~$40 remaining; migration evaluation started |
| 2026-04-18 AM | Hindsight deployed (full Docker image, Groq gpt-oss-20b) |
| 2026-04-18 AM | Docker volume permissions fixed (chmod 777 ~/.hindsight-data) |
| 2026-04-18 AM | Embedding env vars removed (full image has local embeddings) |
| 2026-04-18 AM | HTTP 413 on every retain — root cause: 8k TPM limit |
| 2026-04-18 AM | Switched to llama-3.3-70b-versatile (32k TPM) |
| 2026-04-18 AM | $GROQ_API_KEY not in shell env → container failed to start |
| 2026-04-18 PM | User elected to stay on Honcho; Hindsight container removed |

**Skill updated:** `hindsight-memory-setup` has correct docker run template with `llama-3.3-70b-versatile`.

---

## When to Resume

When Honcho credits approach $0:

1. Export Groq key: `export GROQ_API_KEY=gsk_...`
2. Run with `llama-3.3-70b-versatile` + `HINDSIGHT_API_RETAIN_MAX_COMPLETION_TOKENS=32000`
3. Test single fact retain before batch import
4. Use REST API with unique `document_id` per fact (CLI batch is synchronous and times out)
5. Migrate Honcho peer cards + observations via Honcho export tools

---

## See Also

- [[entities/honcho]] — Current memory provider ($40 credits)
- [[analyses/memory-systems-comparison]] — Full benchmark comparison
- [[concepts/agent-memory-taxonomy]] — Memory type taxonomy
- [[entities/hermes-agent]] — Hermes agent integration
- [[entities/memmachine]] — Best self-hosted competitor
