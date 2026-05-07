---
id: wims-bfp-orchestrator-ultraplan-001
type: analysis
created: 2026-04-25
updated: 2026-04-25
last_verified: 2026-04-25
review_after: 2026-05-25
stale_after: 2026-07-25
confidence: high
source_refs:
  - concepts/multi-agent-orchestrator-template
  - mocs/wims-bfp
  - analyses/4-agent-pipeline-postmortem
status: active
tags:
  - wims-bfp
  - agents
  - hermes
  - multi-agent
  - design
  - software-dev
  - security
related:
  - concepts/multi-agent-orchestrator-template
  - entities/hermes-agent-setup
  - analyses/4-agent-pipeline-postmortem
  - concepts/delegate-task-architecture
---

# WIMS-BFP Orchestrator Ultraplan v1.0

**Architecture:** Multi-agent swarm specialized for WIMS-BFP thesis development  
**Base Template:** [[concepts/multi-agent-orchestrator-template]]  
**Status:** Design finalized — pending implementation  
**Replaces:** [[analyses/4-agent-pipeline-postmortem]] (abandoned Discord approach)  

---

## 1. Differentiation from Archived 4-Agent Pipeline

| Aspect | Old (Apr 8, Archived) | New (This Plan) |
|--------|----------------------|-----------------|
| Gateway | Discord bot | Hermes CLI / Telegram (actual gateway) |
|| Model mix | MiMo-V2-Pro + Sushi-Coder (never served) | GPT-5.4 xhigh (orchestrator) + minimax-m2.7 (all specialists) |
| Security isolation | None | `wims-sec` always runs via `hermes -p` tmux spawn |
| Git safety | None | Dirty-tree halt + `ALLOW_DIRTY` override |
| Audit trail | None | Per-run directory in `.hermes/orchestrator/runs/` |
| Context layer | None (planned Hindsight RAG) | **Wiki-first** (reads from LLM Wiki directly) |
| Write conflicts | None | `check_write_conflicts.py` serializes overlapping edits |
| Routing | Hardcoded in prompt | Explicit `wims-specialists.json` + LLM judgment hybrid |

---

## 2. Wiki-First Context Injection (No Separate Memory Layer)

The LLM Wiki IS the memory layer. A separate `project-memory` skill with Hindsight/pgvector is redundant — the wiki is already a compounding knowledge base with 189 pages, cross-references, and schema discipline.

### Phase 1 Procedure

```
1. Read MOC: ~/Documents/x1n4te-workstation/wiki/mocs/wims-bfp.md
2. Search wiki: search_files(goal, path=wiki, glob=*.md) → top 5 matches
3. Read relevant pages: read_file(match) for top 3–5
4. Supplement with live codebase: search_files(goal, path=project_root)
5. Assemble context bundle: wiki_pages + live_code_matches + knowledge_gaps
```

**Rules:**
- Wiki pages are the **PRIMARY** source for architecture, security policies, and design decisions.
- Live codebase scan is **SECONDARY** — used only to detect drift from documented state.
- If wiki search returns nothing, state "Knowledge gap: no wiki pages match this goal" and rely on live codebase scan alone.

### Why This Works

| Wiki Content | Role in Context Injection |
|-------------|--------------------------|
| `mocs/wims-bfp.md` | Project orientation — module list, tech stack, sprint status |
| `entities/wims-bfp-database-schema` | Schema reference for any DB task |
| `entities/wims-bfp-api-endpoints` | API contract reference for backend tasks |
| `entities/wims-bfp-rbac-roles` | Role definitions for auth/RLS tasks |
| `concepts/wims-bfp-auth-flow` | Auth flow design for security tasks |
| `concepts/wims-bfp-rls-model` | RLS policy model for audit tasks |
|| `concepts/wims-bfp-threat-model` | Threat model for security review |
|| `sources/wims-bfp-codebase-ingestion-*` | Baseline codebase state for drift detection |
|| `sources/wims-bfp-ch3b-architecture` | Thesis architecture section for alignment |

**What the wiki does NOT cover (live scan needed):**
- Uncommitted files in working tree
- Experimental branches not yet documented
- Stack traces from last failed build
- Files modified since last wiki update

---

## 3. WIMS-BFP Specialist Registry

**File:** `~/.hermes/skills/orchestrator/references/wims-specialists.json`

