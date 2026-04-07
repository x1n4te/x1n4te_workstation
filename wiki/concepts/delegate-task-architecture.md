---
id: delegate-task-architecture-001
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
  - delegation
  - subagent
  - multi-agent
  - parallelism
related:
  - concepts/model-routing
  - concepts/closed-learning-loop
  - entities/hermes-agent
---

# delegate_task Architecture

**Framework:** Hermes-Agent (Nous Research)  
**Location:** `tools/delegate_tool.py`  
**Section:** 4.2 of architectural analysis  

---

## Definition

The `delegate_task` function allows a parent orchestrator agent to spawn isolated child sub-agents for compartmentalized parallel work. Each child operates with its own localized conversation context, restricted toolsets, and entirely separate terminal session.

---

## Standard Delegation (ThreadPoolExecutor)

| Parameter | Value |
|---|---|
| Max parallel children | 3 |
| Max depth (grandchildren) | 0 (MAX_DEPTH=2 hard cap) |
| Execution model | ThreadPoolExecutor, synchronous batch |
| Parent behavior | Blocks until all children complete or timeout |
| Failure handling | Child failure is final; parent handles retry/monitoring |

```python
delegate_task(
  goal="Extract dates from this JSON file",
  context=isolated_context,
  toolsets=['terminal', 'file']  # Restricted per sub-task
)
```

---

## Mass Parallelism Mode (Background Subprocesses)

For tasks requiring 10+ parallel agents (e.g., analyzing 50 Git worktrees, scraping dozens of domains), the ThreadPoolExecutor limit is bypassed:

```python
terminal(background=true)  # Spawns independent OS-level hermes-agent process
```

Parent assumes purely supervisory role using `process(poll)` to track health, exit codes, and completion. This shifts paradigm from "conversational agent with tools" to **"Agent OS" orchestrating a distributed compute cluster**.

---

## Isolation Properties

Each child agent is:
- **Context-blind** — no access to parent's memory, global state, or strategic goals
- **Toolset-restricted** — only sees tools needed for its specific sub-task
- **Session-isolated** — entirely separate terminal session
- **Failure-contained** — one child's crash does not cascade to parent

This is critical for preventing context collapse and token exhaustion during large-scale research operations.

---

## FRS Role Analogy (WIMS-BFP)

The delegation hierarchy maps to WIMS-BFP's FRS escalation:

| Hermes delegate_task | WIMS-BFP FRS |
|---|---|
| Parent orchestrator | SYSTEM_ADMIN / orchestrator |
| Child agent | REGIONAL_ENCODER (task-specific) |
| Context isolation | RLS enforcement per user_id |
| MAX_DEPTH=2 | Role escalation depth |

---

## Model Routing with Delegation

Asymmetric model assignment applies:
- **Parent (orchestrator):** Frontier model (Claude 3.5 Sonnet/Opus) — strategic reasoning, synthesis
- **Children (workers):** Fast/cheap (Gemini Flash 2.0, Claude 3.5 Haiku, Qwen 3.5 MLX) — data extraction, parsing

Configured via `delegation.model` + `delegation.provider` in `config.yaml`.

---

## Related

- [[concepts/model-routing]] — Asymmetric model assignment
- [[entities/hermes-agent]] — Parent entity
