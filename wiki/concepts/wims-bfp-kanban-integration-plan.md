---
id: wims-bfp-kanban-integration-plan-001
type: plan
created: 2026-04-30
updated: 2026-04-30
review_after: 2026-05-07
stale_after: 2026-05-14
confidence: high
status: in_progress
tags:
  - kanban
  - wims-bfp
  - integration
  - orchestrator
  - multi-agent
related:
  - concepts/multi-agent-orchestrator-template
  - concepts/kanban-worker
  - autonomous-ai-agents/kanban-worker
  - entities/wims-bfp-agentic-workflow
  - analyses/wims-bfp-orchestrator-ultraplan
---

# WIMS-BFP Kanban Integration — PR #8 Plan

**PR #8 goal:** Wire the existing WIMS-BFP orchestrator template to the Hermes Kanban board. Map the orchestrator's 5-phase execution (decompose → implement → review → iterate → PR) to a P2 pipeline on the board. Add P4 recurring journal tasks for daily triage and 3-day architecture reviews.

**Scope:** Profile creation + board setup + cron wiring. No changes to `kanban_db.py`, `kanban.py`, or `dispatch.py`.

---

## What Is Being Integrated

The existing [[concepts/multi-agent-orchestrator-template]] designs a per-session orchestrator that:
- Decomposes a user goal into a task graph
- Routes tasks to specialists via `delegate_task` or `hermes -p`
- Synthesizes results in-memory
- Dies when the session ends

**The problem:** workers can't survive session restarts, the task graph is ephemeral, and there's no persistent board for human interposition or cross-session visibility.

**Kanban's fix:** The orchestrator becomes a **kanban-worker profile**. The task graph is written to the board as tasks with dependency links. Workers are OS processes that survive session restarts. The board is the single source of truth.

---

## Architecture: How Orchestrator Maps to Kanban

```
USER (Telegram/CLI)
    │
    │ /kanban create "Implement incident CRUD API"
    │
    ▼
kanban.db (SQLite WAL)
    │
    ├─ t_parent (orchestrator task)
    │     │
    │     ├── t_impl_1 (swe: implement endpoint)
    │     ├── t_impl_2 (swe: write tests)
    │     └── t_review (sec-audit: security review)
    │
    ▼
dispatcher (cron, 60s)
    │ claims ready tasks → spawns hermes -p <profile>
    ▼
workers (OS processes)
    ├─ swe-worker: implements endpoint, posts comment, completes t_impl_1
    ├─ swe-worker: writes tests, posts comment, completes t_impl_2
    └─ sec-audit: reviews, posts findings, completes t_review
```

**Key insight:** The orchestrator profile doesn't do the implementation work — it **plans and coordinates**. Implementation happens in specialist workers. The orchestrator's job is to decompose the parent task, create children, link them, and monitor until all children are `done`, then complete itself.

---

## The 5 Profiles to Create

| Profile Name | Role | Workspace |
|-------------|-------|-----------|
| `wims-bfp-orchestrator` | Strategic planner — decomposes goals, creates children, monitors pipeline | `dir:~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/` |
| `wims-bfp-swe` | Software implementation — writes code, runs tests | `worktree` |
| `wims-bfp-sec-audit` | Security review — auth, RLS, OWASP, Keycloak policies | `dir:~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/` |
| `wims-bfp-researcher` | Research — scans HN/ArXiv, thesis chapter writing, trend reports | `dir:~/Documents/x1n4te-workstation/` |
| `wims-bfp-analyst` | Data analysis — PostGIS queries, heatmaps, Celery report generation | `dir:~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/` |

All 5 created via:
```bash
hermes kanban create-worker wims-bfp-orchestrator
hermes kanban create-worker wims-bfp-swe
hermes kanban create-worker wims-bfp-sec-audit
hermes kanban create-worker wims-bfp-researcher
hermes kanban create-worker wims-bfp-analyst
```

Each gets the `kanban-worker` skill + bundled skills seeded. Each gets a domain-specific `SOUL.md`.

---

## P2 Pipeline: Orchestrator Decomposition

### Stage 1 — Orchestrate (P1 Fan-out)

The orchestrator creates one parent task per user goal. It immediately creates child tasks for each step and links them.

```bash
# User creates the top-level task (or orchestrator creates it on behalf of user):
hermes kanban create "Implement National Analyst CRUD + Heatmap" \
  --assignee wims-bfp-orchestrator \
  --body "Implement full CRUD for national analyst role: dashboard, PostGIS heatmaps, CSV/GeoJSON exports, Celery async reports. See PR #78 context."
t_goal=t_N1

# Orchestrator decomposes into children:
hermes kanban create "Implement analyst dashboard UI" --assignee wims-bfp-swe
t_ui=t_N2
hermes kanban link $t_goal $t_ui

hermes kanban create "Implement PostGIS heatmap API" --assignee wims-bfp-swe
t_api=t_N3
hermes kanban link $t_goal $t_api

hermes kanban create "Write API integration tests" --assignee wims-bfp-swe
t_tests=t_N4
hermes kanban link $t_goal $t_tests

hermes kanban create "Security review: RLS + auth" --assignee wims-bfp-sec-audit
t_sec=t_N5
hermes kanban link $t_goal $t_sec

hermes kanban create "Celery async report generation" --assignee wims-bfp-analyst
t_reports=t_N6
hermes kanban link $t_goal $t_reports

# Orchestrator blocks until all children done
hermes kanban block $t_goal
```