```json
{
  "schema_version": "1.0",
  "project": "WIMS-BFP",
  "specialists": [
    {
      "name": "wims-sec",
      "description": "Security: RLS, RBAC, Keycloak, OWASP, threat modeling",
      "backend": "hermes_profile",
      "profile_name": "wims-sec",
      "model_hint": "minimax/minimax-m2.7",
      "toolsets": ["file", "terminal", "web"],
      "domains": ["security", "auth", "rls", "rbac", "keycloak", "owasp", "audit"],
      "prompt_prefix": "You are WIMS-SEC. You audit WIMS-BFP for security anti-patterns. You fail closed. You never weaken security for speed. Cite OWASP, CWE, or NIST standards in every finding.",
      "routing_confidence": 0.98,
      "max_concurrent": 1,
      "notes": "ALWAYS isolated tmux spawn. Never delegate_task."
    },
    {
      "name": "wims-db",
      "description": "Database: PostgreSQL, PostGIS, migrations, schema design",
      "backend": "delegate_task",
      "model_hint": "minimax/minimax-m2.7",
      "toolsets": ["file", "terminal"],
      "domains": ["schema", "postgresql", "postgis", "migration", "rls_policy"],
      "prompt_prefix": "You are WIMS-DB. You design and modify PostgreSQL schemas for WIMS-BFP. All changes must be idempotent migration scripts. Never drop data without explicit user confirmation.",
      "routing_confidence": 0.90,
      "max_concurrent": 2
    },
    {
      "name": "wims-be",
      "description": "Backend: FastAPI, Celery, Redis, API endpoints",
      "backend": "delegate_task",
      "model_hint": "minimax/minimax-m2.7",
      "toolsets": ["file", "terminal", "web"],
      "domains": ["api", "fastapi", "celery", "redis", "backend", "python"],
      "prompt_prefix": "You are WIMS-BE. You implement FastAPI endpoints and Celery tasks. Follow existing patterns in src/api/. All endpoints must have Pydantic request/response models. Include docstrings.",
      "routing_confidence": 0.88,
      "max_concurrent": 3
    },
      {
        "name": "wims-fe",
        "description": "Frontend: Next.js, React, TypeScript, UI components",
        "backend": "delegate_task",
        "model_hint": "minimax/minimax-m2.7",
        "toolsets": ["file", "terminal", "web"],
        "domains": ["frontend", "nextjs", "react", "typescript", "ui", "shadcn"],
        "prompt_prefix": "You are WIMS-FE. You implement Next.js pages and components. Use existing UI patterns in src/components/. Prefer server components where possible. Client components only for interactivity.",
        "routing_confidence": 0.85,
        "max_concurrent": 2
      },
      {
        "name": "wims-ops",
        "description": "DevOps: Docker, Docker Compose, CI/CD, deployment",
      "backend": "delegate_task",
      "model_hint": "minimax/minimax-m2.7",
      "toolsets": ["file", "terminal"],
      "domains": ["docker", "compose", "ci_cd", "deployment", "nginx", "infra"],
      "prompt_prefix": "You are WIMS-OPS. You manage Docker Compose services, CI pipelines, and deployment configs. All changes must be tested with `docker compose config` before approval.",
      "routing_confidence": 0.80,
      "max_concurrent": 2
    },
    {
      "name": "wims-doc",
      "description": "Documentation: Thesis alignment, FRS traceability, code docs",
      "backend": "delegate_task",
      "model_hint": "minimax/minimax-m2.7",
      "toolsets": ["file", "web"],
      "domains": ["documentation", "thesis", "frs", "traceability", "markdown"],
      "prompt_prefix": "You are WIMS-DOC. You maintain alignment between codebase and thesis documentation. You update .qmd files, README sections, and FRS traceability matrices. Never modify code files.",
      "routing_confidence": 0.75,
      "max_concurrent": 2
    }
  ]
}
```

---

## 4. WIMS-BFP Security Override Rules

These override the generic threshold heuristic for thesis work. Non-negotiable.

```python
# Rule 1: Auth/RLS changes ALWAYS route through wims-sec
if any(k in task_description.lower() for k in [
    "rls", "policy", "auth", "jwt", "keycloak", "rbac",
    "password", "token", "encrypt", "role", "permission"
]):
    task["specialist"] = "wims-sec"
    task["backend"] = "hermes_profile"
    task["security_sensitive"] = True

# Rule 2: Database migrations touching auth tables ALWAYS sec-audit first
if "migration" in task and any(t in task.get("tables", []) for t in [
    "users", "auth", "identities", "sessions", "roles"
]):
    inject_pre_task("wims-sec", "Audit migration for auth table safety")
```

---

## 5. Execution Backend Assignments

| Specialist | Backend | Rationale |
|------------|---------|-----------|
| `wims-sec` | `hermes_profile` | Isolated tmux session. Security audits must not share context with implementation agents. |
| `wims-db` | `delegate_task` | Fast, iterative. Schema changes need quick feedback loops. |
| `wims-be` | `delegate_task` | Fast. API endpoints are self-contained files. |
| `wims-fe` | `delegate_task` | Fast. UI components are independent. |
| `wims-ops` | `delegate_task` | Docker commands are terminal-heavy but safe. |
| `wims-doc` | `delegate_task` | No code execution, just file editing. |

---

