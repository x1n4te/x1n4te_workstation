---
id: multi-agent-orchestrator-template-001
type: concept
created: 2026-04-25
updated: 2026-04-25
last_verified: 2026-04-25
review_after: 2026-05-25
stale_after: 2026-07-25
confidence: high
source_refs:
  - sessions/2026-04-25.md
status: active
tags:
  - agents
  - hermes
  - multi-agent
  - design
  - software-dev
related:
  - concepts/delegate-task-architecture
  - analyses/4-agent-pipeline-postmortem
  - entities/hermes-agent-setup
  - concepts/hermes-production-stack
  - concepts/slopcodebench-iterative-degradation
---

# Multi-Agent Orchestrator Template

**Architecture:** Project-agnostic multi-agent swarm for Hermes Agent  
**Status:** v1 design finalized — pending implementation  
**Replaces:** [[analyses/4-agent-pipeline-postmortem]] (abandoned Discord-based approach)  
**Scope:** Generic template; WIMS-BFP specialization documented in [[analyses/wims-bfp-orchestrator-ultraplan]]

---

## Overview

A **project-agnostic multi-agent template** where:
- **1 orchestrator** (frontier model, high reasoning) decides *what* and *when*
- **3–7 specialist agents** (smaller models) execute *in domain*
- **Hermes Agent** serves as the **execution bus** — it spawns, routes, and aggregates

Key design tension resolved: **autonomy vs. control**. Specialists act independently within their domain, but the orchestrator retains final say on cross-domain conflicts.

---

## Core Principles

1. **Hermes-Native**: Uses actual Hermes mechanics (`delegate_task`, `hermes -p`, tmux, skills as procedural context — not as microservices).
2. **Fail-Closed**: No automated execution without git safety check. Dirty tree → halt unless `ALLOW_DIRTY=true`.
3. **Deterministic Routing**: No LLM-guessed routing in v1. Explicit `specialists.json` registry. Orchestrator plans; registry routes.
4. **Audit Everything**: Every run persists to `.hermes/orchestrator/runs/<uuid>/`.
5. **Write Conflict Detection**: Two agents cannot hold write locks on the same file concurrently. Serialize or fail.
6. **Hybrid Execution**: `delegate_task` for generalists, `hermes -p <profile>` for security/isolated work.

---

## Architecture

```
USER GOAL (natural language)
         │
         ▼
┌──────────────────────────────────────────────────┐
│  ORCHESTRATOR (Hermes profile, GPT 4.5 xhigh)   │
│                                                  │
│  Phase 1 — Context Injection                    │
│  ├── Query project-memory script (Qwen2.5-3B)   │
│  ├── search_files() scan if needed              │
│  └── Build context bundle (tokens: controlled)  │
│                                                  │
│  Phase 2 — Task Decomposition                    │
│  ├── LLM classifies security sensitivity         │
│  ├── LLM assesses complexity (LOW/MEDIUM/HIGH)  │
│  ├── Threshold check: solo vs specialists       │
│  ├── Discover specialists from specialists.json │
│  └── Output: JSON task graph (human review)     │
│                                                  │
│  Phase 3 — Approval Gate (interactive default)  │
│                                                  │
│  Phase 4 — Execution                            │
│  ├── Topological sort by dependencies           │
│  ├── Write-conflict detection                   │
│  ├── delegate_task for delegate_backend tasks   │
│  ├── tmux spawn for hermes_profile tasks        │
│  └── Circuit breaker: max 5 concurrent          │
│                                                  │
│  Phase 5 — Synthesis                           │
│  ├── Gather SpecialistResult[]                 │
│  ├── Merge artifacts, flag conflicts           │
│  └── Deliver briefing to user                  │
└──────────────────────────┬───────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │  swe        │  │  sec-audit  │  │  arch-design│
    │  delegate   │  │  hermes -p  │  │  delegate   │
    └─────────────┘  └─────────────┘  └─────────────┘
```

---

## Task Graph Schema

Each orchestrator output must conform to:

```json
{
  "schema_version": "1.0",
  "run_id": "uuid",
  "project_root": "/abs/path",
  "orchestrator_assessment": {
    "goal_summary": "string",
    "project_context_hash": "string",
    "complexity": "LOW|MEDIUM|HIGH",
    "security_sensitive": true,
    "security_reasoning": "string"
  },
  "tasks": [
    {
      "id": "t1",
      "specialist": "sec-audit",
      "backend": "delegate_task|hermes_profile",
      "prompt": "Self-contained instruction...",
      "depends_on": [],
      "estimated_minutes": 20,
      "routing_confidence": 0.92,
      "security_sensitive": true,
      "read_scope": ["src/auth/**"],
      "write_scope": [],
      "files_expected": []
    }
  ],
  "routing_reasoning": "string"
}
```

**Key fields:**
- `backend`: `delegate_task` (fast, shared context) or `hermes_profile` (isolated tmux session)
- `read_scope`/`write_scope`: filesystem paths for conflict detection
- `routing_confidence`: orchestrator's self-assessed routing certainty (0.0–1.0)

---

## Threshold Heuristic (Solo vs. Specialists)

```
IF orchestrator_assessment.security_sensitive:
    → ALWAYS use specialists (security override)
ELIF len(tasks) == 1 AND len(files_expected) <= 2 AND complexity == "LOW":
    → orchestrator solo (skip to synthesis, no delegation)
ELIF len(files_expected) > 5:
    → specialist (scope too wide)
ELIF complexity == "HIGH":
    → specialist (complexity too high)
ELSE:
    → specialist
```

