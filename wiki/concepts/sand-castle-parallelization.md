---
id: sand-castle-parallelization-001
type: concept
created: 2026-04-26
updated: 2026-04-26
last_verified: 2026-04-26
review_after: 2026-06-26
stale_after: 2026-10-26
confidence: high
source_refs:
  - raw/transcripts/matt-pocock-ai-coding-advanced-techniques-2026.md
status: active
tags:
  - ai-coding
  - software-dev
  - agents
  - pocock
  - parallelization
  - sand-castle
  - automation
related:
  - concepts/ralph-wiggum-software-practice
  - concepts/smart-zone-dumb-zone
  - concepts/feedback-loops-ai-coding
  - concepts/improve-codebase-architecture-skill
  - concepts/multi-agent-orchestrator-template
  - entities/hermes-agent
---

# Sand Castle — Parallelized Ralph Loop Infrastructure

## Definition

**Sand Castle** is a TypeScript library built by Matt Pocock (2026) for running Ralph Wiggum-style loops asynchronously and in parallel across multiple AI agents. It bridges the gap between single-session Ralph Wiggum (sequential steps) and multi-developer AI teams.

**GitHub:** `sandcastle` (Pocock's organization)
**Purpose:** TypeScript library for running parallelized AI coding loops AFK (away from keyboard).

## The Problem It Solves

Ralph Wiggum works well for single-threaded incremental work. But when you have:
- A backlog of 10+ issues
- Issues with blocking dependencies
- A desire to work AFK overnight

...sequential Ralph loops don't scale. Sand Castle adds:

1. **Planner agent** — reads the Kanban board, resolves blocking relationships, chooses which issues to work on in parallel
2. **Sandbox per issue** — each parallel branch runs in an isolated Docker container with its own git branch
3. **Implement agent per sandbox** — runs the Ralph loop for that issue
4. **Reviewer agent** — automated code review with coding standards pushed to it
5. **Merger agent** — handles merge conflicts when branches reunite

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│  Sand Castle Runner                                      │
│                                                          │
│  ┌──────────┐    ┌─────────┐    ┌──────────┐          │
│  │ Planner  │───▶│ Sandover │───▶│  Merger   │          │
│  │ (Opus)   │    │ Branches │    │  Agent    │          │
│  └──────────┘    └────┬────┘    └──────────┘          │
│                       │                                 │
│         ┌─────────────┼─────────────┐                 │
│         ▼             ▼             ▼                 │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│   │ Implement│  │ Implement│  │ Implement│           │
│   │ (Sonnet) │  │ (Sonnet) │  │ (Sonnet) │           │
│   │ Sandbox1 │  │ Sandbox2 │  │ Sandbox3 │           │
│   └────┬─────┘  └────┬─────┘  └────┬─────┘           │
│        │             │             │                   │
│        └─────────────┼─────────────┘                 │
│                      ▼                                 │
│               ┌──────────┐                            │
│               │ Reviewer │                            │
│               │  (Opus)  │                            │
│               └──────────┘                            │
└──────────────────────────────────────────────────────────┘
```

### Roles in Sand Castle

| Role | Model | Responsibility |
|------|-------|----------------|
| Planner | Opus | Reads Kanban, resolves blocking graph, assigns work |
| Implementer | Sonnet | Ralph loop — one small change at a time |
| Reviewer | Opus | Push coding standards, enforce quality |
| Merger | Opus | Resolve merge conflicts, finalize |

## Key Design Decisions

### Docker Sandboxes = Git Branches

Each parallel unit of work is a Docker container with a git branch inside. This means:
- Complete isolation between parallel agents
- Branch is the atomic unit of work — easy to diff, review, merge
- Git history provides natural audit trail

### AFK Operation

Sand Castle is explicitly designed for unattended overnight runs:
- The loop runs without human supervision
- Human reviews the output in the morning
- Only blocking issues are surfaced for human resolution

### Push vs Pull for Coding Standards

In the reviewer phase, **push** coding standards to the reviewer:
- The reviewer receives both the code AND the coding standards
- Reviewer checks code against standards automatically

In the implementer phase, coding standards are available via **pull**:
- The agent can reference them if it has a question
- But they are not forced into every prompt (conserves tokens)

## Relationship to WIMS-BFP Orchestrator

Sand Castle is the closest existing analog to the WIMS-BFP orchestrator design:

| Sand Castle Component | WIMS-BFP Orchestrator Equivalent |
|----------------------|----------------------------------|
| Planner agent | Orchestrator — topological sort, concurrency limits |
| Implementer (Sonnet) | Specialist agents (SEC, DB, BE, FE, OPS, DOC) |
| Reviewer (Opus) | Human review gate + code review specialist |
| Merger | Result aggregation + write conflict resolution |
| Docker sandbox | Isolated subagent session |

**Key difference:** Sand Castle is generic TypeScript; WIMS-BFP orchestrator is designed for the specific 6-role model with security-first precedence.

## The Quality Ceiling

Pocock's most important insight about Sand Castle:

> "The quality of your feedback loops influences how good your AI can code. Essentially, that is the ceiling."

This applies to both Sand Castle and the WIMS-BFP orchestrator:
- Better type checking → better AI output
- Better test coverage → better AI output
- Better code review → better AI output

## Practical Takeaways for Hermes Agent

1. **Sand Castle pattern for batch jobs** — use the parallel Ralph loop for overnight runs on large tasks
2. **Model hierarchy** — Sonnet for implementation (fast, cheap), Opus for review (slow, smart)
3. **Push/pull distinction** — coding standards pushed to reviewer, available via pull for implementer
4. **Git as the integration layer** — branches are the natural unit of parallel AI work

## Key Takeaway

Sand Castle is Ralph Wiggum with a planner, parallel sandboxes, and a merger — designed to let you work AFK. It demonstrates that the Ralph loop is the fundamental atomic operation, and parallelization is a coordination layer on top.

> "This has been my flow for quite a while now for working on most projects. It works super super well."

## References

- Matt Pocock, "Advanced AI Coding Techniques" (YouTube, 2026) — live walkthrough of Sand Castle architecture
- Sand Castle GitHub: `sandcastle` TypeScript library
- Design inspired by: Ralph Wiggum practice, Kanban-style dependency resolution
