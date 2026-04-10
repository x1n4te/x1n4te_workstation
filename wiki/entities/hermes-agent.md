---
id: hermes-agent-entity-001
type: entity
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
  - nous-research
  - agent-framework
  - open-source
related:
  - concepts/closed-learning-loop
  - concepts/procedural-memory
  - concepts/delegate-task-architecture
  - concepts/model-routing
  - concepts/context-caching
  - concepts/hermes-production-stack
  - entities/nous-research
---

# Hermes-Agent

**Type:** AI Agent Framework  
**Organization:** [Nous Research](entities/nous-research)  
**License:** MIT  
**Website:** https://github.com/NousResearch/hermes-agent  
**Documentation:** https://hermes-agent.nousresearch.com/docs/  

---

## Overview

Hermes-Agent is an open-source, self-improving AI agent framework engineered by [Nous Research](entities/nous-research). It operates across 14+ messaging platforms (CLI, Discord, Telegram, Slack, WhatsApp, etc.) from a single centralized gateway process.

Primary differentiator vs. competitors (Claude Code, Codex, OpenClaw): **persistent procedural memory via self-authored SKILL.md files** — the agent converts successful task resolutions into reusable procedural knowledge that compounds across sessions.

---

## Key Facts

| Property | Value |
|---|---|
| Author | Nous Research |
| License | MIT |
| Language | Python |
| Core Loop | AIAgent class (`run_agent.py`) |
| Session Store | SQLite (default) / PostgreSQL (production) |
| Gateway Platforms | 14+ (CLI, Discord, Telegram, Slack, WhatsApp, Signal, Matrix, etc.) |
| Terminal Backends | local, Docker, SSH, Daytona, Singularity, Modal |
| Memory Layers | 4 (Session, Prompt, Procedural, External/Honcho) |

---

## Memory Architecture (4-Layer Stack)

1. **Session History** — SQLite/PostgreSQL FTS5; automatic per-turn logging
2. **Prompt Memory** — `MEMORY.md` + `USER.md`; agent-curated user preferences and session state
3. **Procedural Memory** — `~/.hermes/skills/*.md` (SKILL.md); self-authored task methodologies
4. **External Pluggable** — Honcho (PostgreSQL-backed), vector stores; dialectic user modeling

Layer 3 (Procedural/SKILL.md) is the defining innovation. Triggered after tasks requiring >5 tool calls, or involving unexpected API errors or user corrections.

---

## Core Components

### AIAgent (`run_agent.py`)
- Synchronous orchestration engine managing the full conversation lifecycle
- Handles provider resolution, prompt assembly (`prompt_builder.py`), context compression, tool dispatch
- Design principle: tool execution must be **observable and interruptible** at any point

### delegate_task (`tools/delegate_tool.py`)
- Spawns isolated child agents via ThreadPoolExecutor
- Max 3 parallel children, MAX_DEPTH=2 hard cap (no grandchildren)
- Each child: own context, restricted toolsets, separate terminal session
- Child failure is final; parent handles retry/health monitoring

### context_compressor (`agent/context_compressor.py`)
- Triggers at 50% context threshold; LLM-driven summarization preserving facts + system instructions
- Secondary 85% gateway failsafe in `gateway/run.py`

### prompt_caching (`agent/prompt_caching.py`)
- Activated automatically for Claude models
- Stable-prefix architecture: system instructions + history identical across tool-call turns
- Measured: 33K token context, TTFT 28s un-cached → 0.3s cached (~75% input token reduction)

---

## Multi-Agent Capabilities

### Standard Delegation (3-child max)
```
delegate_task(goal, context, toolsets=['terminal', 'file'])
```
- ThreadPoolExecutor-based
- Synchronous batch: up to 3 in parallel
- Parent blocks until all complete or timeout

### Mass Parallelism (background subprocesses)
```python
terminal(background=true)  # bypasses 3-child limit
# Spawns independent hermes-agent OS-level processes
# Parent supervises via process(poll)
```

---

## Model Routing

### OpenRouter Deterministic Routing

| Sort Parameter | Optimization | Use Case |
|---|---|---|
| `latency` | Lowest TTFT | Interactive CLI, fast approvals |
| `throughput` | Tokens/sec | Long-form synthesis, report generation |
| `price` | Cost-per-token | Mass scraping, categorization |

### Asymmetric Delegation
- Orchestrator parent: frontier model (Claude 3.5 Sonnet/Opus, GPT-4o)
- Child subagents: fast/cheap (Gemini Flash 2.0, Claude 3.5 Haiku, Qwen 3.5 MLX)
- Configured via `delegation.model` + `delegation.provider` in config.yaml

### MiniMax-M2.7
- Highlighted as agent-native model achieving 56.2% on SWE-Pro benchmark
- 1495 ELO on GDPval-AA
- Provider: `minimax` (direct) or OpenRouter

---

## Production Infrastructure

| Component | Technology | Purpose |
|---|---|---|
| API Layer | FastAPI (Python 3.11+, async) | OpenAI-compatible interface |
| Memory | PostgreSQL 14.5/16 + PgBouncer | Connection-pooled persistence |
| ORM | SQLAlchemy | Object-relational mapping |
| Migrations | Alembic | Version-controlled schema evolution |
| Container | Docker Compose | Environment portability |
| Vector Search | pgvector (extension) | Semantic search in PostgreSQL |

---

## Platform Support

**Gateway (14 platforms):**
CLI, Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Email, SMS, Home Assistant, DingTalk, Feishu, WeCom, API Server / Webhooks

**Terminal Backends (6):**
local, Docker, SSH, Daytona, Singularity, Modal

Modal/Daytona: serverless hibernation — zero compute cost when idle, instant wake with full filesystem/repo state preserved.

---

## Related Entities

- Nous Research — Author organization (see [[mocs/ai-research]])
- [[concepts/procedural-memory]] — Core SKILL.md mechanism
- [[concepts/delegate-task-architecture]] — Child agent spawning
- [[concepts/closed-learning-loop]] — Execute → Evaluate → Extract → Refine → Retrieve
- [[concepts/model-routing]] — OpenRouter + asymmetric delegation
- [[concepts/context-caching]] — Stable-prefix + dual compression
- [[concepts/hermes-production-stack]] — FastAPI + PostgreSQL + Docker

---

## WIMS-BFP Relevance

**4-agent Discord pipeline was attempted (2026-04-08) and FAILED.** See [[analyses/4-agent-pipeline-postmortem]] for full postmortem.

Architecture: 1 Discord bot (Orchestrator) + 3 delegate_task children (Builder/Tester/Critic). Configs created, Discord bot live, but RTX 3090 Ollama never served models and no integration test was executed. Pipeline never reached first live test run.

Key failure: Sushi-Coder (competitive programming training) mismatched with WIMS-BFP production patterns (RLS, Celery, Keycloak JWT). Model domain fit > parameter count.

The **delegate_task** hierarchy remains architecturally sound — the failure was execution/infra, not design.

The **SKILL.md procedural memory** pattern is directly applicable to WIMS-BFP audit/remediation workflows — the agent can self-author skill documents for RLS policy fixes, Celery task patterns, etc.
