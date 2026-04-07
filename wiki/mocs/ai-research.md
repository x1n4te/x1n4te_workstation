---
id: ai-research-moc-001
type: MOC
title: "AI Research — Map of Content"
created: 2026-04-07
updated: 2026-04-07
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
  - sources/ai-research/ai-2027
  - sources/ai-research/memmachine
  - sources/ai-research/dspy-declarative-prompt-optimization
---

# AI Research — Map of Content

*Reading path and overview for AI research in the vault.*

---

## Overview

AI research in this vault covers three primary themes:

1. **AI Agent Memory Systems** — How AI agents maintain persistent memory across sessions (MemMachine, Mem0, Mastra, MemGPT)
2. **Prompt Optimization** — Declarative and learned approaches to LLM prompt engineering (DSPy)
3. **AI Futures & Forecasting** — Long-range AI scenario planning (AI-2027)

---

## Agent Memory Systems

*Start here if researching how AI agents remember.*

### Core Reading Path

1. [[concepts/agent-memory-taxonomy]] — Four memory types: STM, episodic, semantic, procedural
2. [[concepts/episodic-vs-semantic-memory]] — Deep dive: episodic (ground truth) vs. semantic (distilled)
3. [[entities/memmachine]] — Ground-truth-preserving memory system (best-in-class preservation)
4. [[analyses/memory-systems-comparison]] — Full architectural comparison table

### Quick Reference: Systems

| System | Ground Truth | Benchmark | Token Cost |
|---|---|---|---|
| [[entities/memmachine|MemMachine]] | ✓ | LoCoMo 0.9169 | Low (~80% less vs Mem0) |
| [[entities/mem0|Mem0]] | ✗ | — | High |
| [[entities/mastras|Mastra]] | ✗ | 94.87% LongMemEval | Very low |
| [[entities/memgpt|MemGPT]] | Partial | — | Variable |

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

## AI Futures

*Start here for long-range AI forecasting.*

### Core Reading Path

1. [[sources/ai-research/ai-2027]] — AI-2027 scenario document
2. [[entities/openbrain]] — Fictional AGI company in AI-2027
3. [[entities/deepcent]] — Fictional Chinese AI competitor

---

## Open Questions / Research Gaps

- Procedural memory not implemented in any current system
- Temporal reasoning remains limited across all systems
- LongMemEvalM evaluation pending (500 sessions, ~1.5M tokens/question)
- DSPy evaluated on reasoning/RAG/summarization — needs testing on classification tasks
- How do agent memory systems perform under adversarial conditions?

---

## Thesis Relevance

**WIMS-BFP** uses a local Qwen2.5-3B SLM for threat detection on Suricata logs. Relevant connections:

- [[entities/memmachine|MemMachine]] episodic memory → incident audit trail design
- [[entities/dspy|DSPy]] declarative prompt optimization → automated threat classification prompt tuning
- [[sources/ai-research/ai-2027|AI-2027]] AGI timeline → thesis risk assessment for AI components
