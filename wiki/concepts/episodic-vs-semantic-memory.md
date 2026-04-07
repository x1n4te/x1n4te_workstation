---
id: episodic-semantic-memory-001
type: concept
title: "Episodic vs. Semantic Memory (AI Agent Context)"
created: 2026-04-07
updated: 2026-04-07
last_verified: 2026-04-07
review_after: 2026-05-07
stale_after: 2026-07-07
confidence: high
source_refs:
  - raw/ai-research/2604.04853v1.pdf
  - raw/sources/karpathy-llm-wiki-gist.md
status: active
tags:
  - cognitive-science
  - memory-systems
  - episodic-memory
  - semantic-memory
  - tulving
related:
  - entities/memmachine
  - sources/ai-research/memmachine
  - concepts/agent-memory-taxonomy
  - concepts/llm-wiki-pattern
---

## Episodic vs. Semantic Memory (AI Agent Context)

### Origin

Drawn from cognitive science — specifically Tulving's taxonomy (1972) and the Atkinson-Shiffrin multi-store model (1968). Adapted to AI agent systems with approximate implementations.

### Episodic Memory

**Definition:** Memory of specific personal experiences, bound to time and place. In AI agents: each conversational turn = one episode.

**Characteristics:**
- **Ground truth**: stores what actually happened, verbatim or near-verbatim
- **Point-in-time**: each episode has a timestamp and session ID
- **High fidelity**: preserves exact statements, decisions, facts
- **Queryable**: "What did the user say about X in session 7?"

**AI Agent usage:**
- Factual recall
- Conversation history reconstruction
- Audit trails
- Evidence for decisions
- Cross-session continuity

### Semantic Memory

**Definition:** Generalized knowledge abstracted from experience — facts, concepts, preferences. In AI agents: Profile Memory.

**Characteristics:**
- **Generalized**: "The user prefers vegetarian restaurants" (not "User said 'I am vegetarian' on March 3")
- **Approximate**: distilled from episodic data, not raw record
- **Cross-session**: stable across interactions
- **Lower fidelity**: loses specific context in exchange for generalization

**AI Agent usage:**
- Personalization
- Preference-aware responses
- Tone and content adaptation
- Quick context without re-reading full history

### When to Use Which

| Criterion | Episodic | Semantic |
|---|---|---|
| Accuracy need | High — ground truth | Moderate — approximation |
| Temporal scope | Specific past event | General, cross-session |
| Data form | Raw conversation | Extracted facts |
| Example query | "What did I say about X?" | "What foods do I like?" |

### In MemMachine

MemMachine implements:
- **Episodic memory** → short-term + long-term store of raw episodes
- **Profile memory** (semantic) → distilled user preferences, facts, patterns

Procedural memory (skills, strategies) is NOT implemented.

### Tension: Preservation vs. Compression

This is the core design trade-off in agent memory systems:

| System | Choice | Implication |
|---|---|---|
| MemMachine | Preserve raw episodes | High recall, needs good retrieval |
| Mastra | Compress aggressively (Observer+Reflector) | Low context cost, loses verbatim access |
| Mem0 | Extract to facts | Lower storage, compounding extraction error |
| MemOS | Multi-tier (text+KV+parametric) | Most flexible, most complex |

### Connection to LLM Wiki Pattern

The LLM Wiki pattern (Karpathy) is analogous to **semantic memory at the knowledge level**: instead of retrieving raw source documents on every query, the LLM pre-compiles them into synthesized concept pages. The `raw/` layer is episodic (immutable ground truth), and `wiki/` is semantic (synthesized distillation).

---

## See Also

- [[concepts/agent-memory-taxonomy]] — Full taxonomy: STM, episodic, semantic, procedural
- [[entities/memmachine]] — Implements this taxonomy
- [[concepts/llm-wiki-pattern]] — Analogous to the episodic/semantic split
