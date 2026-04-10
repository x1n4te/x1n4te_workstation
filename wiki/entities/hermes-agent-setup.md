---
id: hermes-agent-setup-001
type: entity
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-07-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - hermes-agent v0.8.0 release notes (2026-04-08)
status: active
tags:
  - hermes
  - setup
  - operations
  - config
related:
  - concepts/hermes-production-stack
  - entities/hermes-agent
---

# Hermes Agent — Personal Setup (x1n4te)

**Owner:** xynate (x1n4te)
**Machine:** Arch Linux, Kitty terminal
**Version:** v0.8.0 (v2026.4.8)

---

## Provider Configuration

### Orchestrator (Main Model)
- **Model:** xiaomi/mimo-v2-pro
- **Provider:** Nous Portal (free-tier)
- **Role:** Primary conversation, reasoning, tool use

### Auxiliary / Compression
- **Model:** xiaomi/mimo-v2-pro
- **Provider:** Nous Portal (free-tier)
- **Role:** Vision, summarization, compression, non-conversational tasks

**Note:** MiMo v2 Pro is officially free-tier on Nous Portal as of v0.8.0 (#6018, #5880). Pricing display enabled in model selection.

---

**Related:** [[entities/hermes-agent-v2-reference]], [[concepts/decisions-and-rationale]], [[mocs/skills]], [[concepts/environment-snapshot]]

## Gateway Configuration

### Active Gateways
| Gateway | Status | Purpose |
|---------|--------|---------|
| **Telegram** | Active | Mobile/remote access, image pipeline |
| **CLI** | Primary | Localhost, daily use |
| **Matrix** | Not configured | Considered for future image-sending from desktop |
| **Discord** | Abandoned | Multi-agent architecture attempt failed |

### Telegram Usage
- Primary gateway when outside or away from desk
- Image sending pipeline — photos get vision-analyzed and saved to [[artifacts/README|wiki/artifacts/]]
- Session continuity: use `hermes chat --resume` to pick up Telegram sessions from CLI

---

## Workspace

### Vault
- **Location:** `~/Documents/x1n4te-workstation/`
- **Type:** [[overview-state-of-field|LLM Wiki]] (Karpathy pattern)
- **Editor:** Obsidian
- **Git:** Enabled, auto-commit on agent operations

### Key Directories
| Directory | Purpose |
|-----------|---------|
| `raw/` | Immutable sources (root-owned, chattr +i) |
| `wiki/` | LLM-maintained synthesis layer |
| `wiki/artifacts/` | Image descriptions from Telegram/CLI |
| `wiki/sources/operational/` | Session logs, incident notes, debug artifacts |
| `workflows/` | Task playbooks (ingest, sweep, session-close, etc.) |
| `sessions/` | Per-session state files |
| `scripts/` | [[concepts/common-hermes-commands|token-budget.py]], wiki-sweep.py, wipe-and-recompile.py |
| `conflict-queue/` | Collision artifacts (agent never auto-resolves) |

---

## Session Protocol

**Session Open:** HERMES.md → wiki/index.md → wiki/log.md (last 20) → last session → feedback items
**Session Close:** Update session file → Decisions Made (required) → git commit → report summary
**Token Budget:** Init context capped at 50,000 tokens (HERMES.md + index + log + last session)

---

## What Was Tried and Rejected

### Multi-Agent Discord Architecture
- **Status:** Abandoned
- **Reason:** Didn't work as intended
- **What it was:** 4-agent setup using Discord channels
- **Lesson:** Stick to single-agent with Telegram + CLI

---

## Notes for Future Sessions

- Telegram is the image pipeline — when receiving images, vision-analyze and save to `wiki/artifacts/`
- Multi-agent delegation is not part of this setup
- PyNaCl/Libsodium (X25519) is deprecated in WIMS-BFP — don't reference as current
- `notify_on_complete` is available in v0.8.0 for background process notifications
