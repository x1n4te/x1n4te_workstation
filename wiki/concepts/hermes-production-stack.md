---
id: hermes-production-stack-001
type: concept
created: 2026-04-07
updated: 2026-04-07
last_verified: 2026-04-07
review_after: 2026-05-07
stale_after: 2026-07-06
confidence: high
source_refs:
  - raw/ai-research/HERMES-AGENT.md
status: active
tags:
  - hermes-agent
  - production
  - fastapi
  - postgresql
  - docker
  - infrastructure
  - pgbouncer
  - alembic
related:
  - entities/hermes-agent
  - concepts/context-caching
---

# Hermes-Agent Production Stack

**Framework:** Hermes-Agent (Nous Research)  
**Section:** 7 of architectural analysis  

---

## Definition

The production deployment stack for Hermes-Agent in high-availability, long-running research environments. Replaces default SQLite (local CLI) with enterprise-grade infrastructure: **Python + FastAPI + PostgreSQL + PgBouncer + Alembic + Docker Compose**.

---

## Component Stack

| Component | Technology | Purpose |
|---|---|---|
| API Layer | FastAPI (Python 3.11+, async) | OpenAI-compatible interface; non-blocking I/O for agentic workloads |
| Validation | Pydantic | Strict schema enforcement on data flowing from web/external sources |
| Database | PostgreSQL 14.5 or 16 | Centralized memory layer; multi-turn chat logs, structured data, JSON payloads |
| Connection Pooling | PgBouncer | Prevents connection bottleneck under high-concurrency multi-agent workloads |
| ORM | SQLAlchemy | Python object to relational table mapping |
| Migrations | Alembic | Version-controlled, deterministic schema evolution |
| Containerization | Docker Compose | Environment portability; defines `chat-network` bridge isolating DB from app |
| Vector Search | pgvector (PostgreSQL extension) | Semantic search within PostgreSQL layer (no third-party vector DB needed) |
| Volume Mounts | PostgreSQL `/var/lib/postgresql/data` | Persistent memory across container restarts/server reboots |

---

## Why FastAPI for Agentic Workloads

Agent steps involve inherent waiting:
- LLM API calls (network I/O, seconds of latency)
- Web scraping spiders returning large payloads
- File system operations on remote machines

FastAPI's native `asyncio` model ensures these waits **do not block the main event loop**. The server can handle dozens of concurrent incoming subagent webhook notifications without stalling.

Pydantic validates all incoming data against schemas before injection — prevents hallucination cascades from unvalidated external data.

---

## PgBouncer: Connection Pooling for Multi-Agent Scale

In massive parallel workflows, dozens of subagents may write simultaneously. Without pooling:

```
subagent_1 → PostgreSQL connection 1 ✓
subagent_2 → PostgreSQL connection 2 ✓
...
subagent_50 → PostgreSQL connection → CONNECTION EXHAUSTED → bottleneck/failure
```

PgBouncer manages a pool of N connections shared across all agents. Agents borrow connections as needed, return them when done. PostgreSQL never sees more than pool_size connections.

---

## Alembic: Deterministic Schema Migrations

As Hermes-Agent capabilities evolve, database schemas must change:
- New memory layers
- Honcho integration user-modeling schemas
- New agent state tables

Manual table modifications are prohibited. Alembic provides:
- Version-controlled migrations
- `upgrade()` / `downgrade()` reversible changes
- Migration history in version control

---

## Docker Compose: Environment Portability

```yaml
services:
  app:
    build: .
    networks: [chat-network]
  postgres:
    image: postgres:16
    volumes: [postgres_data:/var/lib/postgresql/data]
    networks: [chat-network]
networks:
  chat-network:
    internal: true  # Isolates DB from external exposure
```

Key properties:
- **Network isolation:** PostgreSQL not directly exposed to internet
- **Volume persistence:** Memory survives container restarts
- **Snapshot portability:** Entire DB + config can be bundled as a single snapshot

If an agent completes intensive research on an expensive GPU cluster, the entire state can be spun up on a cheap headless server for passive monitoring.

---

## pgvector: Semantic Search Without a Separate Database

Adding `pgvector` extension to PostgreSQL enables:
```sql
CREATE EXTENSION vector;
-- Store embeddings in regular tables
-- Query with semantic similarity directly in SQL
```

Eliminates need for separate Chroma/FAISS/Pinecone deployment. All agent memory (chat logs, structured data, embeddings) in one PostgreSQL instance.

---

## Relevance to WIMS-BFP

The WIMS-BFP backend already uses:
- **FastAPI** — aligns perfectly
- **PostgreSQL + RLS** — aligns, WIMS-BFP uses pgcrypto + PostGIS
- **Redis + Celery** — complementary (queue/async), not replacement

The production stack described is a superset of WIMS-BFP's current architecture — validates the existing choices and provides a migration path for scaling beyond single-server deployment.

---

## Related

- [[entities/hermes-agent]] — Parent entity
- [[concepts/context-caching]] — Complementary token optimization layer