### Stage 2 — Parallel Implementation (P1 Fan-out)

Children are all `ready` immediately. Dispatcher claims all 5 in the same tick and spawns 5 workers in parallel:

```
t_N2 (swe): builds dashboard UI
t_N3 (swe): implements PostGIS heatmap API
t_N4 (swe): writes tests
t_N5 (sec-audit): reviews RLS + auth
t_N6 (analyst): implements Celery reports
```

Each worker:
1. Reads task body from `hermes kanban show $KANBAN_TASK_ID`
2. Works in its assigned workspace (`KANBAN_TASK_DIR`)
3. Posts progress/comments
4. Marks `done` on completion

### Stage 3 — Review

When all children are `done`, orchestrator's `recompute_ready()` fires — `t_goal` flips from `todo` → `ready`.

Dispatcher claims `t_goal` and re-spawns orchestrator. Orchestrator:
1. Reads all child task comments (implementation summaries, security findings)
2. Synthesizes into a final comment on `t_goal`
3. Creates a final PR task if needed

### Stage 4 — PR Task

```bash
hermes kanban create "PR: Merge National Analyst CRUD" \
  --assignee wims-bfp-swe \
  --workspace "dir:~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/"
t_pr=t_N7
hermes kanban link $t_goal $t_pr
hermes kanban link $t_sec $t_pr   # security must approve before PR
```

### Stage 5 — Complete

```bash
hermes kanban complete $t_pr
# When t_pr done, orchestrator completes t_goal
hermes kanban complete $t_goal
```

---

## P4 Recurring Journal Tasks

### Daily Triage (every day at 8 AM)

**Task:** `hermes kanban create "Daily Triage: $(date +%Y-%m-%d)" --assignee wims-bfp-orchestrator --body "Review: CI status, open PRs, team commits (laqqui/orljorstin/ShibaTheShiba), GitHub issues. Post summary as comment."`

**Cron command:**
```bash
hermes cron create \
  --name "WIMS-BFP Daily Triage" \
  --schedule "0 8 * * *" \
  --repeat 0 \
  --deliver telegram \
  --prompt 'TODAY=$(date +%Y-%m-%d)
EXISTING=$(hermes kanban list --status todo --assignee wims-bfp-orchestrator 2>/dev/null | grep "$TODAY" | awk "{print \$1}")
if [ -n "$EXISTING" ]; then
  echo "Already exists: $EXISTING"
else
  hermes kanban create "Daily Triage: $TODAY" \
    --assignee wims-bfp-orchestrator \
    --body "Review: CI status, open PRs, team commits (laqqui/orljorstin/ShibaTheShiba), GitHub issues, CVE feeds. Post summary as comment."
fi
hermes kanban dispatch'
```

### Codebase Architecture Review (every 3 days, 10 PM)

**Task:** `hermes kanban create "Architecture Review: $(date +%Y-%m-%d)" --assignee wims-bfp-researcher --body "Review WIMS-BFP codebase: dead UI affordances, RLS gaps, API spec drift, unused endpoints, auth flow regressions. Report findings as comment."`

**Cron command:**
```bash
hermes cron create \
  --name "WIMS-BFP Architecture Review" \
  --schedule "0 22 */3 * *" \
  --repeat 0 \
  --deliver telegram \
  --prompt 'TODAY=$(date +%Y-%m-%d)
EXISTING=$(hermes kanban list --status todo --assignee wims-bfp-researcher 2>/dev/null | grep "Architecture Review.*$TODAY" | awk "{print \$1}")
if [ -n "$EXISTING" ]; then
  echo "Already exists: $EXISTING"
else
  hermes kanban create "Architecture Review: $TODAY" \
    --assignee wims-bfp-researcher \
    --body "Review WIMS-BFP codebase for: dead UI affordances, RLS gaps, API spec drift, unused endpoints, auth flow regressions, thesis-codebase alignment. Report findings as comment."
fi
hermes kanban dispatch'
```

---

## WIMS-BFP Orchestrator SOUL.md

