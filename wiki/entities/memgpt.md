---
id: memgpt-entity-001
type: entity
title: "MemGPT"
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
  - virtual-memory
  - os-inspired
related:
  - entities/memmachine
  - entities/mem0
  - entities/mastras
  - analyses/memory-systems-comparison
---

## MemGPT

**Type:** OS-inspired virtual memory hierarchy for LLMs  
**Authors:** Packer, Wooders, Lin, Fang, Patil, Stoica, Gonzalez (2024)  
**Paper:** arXiv:2310.08560  
**Approach:** Virtual memory paging between main context and external storage

### Key Characteristics

- **OS-inspired** — treats LLM context like OS memory: paging between fast context and slow external storage
- **MemGPT** — "LLMs as Operating Systems"
- **LLM-driven paging decisions** — the model decides what to keep in context vs. externalize
- **Partial ground truth** — some episodes stored externally, retrieval quality depends on paging decisions
- **Pioneering work** — established the agent memory research thread

### Comparison to MemMachine

| Aspect | MemGPT | MemMachine |
|---|---|---|
| Arch style | OS/virtual memory paging | Ground-truth episodic + profile |
| LLM dependency | High (paging decisions) | Low (retrieval only) |
| Ground truth | Partial | ✓ Full preservation |
| Complexity | Higher (paging logic) | Lower (retrieval + indexing) |

### See Also

- [[entities/memmachine]] — Ground-truth-preserving competitor
- [[analyses/memory-systems-comparison]]