## 6. Common Task Decomposition Patterns

### Pattern A: New FRS Module Implementation

**Goal:** "Implement FRS Module 07 — Incident Reporting with AFOR import"

```
t1  wims-db   Design incident_reports + incident_wildland_afor schema
    depends_on: []
    read_scope:  [database/schema.sql, docs/frs/module-07.md]
    write_scope: [database/migrations/007_incident_reports.sql]
    security_sensitive: true

t2  wims-sec  Audit t1 schema for RLS and PII encryption
    depends_on: [t1]
    read_scope:  [database/migrations/007_incident_reports.sql]
    write_scope: []
    security_sensitive: true

t3  wims-be   Implement FastAPI endpoints for incident CRUD
    depends_on: [t2]
    read_scope:  [src/api/, src/models/]
    write_scope: [src/api/incidents.py, src/models/incident.py]
    security_sensitive: false

t4  wims-fe   Implement Next.js incident form + list view
    depends_on: [t3]
    read_scope:  [src/app/, src/components/]
    write_scope: [src/app/incidents/, src/components/IncidentForm.tsx]
    security_sensitive: false

t5  wims-doc  Update thesis Ch3b with Module 07 implementation details
    depends_on: [t4]
    read_scope:  [docs/thesis/ch3b.qmd, docs/frs/module-07.md]
    write_scope: [docs/thesis/ch3b.qmd]
    security_sensitive: false
```

### Pattern B: Security Hotfix

**Goal:** "Fix RLS bypass in batches_region_read policy"

```
t1  wims-sec  Identify exact RLS bypass vector and draft fix
    depends_on: []
    read_scope:  [database/policies/batches.sql, src/api/batches.py]
    write_scope: [database/policies/batches.sql]
    security_sensitive: true

t2  wims-db   Apply policy fix as idempotent migration
    depends_on: [t1]
    read_scope:  [database/policies/batches.sql]
    write_scope: [database/migrations/2026-04-25-fix-batches-rls.sql]
    security_sensitive: true

t3  wims-be   Update backend to respect new policy constraints
    depends_on: [t2]
    read_scope:  [src/api/batches.py]
    write_scope: [src/api/batches.py]
    security_sensitive: false

t4  wims-sec  Verify fix closes bypass with regression test
    depends_on: [t3]
    read_scope:  [src/tests/test_batches_rls.py]
    write_scope: [src/tests/test_batches_rls.py]
    security_sensitive: true
```

### Pattern C: Thesis-Codebase Sync

**Goal:** "Sync thesis Ch3c with actual security tools implementation"

```
t1  wims-sec  Extract actual security controls from codebase
    depends_on: []
    read_scope:  [src/, docker-compose.yml, nginx.conf]
    write_scope: [.hermes/orchestrator/runs/<id>/t1-security-controls.json]
    security_sensitive: false

t2  wims-doc  Compare extracted controls against thesis claims
    depends_on: [t1]
    read_scope:  [docs/thesis/ch3c.qmd, .hermes/orchestrator/runs/<id>/t1-security-controls.json]
    write_scope: [docs/thesis/ch3c.qmd]
    security_sensitive: false

t3  wims-doc  Flag discrepancies for user review
    depends_on: [t2]
    read_scope:  [docs/thesis/ch3c.qmd]
    write_scope: [docs/thesis/ch3c-discrepancies.md]
    security_sensitive: false
```

---

## 7. Threshold Heuristic (Solo vs. Specialists)

```
IF task matches WIMS-BFP security override rules:
    → ALWAYS use wims-sec (isolated hermes_profile)
ELIF orchestrator_assessment.complexity == "HIGH":
    → specialist
ELIF len(files_expected) > 5:
    → specialist (scope too wide)
ELIF len(tasks) == 1 AND len(files_expected) <= 2 AND complexity == "LOW":
    → orchestrator solo (no delegation)
ELSE:
    → specialist
```

---

## 8. Run Directory & Audit Trail

```
~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/
└── .hermes/
    └── orchestrator/
        ├── runs/
        │   └── 2026-04-25-07d3f9a2/
        │       ├── meta.json              # goal, run_id, project_root
        │       ├── task-graph.json        # full plan
        │       ├── context-bundle.json    # wiki pages + live scan results
        │       ├── approval.md            # "Y" or "modify: ..."
        │       ├── git-status.json        # pre-run git snapshot
        │       ├── conflicts.json         # write-scope overlap report
        │       ├── tasks/
        │       │   ├── t1.prompt.md
        │       │   └── ...
        │       ├── results/
        │       │   ├── t1.result.json
        │       │   └── ...
        │       └── synthesis.md           # final briefing
        └── task-graph-latest.json -> runs/2026-04-25-07d3f9a2/task-graph.json
```

---

## 9. Task Graph Schema (WIMS-BFP Fields)

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
      "specialist": "wims-sec",
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

