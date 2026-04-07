---
id: mastras-entity-001
type: entity
title: "Mastra"
created: 2026-04-07
updated: 2026-04-07
last_verified: 2026-04-07
review_after: 2026-05-07
stale_after: 2026-07-07
confidence: medium
source_refs:
  - raw/ai-research/2604.04853v1.pdf
status: active
tags:
  - memory-system
  - llm-agents
  - observational-memory
  - compression
related:
  - entities/memmachine
  - entities/mem0
  - analyses/memory-systems-comparison
---

## Mastra

**Type:** AI agent framework with observational memory  
**Organization:** Mastra  
**Paper:** Barnes & Bhagwat (2026) — Mastra Technical Report  
**Approach:** Observational memory via Observer + Reflector background agents that compress conversation history

### Key Characteristics

- **Observational compression** — two background agents (Observer, Reflector) compress conversation into dated observation log
- **No retrieval** — compressed log stays in context always; no external search
- **Excellent benchmarks** — 94.87% on LongMemEval (GPT-5-mini)
- **Loses verbatim access** — cannot do open-ended knowledge discovery or audit/compliance recall
- **Strong prompt caching** — aggressive compression enables efficient context reuse

### Comparison to MemMachine

| Aspect | Mastra | MemMachine |
|---|---|---|
| Benchmark | 94.87% LongMemEval | 93.0% LongMemEvalS |
| Ground truth | ✗ Compressed | ✓ Preserved |
| Retrieval | ✗ None | ✓ Contextualized |
| Best for | Closed-domain QA | Audit, compliance, multi-hop |

### Key Insight

Mastra wins on benchmark score. MemMachine wins on factual preservation and audit capability. These are fundamentally different use cases.

### See Also

- [[entities/memmachine]] — Ground-truth-preserving competitor
- [[analyses/memory-systems-comparison]]
