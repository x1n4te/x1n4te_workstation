---
id: ai-research-moc-001
type: MOC
title: "AI Research — Map of Content"
created: 2026-04-07
updated: 2026-04-08
last_verified: 2026-04-07
review_after: 2026-05-07
stale_after: 2026-07-07
confidence: high
source_refs: []
status: active
tags:
  - moc
  - ai-research
related:
  - sources/ai-research/memmachine
  - sources/ai-research/dspy-declarative-prompt-optimization
  - sources/ai-research/hermes-agent
---

# AI Research — Map of Content

*Reading path and overview for AI research in the vault.*

---

## Overview

AI research in this vault covers four primary themes:

1. **AI Agent Memory Systems** — How AI agents maintain persistent memory across sessions (MemMachine, Mem0, Mastra, MemGPT)
2. **Prompt Optimization** — Declarative and learned approaches to LLM prompt engineering (DSPy)
3. **Agentic Architecture** — Autonomous agent frameworks, delegation, multi-agent orchestration (Hermes-Agent)
4. **Applied to WIMS-BFP** — How these concepts drive the 4-agent development pipeline

---

## Agent Memory Systems

*Start here if researching how AI agents remember.*

### Core Reading Path

1. [[concepts/agent-memory-taxonomy]] — Four memory types: STM, episodic, semantic, procedural
2. [[concepts/episodic-vs-semantic-memory]] — Deep dive: episodic (ground truth) vs. semantic (distilled)
3. [[entities/memmachine]] — Ground-truth-preserving memory system (best-in-class preservation)
4. [[analyses/memory-systems-comparison]] — Full architectural comparison table

### Quick Reference: Systems

| System                  | Ground Truth   | Benchmark | Token Cost         |                         |
| ----------------------- | -------------- | --------- | ------------------ | ----------------------- |
| [[entities/memmachine]] | [[MemMachine]] | ✓         | LoCoMo 0.9169      | Low (~80% less vs Mem0) |
| [[entities/mem0]]       | [[Mem0]]       | ✗         | —                  | High                    |
| [[entities/mastras]]    | [[Mastras]]    | ✗         | 94.87% LongMemEval | Very low                |
| [[entities/memgpt]]     | [[MemGPT]]     | Partial   | —                  | Variable                |

### Key Insight

> "Retrieval-stage optimizations dominate over ingestion-stage changes." — MemMachine ablation study

---

## Prompt Optimization

*Start here if researching DSPy or learned prompt engineering.*

### Core Reading Path

1. [[sources/ai-research/dspy-declarative-prompt-optimization]] — Full paper summary
2. [[entities/dspy]] — DSPy framework entity
3. [[concepts/declarative-prompt-optimization]] — Core concept

### Key Numbers

- **30-45%** factual accuracy improvement (DSPy vs. manual prompts)
- **~25%** hallucination reduction
- HotpotQA: +32%, GSM-8K: +45%, XSum: +38%

---

## Agentic Architecture

*Start here if researching autonomous agent frameworks, delegation, and multi-agent systems.*

### Core Reading Path

1. [[sources/ai-research/hermes-agent]] — Full architectural analysis of Hermes-Agent deep research workflows
2. [[entities/hermes-agent]] — Hermes-Agent entity (Nous Research)
3. [[concepts/closed-learning-loop]] — Execute → Evaluate → Extract → Refine → Retrieve
4. [[concepts/procedural-memory]] — SKILL.md: self-authored task methodologies
5. [[concepts/delegate-task-architecture]] — Child agent spawning, isolation, and supervision
6. [[concepts/model-routing]] — Asymmetric model assignment, OpenRouter routing
7. [[concepts/context-caching]] — Stable-prefix prompt caching, dual compression
8. [[concepts/hermes-production-stack]] — FastAPI + PostgreSQL + Docker production deployment

### Key Numbers

- **SKILL.md trigger:** Tasks requiring >5 tool calls, API errors, or user corrections
- **Context cache:** TTFT 28s → 0.3s on cache hit (~75% token cost reduction)
- **Delegation:** max 3 parallel children, MAX_DEPTH=2 hard cap

### Applied to WIMS-BFP

- [[entities/wims-bfp-agentic-workflow]] — 4-agent architecture: Orchestrator (MiMo-V2-Pro), Builder (Qwen3.5-27B-Sushi-Coder), Tester (DeepSeek V3.2), Critic (MiMo-V2-Pro)

---

## Open Questions / Research Gaps

- ~~Procedural memory not implemented in any current system~~ → **SOLVED:** Hermes-Agent implements procedural memory via SKILL.md (self-authored after >5 tool calls)
- Temporal reasoning remains limited across all systems
- LongMemEvalM evaluation pending (500 sessions, ~1.5M tokens/question)
- DSPy evaluated on reasoning/RAG/summarization — needs testing on classification tasks
- How do agent memory systems perform under adversarial conditions?
- Hermes-Agent delegation (3-child max, MAX_DEPTH=2) — how does it scale to 10+ subagents?
- Qwen3.5-27B-Sushi-Coder (trained on Codeforces) — how does it generalize to production code patterns?

---

## Thesis Relevance

**WIMS-BFP** uses AI-assisted threat detection on Suricata IDS logs for the Bureau of Fire Protection. Relevant connections:

- [[entities/memmachine|MemMachine]] episodic memory → incident audit trail design
- [[entities/dspy|DSPy]] declarative prompt optimization → automated threat classification prompt tuning
- [[entities/hermes-agent|Hermes-Agent]] procedural memory (SKILL.md) → WIMS-BFP audit/remediation skill automation
- [[concepts/delegate-task-architecture|delegate_task]] → 4-agent architecture for WIMS-BFP development pipeline
- [[concepts/hermes-production-stack|Production Stack]] → validates WIMS-BFP's FastAPI + PostgreSQL backend choices
