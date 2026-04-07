---
id: closed-learning-loop-001
type: concept
created: 2026-04-07
updated: 2026-04-07
last_verified: 2026-04-07
review_after: 2026-05-07
stale_after: 2026-07-06
confidence: high
source_refs:
  - raw/ai-research/HERMES-AGENT.md
status: active
tags:
  - hermes-agent
  - learning-loop
  - procedural-memory
  - autonomous-learning
related:
  - concepts/procedural-memory
  - entities/hermes-agent
---

# Closed Learning Loop Architecture

**Framework:** Hermes-Agent (Nous Research)  
**Section:** 2.1 of architectural analysis  

---

## Definition

The closed learning loop is Hermes-Agent's defining architectural characteristic. Unlike traditional agent frameworks that function as stateless interpreters (execute → return → discard reasoning pathway), Hermes-Agent treats every successful task execution as **actionable training data** for future operations.

---

## The 5-Phase Loop

| Phase | Description |
|---|---|
| **Execute** | Agent performs task using available tools |
| **Evaluate** | Agent assesses success/failure of the execution |
| **Extract** | If complex (>5 tool calls, API errors, or user corrections), triggers extraction |
| **Refine** | Distills raw token-heavy trajectory into structured SKILL.md format |
| **Retrieve** | On future similar task, skill is loaded → bypasses re-derivation |

---

## Trigger Conditions

A task triggers procedural memory extraction when it meets any of:
- Requires **>5 distinct tool calls**
- Involves **successful navigation of unexpected API errors**
- Required **user-corrected approach** to complete

---

## Contrast With Traditional Agents

| Traditional Agent | Hermes-Agent Closed Loop |
|---|---|
| Stateless — reasoning discarded after task | Stateful — reasoning compiled into SKILL.md |
| Same problem = same planning cost every time | Same problem = skill retrieval, near-zero planning cost |
| Brittle when task deviates from expected path | User corrections auto-captured as training data |
| Scales poorly with task complexity | Complexity compounds into reusable skills |

---

## Relevance

This is the core innovation that makes Hermes-Agent a "self-improving" agent. Each complex task the WIMS-BFP agent solves (RLS policy fixes, Celery task patterns, Suricata rule authoring) can be compiled into a skill that bypasses planning on the next similar task.

---

## Related

- [[concepts/procedural-memory]] — The output of the Extract phase
- [[entities/hermes-agent]] — Parent entity