**Security override:** When security-sensitive, at least one `sec-audit` task must exist in the graph. Security classification is an explicit **Phase 1 LLM judgment**, not substring keyword matching.

---

## Specialist Registry

Explicit `specialists.json` — no magic scanning in v1.

```json
{
  "schema_version": "1.0",
  "specialists": [
    {
      "name": "swe",
      "description": "Software implementation and testing",
      "backend": "delegate_task",
      "model_hint": "minimax/minimax-m2.7",
      "toolsets": ["file", "terminal", "web"],
      "domains": ["implementation", "testing", "refactor"],
      "prompt_prefix": "You are SWE...",
      "routing_confidence": 0.8,
      "max_concurrent": 3
    },
    {
      "name": "sec-audit",
      "description": "Security review, auth, RLS, OWASP",
      "backend": "hermes_profile",
      "profile_name": "sec-audit",
      "model_hint": "minimax/minimax-m2.7",
      "toolsets": ["file", "terminal", "web"],
      "domains": ["security", "auth", "rls", "owasp"],
      "prompt_prefix": "You are SEC-AUDIT...",
      "routing_confidence": 0.95,
      "max_concurrent": 1
    }
  ]
}
```

**Conflict resolution** (when two specialists claim the same domain):
1. Prefer more specific keyword match
2. Prefer higher `routing_confidence`
3. If tied and security-sensitive, prefer `sec-audit`
4. Otherwise spawn both and synthesize

---

## Execution Backends

| Backend | Mechanism | Isolation | Use Case |
|---------|-----------|-----------|----------|
| `delegate_task` | Hermes `delegate_task(tasks=[...])` | Weak (shared process) | 1–3 small subtasks, general implementation |
| `hermes_profile` | `hermes -p <profile> chat -q` in tmux | Strong (separate process) | Security audits, long jobs, codebase-wide work |

---

## Execution Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Interactive** | Default | Emits approval block, pauses for `Y/n/modify` |
| **Batch** | `HERMES_BATCH=true` | Skips approval, proceeds directly to execution |
| **Plan-only** | `PLAN_ONLY=true` | Emits `task-graph.json`, exits 0, no delegation |

---

## Run Directory Structure

Every execution persists:

```
.hermes/orchestrator/runs/<uuid>/
├── task-graph.json          # The plan
├── context-bundle.json      # Project memory output
├── approval.md              # User approval record
├── tasks/
│   ├── t1.prompt.md
│   └── t2.prompt.md
├── results/
│   ├── t1.result.json
│   └── t2.result.json
├── conflicts.json           # Write conflict report
├── git-status.json          # Git state snapshot
└── synthesis.md             # Final orchestrator briefing
```

---

## Safety Gates

### Git Safety
```bash
if git status --short | grep -q .; then
  if [ "$ALLOW_DIRTY" != "true" ]; then
    exit 1  # Halt
  fi
fi
```

### Write Conflict Detection
```python
# check_write_conflicts.py
from collections import defaultdict

def detect_conflicts(tasks):
    writes = defaultdict(list)
    for task in tasks:
        for path in task.get("write_scope", []):
            writes[path].append(task["id"])
    return {path: ids for path, ids in writes.items() if len(ids) > 1}
```

Conflicting tasks are serialized (implicit dependency edges added before topo sort).

---

## File Manifest (What Ships)

```
~/.hermes/
├── profiles/
│   ├── orchestrator.yaml
│   └── sec-audit.yaml
├── skills/
│   ├── orchestrator/
│   │   ├── SKILL.md
│   │   ├── orchestrate.sh
│   │   ├── references/
│   │   │   ├── task-graph-schema.json
│   │   │   └── specialists.json
│   │   └── scripts/
│   │       ├── detect_project_root.sh
│   │       ├── check_git_safety.sh
│   │       ├── validate_task_graph.py
│   │       ├── topo_sort.py
│   │       ├── check_write_conflicts.py
│   │       ├── run_delegate_backend.py
│   │       ├── run_profile_backend.sh
│   │       ├── execute_tasks.py
│   │       └── synthesize.py
│   ├── project-memory/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── query_project_memory.py
│   └── _scaffolds/
│       └── specialist/
│           └── SKILL.md
```

---

## Differentiation from Archived 4-Agent Pipeline

| Aspect | Old (Archived) | New Template |
|--------|---------------|--------------|
| Control plane | Discord bot | Hermes CLI / Telegram |
| Discovery | Manual profile config | Explicit `specialists.json` |
| Routing | Hardcoded in orchestrator prompt | Registry + LLM judgment hybrid |
| Execution | `delegate_task` only | Hybrid: `delegate_task` + `hermes_profile` |
| Safety | None | Git dirty-tree gate + write-conflict detection |
| Audit | None | Per-run directory with full artifact persistence |
| Security classification | None | Phase 1 explicit LLM judgment |
| Context injection | None | `query_project_memory.py` with RAG fallback |

---

## Related

- [[analyses/wims-bfp-orchestrator-ultraplan]] — WIMS-BFP specialization of this template
- [[concepts/delegate-task-architecture]] — Hermes child agent spawning mechanism
- [[analyses/wims-bfp-orchestrator-ultraplan]] — WIMS-BFP specialization of this template
- [[analyses/4-agent-pipeline-postmortem]] — Lessons from the abandoned Discord approach
- [[entities/hermes-agent-setup]] — Current single-agent operational setup
