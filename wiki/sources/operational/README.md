---
id: operational-readme-001
type: meta
created: 2026-04-08
---

# Operational Sources

Related: [[mocs/wims-bfp]], [[sources/software-dev/wims-bfp-codebase-ingestion-2026-04-08]]

This folder accumulates over time as you use hermes day to day.

## What Goes Here

- **Incident notes** — something broke, what happened, how it was fixed
- **Debug artifacts** — error logs, stack traces, config diffs
- **Provider evaluations** — testing a new model, latency notes, quality observations
- **Config snapshots** — notable config changes and why
- **Workflow observations** — what worked, what didn't, process improvements

## File Convention

```
YYYY-MM-DD-topic.md
```

Examples:
- `2026-04-08-telegram-gateway-setup.md`
- `2026-04-10-mimo-v2-pro-latency-test.md`
- `2026-04-15-session-continuity-bug.md`

## Template

```
---
id: ops-YYYY-MM-DD-topic
type: source
created: YYYY-MM-DD
confidence: high | medium | low
status: active
source_refs: []
review_after: 2026-07-08
stale_after: 2026-10-08
tags:
  - operational
---

# [What Happened]

## Context
What were you doing?

## What Happened
The actual event/finding.

## Resolution
How it was fixed or what was learned.

## Notes
Anything to remember for next time.
```

---

*50+ operational source files accumulated across sessions (2026-04-12 to 2026-04-26).*
