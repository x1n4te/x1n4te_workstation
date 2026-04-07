---
id: hermes-agent-source-001
type: source
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
  - agentic-workflows
  - nous-research
  - deep-research
  - procedural-memory
related:
  - concepts/procedural-memory
  - concepts/delegate-task-architecture
  - concepts/model-routing
  - concepts/context-caching
  - concepts/closed-learning-loop
  - concepts/hermes-production-stack
---

# Hermes-Agent: Deep Research Agentic Workflows (Source Summary)

**Source:** `raw/ai-research/HERMES-AGENT.md`  
**Type:** Architectural analysis / framework documentation  
**Date:** 2026-04-07  
**Confidence:** High  

---

## Core Thesis

Hermes-Agent (Nous Research) is an open-source, self-improving AI agent framework that abandons the static control-plane model in favor of a **closed learning loop** — converting every successful task resolution into reusable procedural memory (SKILL.md), bypassing redundant LLM planning phases on future similar tasks.

Key differentiator vs. traditional agents: persistent procedural memory vs. stateless interpretation.

---

## Key Findings

### Architecture Layers
1. **Session History** — SQLite/PostgreSQL FTS5; turn-by-turn recall
2. **Prompt Memory** — MEMORY.md / USER.md; persistent user preferences
3. **Procedural Memory** — SKILL.md; self-authored task methodologies
4. **External Pluggable** — Honcho/vector stores; long-term semantic retrieval

### Delegation Topology
- `delegate_task`: ThreadPoolExecutor, max 3 parallel children, MAX_DEPTH=2
- Background subprocess mode: bypasses 3-child limit via `terminal(background=true)`
- Parent blocks until all children complete or timeout

### Model Routing
- OpenRouter deterministic routing: `latency` | `throughput` | `price`
- Asymmetric delegation: heavy frontier model for orchestrator, fast/cheap for child agents
- MiniMax-M2.7 highlighted as agent-native model (56.2% SWE-Pro, 1495 ELO on GDPval-AA)

### Context Caching
- **50% threshold**: agent/context_compressor.py — proactive LLM summarization
- **85% threshold**: gateway/run.py — edge failsafe truncation
- Stable-prefix caching (Anthropic): TTFT 28s → 0.3s on cache hit (~75% token cost reduction)

### Production Stack
- FastAPI (async) + PostgreSQL + PgBouncer + Alembic + Docker Compose
- 14-platform gateway (Discord, Telegram, Slack, etc.)
- 6 terminal backends: local, Docker, SSH, Daytona, Singularity, Modal

---

## Relevance to WIMS-BFP

- **Multi-agent Discord setup**: Gateway supports Discord natively; aligns with 4-agent architecture proposal
- **Procedural memory**: SKILL.md pattern directly applicable to WIMS-BFP audit/remediation workflows
- **delegate_task**: Modeled on same hierarchy as FRS role escalation (ENCODER → VALIDATOR → ANALYST)
- **Production stack**: FastAPI + PostgreSQL matches existing WIMS-BFP backend stack

---

## Concepts Derived From This Source

- [[concepts/closed-learning-loop]]
- [[concepts/procedural-memory]]
- [[concepts/delegate-task-architecture]]
- [[concepts/model-routing]]
- [[concepts/context-caching]]
- [[concepts/hermes-production-stack]]