---

## 10. Safety Gates

### Git Safety
```bash
if [ -n "$(git status --short)" ]; then
  if [ "$ALLOW_DIRTY" != "true" ]; then
    echo "ERROR: Dirty git tree. Commit or set ALLOW_DIRTY=true"
    exit 1
  fi
fi
```

### Write Conflict Detection
```python
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

## 11. Implementation Phases

### Phase 0: Environment (Today)
- Verify `hermes`, `tmux`, `jq`, Python 3.11+, `git`
- Create `~/.hermes/profiles/wims-sec.yaml`
- Create `~/.hermes/skills/orchestrator/references/wims-specialists.json`

### Phase 1: Core Scripts (Day 1)
- `validate_task_graph.py` — schema enforcement
- `check_write_conflicts.py` — overlap detection
- `topo_sort.py` — dependency resolution

### Phase 2: Execution Engine (Day 2)
- `run_delegate_backend.py` — delegate_task wrapper
- `run_profile_backend.sh` — tmux spawn for wims-sec
- `execute_tasks.py` — hybrid backend orchestration

### Phase 3: Orchestrator Skill (Day 3)
- `orchestrator/SKILL.md` — 4-phase system prompt with wiki-first context
- `orchestrate.sh` — entrypoint with git safety + mode flags

### Phase 4: First Live Test (Day 4)
- Goal: "Plan-only: Implement FRS Module 07"
- Verify task graph structure, security placement, no execution

### Phase 5: Security Hardening (Day 5)
- Test dirty-tree halt
- Test write-conflict serialization
- Test wims-sec tmux isolation

---

## 12. File Manifest (What Gets Created)

```
~/.hermes/
├── profiles/
│   ├── orchestrator.yaml
│   └── wims-sec.yaml
└── skills/
    └── orchestrator/
        ├── SKILL.md
        ├── orchestrate.sh
        ├── references/
        │   ├── task-graph-schema.json
        │   └── wims-specialists.json
        └── scripts/
            ├── detect_project_root.sh
            ├── check_git_safety.sh
            ├── validate_task_graph.py
            ├── topo_sort.py
            ├── check_write_conflicts.py
            ├── run_delegate_backend.py
            ├── run_profile_backend.sh
            ├── execute_tasks.py
            └── synthesize.py
```

**NOT included (eliminated):**
- `~/.hermes/skills/project-memory/` — replaced by wiki-first Phase 1
- `query_project_memory.py` — replaced by `search_files` + `read_file` on wiki

---

## 13. Critical WIMS-BFP Constraints

1. **No cloud inference for incident data.** Not applicable — XAI pipeline not in this swarm.
2. **Auth changes = isolated audit.** Any change to auth, RLS, Keycloak, or roles routes through `wims-sec` in a tmux session before any other agent sees the code.
3. **Thesis alignment is first-class.** Every implementation PR must have a corresponding `wims-doc` task that updates the relevant `.qmd` file.
4. **Fail closed on dirty git.** Dirty-tree halt prevents accidental work on uncommitted changes.
5. **Single API key.** All specialists use minimax-m2.7. Orchestrator uses GPT 5.4 xhigh. No mixed providers in specialist layer.
6. **Wiki is the single source of truth.** Agents read from `~/Documents/x1n4te-workstation/wiki/` before any live codebase scan.

---

## 14. Validation Matrix

| Test # | Scenario | Expected |
|--------|----------|----------|
| 1 | "Implement FRS Module 09" | Task graph includes wims-sec audit before wims-db migration |
| 2 | "Fix auth loop" | wims-sec spawned via `hermes -p wims-sec`, not `delegate_task` |
| 3 | "Update XAI pipeline" | model_hint forced to `local/qwen2.5-3b`, no OpenRouter call |
| 4 | Dirty git tree + no `ALLOW_DIRTY` | Halt before task generation |
| 5 | t1 and t2 both write `database/schema.sql` | conflicts.json non-empty, tasks serialized |
| 6 | "Sync thesis Ch3c" | wims-doc only, no code file modifications |
| 7 | Cyclic dependency | validate_task_graph.py exits 1 |
| 8 | Plan-only mode | JSON to stdout, no tmux sessions created |
| 9 | Wiki-first context | Orchestrator reads `mocs/wims-bfp.md` before codebase scan |
| 10 | Security classification | Explicit LLM judgment, not substring keyword match |

---

## Related

- [[concepts/multi-agent-orchestrator-template]] — Generic template this specializes
- [[analyses/4-agent-pipeline-postmortem]] — Lessons from abandoned Discord approach
- [[entities/hermes-agent-setup]] — Current single-agent operational setup
- [[concepts/delegate-task-architecture]] — Hermes child agent spawning mechanism
- [[mocs/wims-bfp]] — Project Map of Content (orchestrator reads this first)
