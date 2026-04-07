---
id: mem0-entity-001
type: entity
title: "Mem0"
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
  - production-ready
related:
  - entities/memmachine
  - entities/mastras
  - entities/memgpt
  - analyses/memory-systems-comparison
---

## Mem0

**Type:** Production-ready memory layer for AI agents  
**Organization:** Mem0.ai  
**Paper:** Chhikara et al., arXiv:2504.19413  
**Approach:** Per-message LLM extraction to hybrid vector + graph database

### Key Characteristics

- **LLM extraction per message** — every conversation turn summarized by LLM into structured facts
- **Hybrid storage** — vector database (semantic search) + graph database (relationships)
- **High token cost** — MemMachine paper reports ~5x more tokens vs MemMachine
- **Mature product** — production-oriented, not research

### Comparison to MemMachine

| Aspect | Mem0 | MemMachine |
|---|---|---|
| Storage | Extracted facts | Raw episodes |
| LLM dependency | Per-message extraction | Minimal |
| Token cost | Higher | ~80% lower |
| Ground truth | ✗ Drift over time | ✓ Preserved |

### See Also

- [[entities/memmachine]] — Ground-truth-preserving competitor
- [[analyses/memory-systems-comparison]]
