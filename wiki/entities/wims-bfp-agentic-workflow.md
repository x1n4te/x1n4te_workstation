---
id: wims-bfp-agentic-workflow-001
type: entity
created: 2026-04-07
updated: 2026-04-10
last_verified: 2026-04-10
review_after: 2026-10-10
stale_after: 2027-04-10
confidence: medium
status: archived
tags:
  - wims-bfp
  - multi-agent
  - hermes
  - archived
related:
  - entities/hermes-agent-setup
  - concepts/decisions-and-rationale
  - analyses/4-agent-pipeline-postmortem
---

# WIMS-BFP 4-Agent Delegate Architecture (ARCHIVED)

**Status:** ARCHIVED — multi-agent architecture abandoned
**Replaced by:** Single-agent with Telegram + CLI → [[entities/hermes-agent-setup]]
**See:** [[concepts/decisions-and-rationale]] and [[analyses/4-agent-pipeline-postmortem]]

---

## Overview

Four Hermes-Agent profiles — one connected to Discord (Orchestrator), three spawned as local sub-agents via `delegate_task`. All cloud API, no local GPU inference required.

## Agent Profiles

| Profile | Model | Provider | Invocation | Role |
|---|---|---|---|---|
| orchestrator | MiMo-V2-Pro | OpenRouter | Discord + local | Routes, delegates, coordinates |
| builder | MiMo-V2-Pro | OpenRouter | delegate_task | Code implementation |
| tester | Gemini Flash 2.0 | OpenRouter | delegate_task | Validation, pytest |
| critic | MiMo-V2-Pro | OpenRouter | delegate_task | Security/RLS review |

All profiles use cloud APIs — no RTX 3090 / Ollama dependency.

## Delegation Flow

```
Discord (@hermes-orchestrator)
  → Orchestrator receives task
    → delegate_task(goal="write FastAPI route + RLS policy",
                    toolsets=['terminal','file','code_execution'])
      → Builder child (MiMo-V2-Pro, isolated context, separate terminal)
        → Returns: code + output

    → delegate_task(goal="run pytest on the new code",
                    toolsets=['terminal','file','code_execution'])
      → Tester child (Gemini Flash 2.0, fast/cheap)
        → Returns: test results

    → delegate_task(goal="review RLS policy for security anti-patterns",
                    toolsets=['terminal','file'])
      → Critic child (MiMo-V2-Pro, isolated context)
        → Returns: approved / needs_fix

  → Orchestrator synthesizes → responds to Discord
```

## Cost Model

| Profile | Model | Cost per 1M tokens |
|---|---|---|
| orchestrator | MiMo-V2-Pro | $1.00 input / $3.00 output |
| builder | MiMo-V2-Pro | Same (delegation override) |
| critic | MiMo-V2-Pro | Same (delegation override) |
| tester | Gemini Flash 2.0 | $0.10 input / $0.40 output |

**Cost optimization:** Override `delegation.model` to Gemini Flash for non-critical tasks:
```bash
# In orchestrator terminal tool:
delegate_task(goal="simple test", model="google/gemini-2.0-flash")
```

## Discord Setup

**Only 1 Discord bot needed:** `hermes-orchestrator`

### Bot Settings

- Enable: **Presence Intent**, **Server Members Intent**, **Message Content Intent**
- Permissions: `274878286912`

### Recommended Server Structure

```
wims-agents/
├── 🏛-orchestrator/    # Bot responds to @hermes-orchestrator
├── 🔧-coding/          # Bot posts code outputs, diffs, etc.
└── 🛡-admin/           # x1n4te oversight
```

## Profile Configs

```
~/.hermes/profiles/
├── orchestrator/
│   ├── config.yaml    # MiMo-V2-Pro, Discord gateway, all toolsets
│   └── .env           # DISCORD_BOT_TOKEN, OPENROUTER_API_KEY
├── builder/
│   ├── config.yaml    # MiMo-V2-Pro, no memory, code toolsets
│   └── .env           # OPENROUTER_API_KEY
├── tester/
│   ├── config.yaml    # Gemini Flash 2.0, no memory, validation toolsets
│   └── .env           # OPENROUTER_API_KEY
└── critic/
    ├── config.yaml    # MiMo-V2-Pro, no memory, review toolsets
    └── .env           # OPENROUTER_API_KEY
```

## Pending Setup Checklist

- [ ] Create 1 Discord bot token (hermes-orchestrator)
- [ ] Set up Discord server + invite bot
- [ ] Fill OPENROUTER_API_KEY in all 4 profile .env files
- [ ] Fill DISCORD_BOT_TOKEN + DISCORD_ALLOWED_USERS in orchestrator .env
- [ ] Orchestrator delegation system prompt (routing rules)
- [ ] Honcho PostgreSQL memory backend (optional)
- [ ] First live test run

## Key Reference Files

- `~/Documents/x1n4te-workstation/scripts/setup-4agents.sh`
- `~/.hermes/profiles/{orchestrator,builder,tester,critic}/`
- `~/.hermes/skills/hermes-4agent-discord-setup/`
