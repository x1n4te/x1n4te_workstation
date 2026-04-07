# WIMS-BFP 4-Agent Discord Architecture

**Created:** 2026-04-07  
**Status:** Active

---

## Overview

Four Hermes-Agent profiles connected via Discord, orchestrating WIMS-BFP development via structured agent delegation.

## Agent Profiles

| Profile | Model | Endpoint | Cost | Role |
|---|---|---|---|---|
| orchestrator | MiniMax-M2.7 | MiniMax API | ~$0.002/1K tokens | Routes, coordinates, delegates |
| builder | Qwen3.5-24B-Sushi-Coder | RTX 3090 ($0.15/hr) | $0.15/hr | Code implementation |
| tester | Gemma 4 | Ollama Cloud/OpenRouter | ~$0.001/1K tokens | Validation, pytest |
| critic | Qwen3.5-24B-Sushi-Coder | RTX 3090 (shared w/ Builder) | included above | Security/RLS review |

## Discord Setup

### Required: 4 Discord Bot Tokens

Create 4 separate Discord applications at https://discord.com/developers/applications:

1. **hermes-orchestrator** — Primary coordinator
2. **hermes-builder** — Code implementation
3. **hermes-tester** — Validation
4. **hermes-critic** — Security review

For each:
1. Create application → Bot → Add Bot
2. Copy bot token to respective `~/.hermes/profiles/<name>/.env`
3. Enable: Presence Intent, Server Members Intent, Message Content Intent

### Recommended Discord Server Structure

```
wims-agents/
├── 🏛-orchestrator/         # Bot only responds to @hermes-orchestrator mentions
├── 🔨-builder/
├── 🧪-tester/
├── 🔍-critic/
├── 📋-handoff/             # Shared channel — Builder posts → Tester reads → Critic reads
└── 🛡-admin/               # x1n4te only — direct oversight
```

**Key principle:** Bots only respond when explicitly @mentioned. This prevents loops.

## Message Flow

```
User (@orchestrator): "build RLS policy for incidents table"

orchestrator → delegate_task(goal="write FastAPI route + RLS policy for incidents table", to="builder")
    builder runs on RTX 3090
    builder → writes code to file / shared handoff doc

orchestrator → delegate_task(goal="run pytest on the new RLS policy code", to="tester")
    tester runs Gemma 4
    tester → reports: pytest pass/fail

orchestrator → delegate_task(goal="review the RLS policy for security anti-patterns", to="critic")
    critic runs on shared RTX 3090
    critic → reports: approved / needs_fix

orchestrator → summarizes to user in orchestrator channel
```

## RTX 3090 Endpoint Setup

```bash
# On the rented RTX 3090 box:
ollama run hf.co/bigatuna/Qwen3.5-27b-Sushi-Coder-RL-GGUF:Q4_K_M

# Ollama serves at http://localhost:11434/v1 by default
# Verify:
curl http://localhost:11434/v1/models

# If you want external access, bind Ollama to 0.0.0.0:
OLLAMA_HOST=0.0.0.0 ollama serve
```

## Profile Startup

```bash
# Terminal 1 — Orchestrator
hermes -p orchestrator

# Terminal 2 — Builder
hermes -p builder

# Terminal 3 — Tester
hermes -p tester

# Terminal 4 — Critic
hermes -p critic
```

## Delegation Config (Orchestrator)

```yaml
delegation:
  model: google/gemma-4-7b    # Children use Gemma (fast/cheap)
  provider: openrouter
  max_depth: 2
```

Children (Builder/Tester/Critic) are spawned via `delegate_task` with:
- Isolated context (no cross-agent memory leakage)
- Restricted toolsets
- Separate terminal session

## WIMS-BFP Specific Notes

- Critic has access to `WIMS_SECURITY_CHECKLIST` pointing to `wiki/entities/hermes-agent.md`
- All agents have WIMS-BFP workspace as `cwd`
- Orchestrator maintains cross-agent handoff state in Honcho memory (PostgreSQL)
- RLS policy changes always go through Critic before merge
