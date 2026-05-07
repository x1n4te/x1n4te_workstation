---
id: llm-wiki-pattern-001
type: concept
created: 2026-04-12
updated: 2026-04-12
last_verified: 2026-04-12
review_after: 2026-05-12
stale_after: 2026-10-12
confidence: high
source_refs:
  - https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
status: active
tags:
  - llm
  - agents
  - knowledge-management
  - ai-research
related:
  - concepts/agent-memory-taxonomy
  - concepts/episodic-vs-semantic-memory
  - mocs/skills
---

# The Karpathy LLM Wiki — Persistent Knowledge Compounding

**Origin:** Andrej Karpathy's 2025 proposal for building persistent, interlinked knowledge bases that LLMs maintain over time.
**Core idea:** Instead of RAG (which rediscovers knowledge from scratch per query), compile knowledge once into a wiki and keep it current.

---

## The Problem with RAG

Traditional Retrieval-Augmented Generation has fundamental limitations:
- **No synthesis:** Retrieves chunks, not compiled understanding
- **No cross-referencing:** Each query is isolated — no relationship mapping
- **Redundant work:** Re-derives the same synthesis every time
- **No contradiction detection:** Conflicting information coexists silently

## The Wiki Alternative

Three-layer architecture:

```
wiki/
├── SCHEMA.md        # Conventions, tag taxonomy, rules
├── index.md         # Sectioned content catalog
├── log.md           # Chronological action log
├── raw/             # Layer 1: Immutable sources
├── entities/        # Layer 2: People, orgs, products
├── concepts/        # Layer 2: Ideas, patterns, how-tos
├── comparisons/     # Layer 2: Side-by-side analyses
└── queries/         # Layer 2: Filed query results
```

**Division of labor:** The human curates sources and directs analysis. The agent summarizes, cross-references, files, and maintains consistency.

## Why It Works

| Property | RAG | LLM Wiki |
|---|---|---|
| Knowledge compilation | Per-query | Once, then maintained |
| Cross-references | None | Mandatory wikilinks |
| Contradiction detection | None | Flagged in lint passes |
| Synthesis quality | Shallow (chunk-level) | Deep (page-level) |
| Cost over time | Constant (re-derives) | Decreasing (compounds) |
| Human curation | None | Source selection + direction |

## Key Conventions

1. **Three layers:** raw (immutable), wiki (agent-owned), schema (rules)
2. **YAML frontmatter** on every page — enables search, staleness detection, graph view
3. **wikilinks** mandatory — minimum 2 outbound per page
4. **Index + log** as navigational backbone — never skip updates
5. **Page thresholds** — don't create pages for passing mentions (2+ source mentions or central to 1 source)
6. **Tag taxonomy** — controlled vocabulary, add to SCHEMA before using
7. **Lint passes** — orphans, broken links, staleness, contradictions

## Implementation in This Wiki

This vault follows the Karpathy pattern with extensions:
- **TTL system:** `review_after` and `stale_after` dates per category (threat intel: 7 days, architecture: 90 days)
- **MOC pages:** Maps of Content for thematic navigation ([[mocs/wims-bfp]], [[mocs/cybersecurity]])
- **Detail split pages:** Large pages split into main + `-details` sub-page
- **Log rotation:** Archives at 500 entries

## Related

- [[concepts/agent-memory-taxonomy]] — how wiki fits into agent memory hierarchy
- [[concepts/episodic-vs-semantic-memory]] — wiki as semantic memory layer
- [[mocs/skills]] — llm-wiki skill family for ingestion workflows
