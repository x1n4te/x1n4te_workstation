---
id: memmachine-entity-001
type: entity
title: "MemMachine"
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
  - memory-system
  - open-source
  - ai-agents
  - llm
related:
  - sources/ai-research/memmachine
  - entities/mem0
  - entities/mastras
  - entities/memgpt
  - concepts/agent-memory-taxonomy
---

## MemMachine

**Type:** Open-source AI Agent Memory System  
**Organization:** MemVerge, Inc.  
**Authors:** Wang, Yu, Love, Zhang, Wong, Scargall, Fan  
**Paper:** arXiv:2604.04853v1 [cs.AI], March 2026  
**License:** Apache 2.0  
**Repository:** https://github.com/MemMachine/MemMachine  

### What It Is

A ground-truth-preserving memory system for LLM-based AI agents. MemMachine stores raw conversational episodes at sentence granularity and layers contextualized retrieval on top, minimizing LLM-dependent extraction to reduce cost and factual drift.

### Key Differentiator

Most competing systems (Mem0, Zep) use **per-message LLM extraction** — every conversation turn gets summarized by an LLM into facts stored in a vector/graph DB. Over time, extraction errors compound. MemMachine's insight: **store the raw episode, extract only when necessary**.

### Benchmarks

| Benchmark | Score |
|---|---|
| LoCoMo (GPT-4.1-mini) | **0.9169** |
| LongMemEvalS ablation (GPT-5-mini) | **93.0%** |
| HotpotQA hard | **93.2%** |
| WikiMultiHop (noise) | **92.6%** |

### Architecture

- REST API v2, Python SDK, MCP server
- PostgreSQL + pgvector, SQLite, Neo4j
- Short-term episodic → Long-term episodic → Profile Memory

### See Also

- [[sources/ai-research/memmachine]] — Full source summary
- [[entities/mem0]] — Competitor: LLM-extraction approach
- [[entities/mastras]] — Competitor: observational compression