```markdown
# WIMS-BFP Kanban Orchestrator

## Role

You are the strategic planner for WIMS-BFP (Wildland Urban Interface Monitoring System — Bureau of Fire Protection). You coordinate specialist workers via the Hermes Kanban board.

## Stack

- Next.js frontend + FastAPI backend
- PostgreSQL 16 + PostGIS
- Keycloak 26 (OIDC, MFA/TOTP)
- Redis + Celery async tasks
- Suricata SIEM integration
- Qwen2.5-3B SLM for AI assistance

## Team

- x1n4te: Lead Architect / DevSecOps
- laqqui: Encoder/Validator
- orljorstin: Encoder/Validator
- ShibaTheShiba: Civilian Reporter
- nathan: Analyst (GitHub handle: INB-Nathan)

## 5 Roles (Keycloak)

CIVILIAN_REPORTER, REGIONAL_ENCODER, NATIONAL_VALIDATOR, NATIONAL_ANALYST, SYSTEM_ADMIN

## Your Workflow

1. **Read board**: `hermes kanban list --status todo`
2. **Decompose**: Large goals → child tasks via `hermes kanban create`
3. **Assign**: `hermes kanban assign <child-id> <profile>`
4. **Link**: `hermes kanban link <parent-id> <child-id>`
5. **Block parent**: `hermes kanban block <parent-id>` — wait for children
6. **Monitor**: `hermes kanban list --status running`
7. **Unblock**: when children done: `hermes kanban unblock <parent-id>`
8. **Complete**: when satisfied: `hermes kanban complete <parent-id>`

## Collaboration Patterns

- **P1 Fan-out**: parallel implementation (swe + swe + swe)
- **P2 Pipeline**: decompose → implement → review → iterate → PR
- **P3 Voting**: security decision requiring multiple reviewers
- **P5 HiTL**: always gate production deployments with human block

## Security Gate

Any task touching auth, RLS, Keycloak, or PII (AES-256-GCM fields) must include a `wims-bfp-sec-audit` child task. Never complete a security-sensitive parent without `wims-bfp-sec-audit` approval.

## Repository

~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/
```

---

## Implementation Steps

### Step 1 — Create 5 worker profiles

```bash
for profile in wims-bfp-orchestrator wims-bfp-swe wims-bfp-sec-audit wims-bfp-researcher wims-bfp-analyst; do
  hermes kanban create-worker $profile
done
```

Each call creates `~/.hermes/profiles/wims-bfp-*/SOUL.md` + skills.

### Step 2 — Update SOUL.md for each profile

Replace each default `SOUL.md` with domain-specific content (examples above for orchestrator). SWE gets repo path + stack info. Sec-audit gets auth/RLS/OWASP checklist. Researcher gets wiki path + thesis structure.

### Step 3 — Create dispatcher cron (if not already)

```bash
hermes cron create \
  --name "Kanban Dispatcher" \
  --schedule "*/1 * * * *" \
  --repeat 0 \
  --deliver local \
  --prompt 'hermes kanban dispatch'
```

### Step 4 — Create P4 recurring tasks (journal tasks)

```bash
# Daily triage (already in cron — just create first task manually)
hermes kanban create "Daily Triage: $(date +%Y-%m-%d)" \
  --assignee wims-bfp-orchestrator \
  --body "Review: CI status, open PRs, team commits, GitHub issues, CVE feeds. Post summary as comment."

# Architecture review (first run)
hermes kanban create "Architecture Review: $(date +%Y-%m-%d)" \
  --assignee wims-bfp-researcher \
  --body "Review WIMS-BFP codebase for: dead UI affordances, RLS gaps, API spec drift, auth flow regressions."
```

### Step 5 — Verify integration

```bash
# List all profiles
hermes profile list | grep wims-bfp

# List all tasks
hermes kanban list

# Run a dispatch tick
hermes kanban dispatch
```

---

## What NOT to Build in PR #8

- No changes to `kanban_db.py`, `kanban.py`, `dispatch.py`
- No new CLI subcommands
- No changes to WIMS-BFP source code (`~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/`)
- No smart routing or priority queues in the dispatcher
- No P6 @mention auto-routing (future v2)

---

## Verification Checklist

```
[ ] 5 worker profiles created at ~/.hermes/profiles/wims-bfp-*/
[ ] Each SOUL.md has domain-specific instructions
[ ] Dispatcher cron job exists (hermes cron list)
[ ] Daily triage P4 task created and on board
[ ] Architecture review P4 task created and on board
[ ] hermes kanban dispatch → claims ready tasks
[ ] hermes kanban list → shows all tasks
[ ] Worker spawns: hermes -p wims-bfp-swe
[ ] Task links: parent → children DAG visible in kanban show
[ ] No changes to kanban_db.py, kanban.py, or dispatch.py
```

---

## Files Modified

| File | Change |
|------|--------|
| `~/.hermes/profiles/wims-bfp-orchestrator/SOUL.md` | Create |
| `~/.hermes/profiles/wims-bfp-swe/SOUL.md` | Create |
| `~/.hermes/profiles/wims-bfp-sec-audit/SOUL.md` | Create |
| `~/.hermes/profiles/wims-bfp-researcher/SOUL.md` | Create |
| `~/.hermes/profiles/wims-bfp-analyst/SOUL.md` | Create |
| `~/.hermes/profiles/wims-bfp-*/skills/autonomous-ai-agents/kanban-worker/SKILL.md` | Seeded by create-worker |

No core kanban files modified.

---

## Relationship to Wiki

| Wiki Page | Change |
|-----------|--------|
| `concepts/multi-agent-orchestrator-template` | Add section: "Kanban Integration (PR #8)" — how orchestrator maps to board |
| `entities/wims-bfp-agentic-workflow` | Archive or supersede with this plan |
| `concepts/wims-bfp-kanban-integration-plan` | This file (plan + execution log) |
