---
id: memory-systems-comparison-001
type: analysis
title: "AI Agent Memory Systems: Architectural Comparison"
created: 2026-04-07
updated: 2026-04-07
last_verified: 2026-04-07
review_after: 2026-05-07
stale_after: 2026-07-07
confidence: high
source_refs:
  - raw/ai-research/2604.04853v1.pdf
status: active
tags:
  - memory-systems
  - llm-agents
  - comparative-analysis
  - rag
  - retrieval
related:
  - entities/memmachine
  - entities/mem0
  - entities/mastras
  - entities/memgpt
  - concepts/agent-memory-taxonomy
  - sources/ai-research/memmachine
---

## AI Agent Memory Systems: Architectural Comparison

### Systems Covered

| System | Organization | Approach |
|---|---|---|
| MemMachine | MemVerge | Ground-truth-preserving episodic + profile |
| Mem0 | Mem0.ai | LLM extraction to hybrid vector+graph DB |
| MemGPT | Packer et al. (2024) | Virtual memory hierarchy / OS-inspired |
| Mastra | Mastra | Observational compression (Observer+Reflector) |
| Zep | Zep AI | Temporal knowledge graph |
| MemOS | Li et al. (2025) | Unified MemCube: text+KV+parametric |
| Memobase | memodb.io | Structured memory storage |
| LangMem | LangChain | Memory for LangChain ecosystem |

---

### Core Architectural Dimensions

**1. Ground Truth Preservation**

| System | Stores Raw Episodes? | Extraction Dependency |
|---|---|---|
| MemMachine | ✓ Sentence-level | Minimal |
| MemGPT | Partial | Memory paging decisions |
| Mem0 | ✗ | Per-message extraction |
| Mastra | ✗ | Aggressive compression |
| Zep | Partial | Temporal graph |
| MemOS | Mixed | Varies by MemCube type |

**2. Retrieval Strategy**

| System | Retrieval Method |
|---|---|
| MemMachine | Contextualized: nucleus + neighboring context → episode clusters |
| Mem0 | Hybrid vector similarity + graph traversal |
| MemGPT | Virtual memory paging (context ↔ external storage) |
| Mastra | No retrieval — compressed observation log always in context |
| Zep | Temporal knowledge graph + vector search |
| MemOS | MemCube scheduler: predictive preloading, cross-type transforms |

**3. Memory Types Implemented**

| System | STM | Episodic | Semantic | Procedural |
|---|---|---|---|---|
| MemMachine | ✓ | ✓ | ✓ (Profile) | ✗ |
| Mem0 | ✓ | ✓ | ✓ | ✗ |
| MemGPT | ✓ | ✓ | ✗ | ✗ |
| Mastra | ✓ | ✗ | ✓ (Observation log) | ✗ |
| Zep | ✓ | ✓ | ✓ | ✗ |
| MemOS | ✓ | ✓ (text MemCube) | ✓ | Partial (via LoRA) |

**4. Token Cost Efficiency**

| System | Token Model |
|---|---|
| MemMachine | ~80% fewer vs Mem0 (selective retrieval vs. full context) |
| Mastra | Aggressive caching + compression — very low retrieval cost |
| MemGPT | Variable — paging decisions affect context size |
| Mem0 | High — per-message LLM extraction |
| Zep | Moderate — graph + vector hybrid |
| MemOS | Variable — MemCube type determines cost |

---

### Key Findings from MemMachine Paper

1. **Retrieval-stage optimizations dominate ingestion changes** (+4.2% retrieval depth vs +0.8% chunking on LongMemEvalS)
2. **Smaller answer models outperform larger ones** when co-optimized (GPT-5-mini > GPT-5, +2.6%)
3. **Ground truth preservation enables better multi-hop reasoning** — retrieval strategies can be layered without modifying storage
4. **Contextualized retrieval** solves embedding dissimilarity in conversational data

---

### Design Tension: Preservation vs. Compression

```
MemMachine ──────────── Mastra
(preserve raw)              (compress aggressively)
    │                           │
    └── HotpotQA: 93.2% ───────┘
    └── LongMemEval: 93.0%
    └── ~80% fewer tokens vs Mem0
    └── Ground truth: ✓

Mastra:
    └── LongMemEval: 94.87% (GPT-5-mini)
    └── Excellent for closed-domain QA
    └── Loses verbatim access
    └── Not suitable for audit/compliance

→ MemMachine wins on audit; Mastra wins on benchmark score
```

---

## See Also

- [[entities/memmachine]] — Primary entity page
- [[sources/ai-research/memmachine]] — Full paper summary
- [[concepts/agent-memory-taxonomy]] — Memory type taxonomy
- [[concepts/episodic-vs-semantic-memory]] — Cognitive science basis
