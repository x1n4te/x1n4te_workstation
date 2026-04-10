---
id: agent-memory-taxonomy-001
type: concept
title: "Agent Memory Taxonomy: STM, Episodic, Semantic, Procedural"
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
  - cognitive-science
  - taxonomy
  - ai-agents
related:
  - concepts/episodic-vs-semantic-memory
  - entities/memmachine
  - sources/ai-research/memmachine
  - concepts/llm-wiki-pattern
---

## Agent Memory Taxonomy

AI agent memory systems draw from cognitive science and adapt to LLM requirements. Four types are commonly identified:

### 1. Short-Term Memory (STM)

**Cognitive origin:** Atkinson-Shiffrin (1968) — limited-capacity working store.

**In AI agents:**
- Current conversation context
- Finite window of recent turns
- Analogous to RAM in an OS
- Usually provided directly in LLM context

**Capacity:** Limited by context window size
**Persistence:** Lost between sessions unless stored externally

### 2. Episodic Memory

**Cognitive origin:** Tulving (1972) — memory of specific experiences bound to time and place.

**In AI agents:**
- Raw records of past interactions (conversational turns)
- Ground truth about what happened
- Episode = one discrete interaction unit with metadata (timestamp, participants, session ID)
- Enables factual recall and auditability

**MemMachine implementation:** Sentence-level indexing, contextualized retrieval, episode clusters

### 3. Semantic Memory (Profile Memory)

**Cognitive origin:** Tulving (1972) — generalized knowledge abstracted from experience.

**In AI agents:**
- User preferences, facts, behavioral patterns
- Distilled from episodic data
- "The user prefers X" vs. "The user said X on date Y"
- Enables personalization without re-reading full history

**MemMachine implementation:** Profile Memory — structured user profiles extracted from conversation

### 4. Procedural Memory

**Cognitive origin:** Skill and habit learning — "how to do" knowledge.

**In AI agents:**
- Learned tool-use patterns
- Workflow steps and decision heuristics
- Reusable action strategies
- Multi-step task execution knowledge

**Status in major systems:** Most systems (MemMachine, Mem0, Zep) do NOT fully implement procedural memory. It remains an open research problem.

---

## Comparison Matrix

| Memory Type | What it stores | Persistence | LLM involvement | Example |
|---|---|---|---|---|
| Short-term (STM) | Current context | Session-only | Full — always in context | Current conversation turns |
| Episodic | Raw past interactions | Long-term | Minimal — raw storage | "User said X on March 3" |
| Semantic (Profile) | Distilled facts/preferences | Long-term | Per-extraction | "User prefers vegetarian" |
| Procedural | Skills, strategies, rules | Long-term | Per-application | "Use tool X for task Y" |

---

## See Also

- [[concepts/episodic-vs-semantic-memory]] — Detailed episodic vs semantic comparison
- [[entities/memmachine]] — Implements STM + episodic + profile
- LLM wiki pattern — Knowledge management analog: raw/ = episodic, wiki/ = semantic
