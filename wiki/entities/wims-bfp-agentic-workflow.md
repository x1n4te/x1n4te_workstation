# WIMS-BFP 4-Agent CLI Delegation Architecture

**Created:** 2026-04-07
**Updated:** 2026-04-08
**Status:** Active

---

## Overview

Four Hermes-Agent profiles with one visible on Discord (Orchestrator), three invoked silently via CLI delegation. The Orchestrator is the only gateway — Builder, Tester, and Critic are one-shot CLI sub-agents spawned by the Orchestrator's terminal tool.

## Agent Profiles

| Profile | Model | Provider | Invocation | Role |
|---|---|---|---|---|
| orchestrator | MiniMax-M2.7 | minimax | Discord + CLI | Routes, delegates, coordinates |
| builder | Qwen3.5-27B-Sushi-Coder-RL-GGUF:Q4_K_M | Ollama (RTX 3090) | CLI only | Code implementation |
| tester | Gemini Flash 2.0 | OpenRouter | CLI only | Validation, pytest |
| critic | Qwen3.5-27B-Sushi-Coder-RL-GGUF:Q4_K_M | Ollama (RTX 3090) | CLI only | Security/RLS review |

Builder and Critic share the RTX 3090 Ollama instance — **sequential use**, never concurrent.

## Discord Setup

**Only 1 Discord bot needed:** `hermes-orchestrator`

Create 1 Discord application at https://discord.com/developers/applications.

### Bot Settings

- Enable: **Presence Intent**, **Server Members Intent**, **Message Content Intent**
- Permissions integer: `274878286912` (View Channels, Send Messages, Read Message History, Attach Files, Embed Links, Send Messages in Threads, Add Reactions)

### Recommended Discord Server Structure

```
wims-agents/
├── 🏛-orchestrator/    # Bot responds to @hermes-orchestrator
├── 🔧-coding/          # Bot posts code outputs, diffs, etc.
└── 🛡-admin/           # x1n4te oversight
```

**Key principle:** Orchestrator bot responds when @mentioned. Routes internally via CLI.

## Message Flow

```
User (@hermes-orchestrator): "build RLS policy for incidents table"

orchestrator (CLI invocation):
  → hermes -p builder -q "Write FastAPI route + RLS policy for wims.incidents table"
  → builder runs Qwen3.5-27B on RTX 3090
  → builder returns: code to file

orchestrator (CLI invocation):
  → hermes -p tester -q "Run pytest on the new RLS policy code"
  → tester runs Gemini Flash 2.0
  → tester returns: pytest results

orchestrator (CLI invocation):
  → hermes -p critic -q "Review the RLS policy for security anti-patterns"
  → critic runs Qwen3.5-27B on RTX 3090
  → critic returns: approved / needs_fix

orchestrator → summarizes to Discord
```

## RTX 3090 Ollama Setup

```bash
# On the rented RTX 3090 box:

# 1. Pull the base model
ollama pull hf.co/bigatuna/Qwen3.5-27b-Sushi-Coder-RL-GGUF:Q4_K_M

# 2. Create optimized models (different Ollama model names)
cd ~/.hermes/profiles/builder
ollama create qwen3.5-27b-sushi-coder-builder -f Modelfile

cd ~/.hermes/profiles/critic
ollama create qwen3.5-27b-sushi-coder-critic -f Modelfile

# 3. Start Ollama with GPU access
export OLLAMA_NUM_GPU=999
export CUDA_VISIBLE_DEVICES=0
ollama serve

# 4. Test
curl http://localhost:11434/api/generate \
  -d '{"model":"qwen3.5-27b-sushi-coder-builder","prompt":"def hello(): pass","stream":false}'
```

## Profile Startup

```bash
# Terminal 1 — Orchestrator (with Discord gateway)
hermes -p orchestrator          # or: orchestrator gateway start

# Builder/Tester/Critic don't need to run — spawned by orchestrator via:
# hermes -p builder -q "task"
# hermes -p tester -q "task"
# hermes -p critic -q "task"
```

## Config Files

```
~/.hermes/profiles/
├── orchestrator/
│   ├── config.yaml    # MiniMax-M2.7, Discord gateway, all toolsets
│   └── .env           # DISCORD_BOT_TOKEN, MINIMAX_API_KEY, OPENROUTER_API_KEY
├── builder/
│   ├── config.yaml    # Qwen3.5-27B-Sushi-Coder, Ollama endpoint, no memory
│   └── .env           # Ollama endpoint only
├── tester/
│   ├── config.yaml    # Gemini Flash 2.0, OpenRouter, no memory
│   └── .env           # OPENROUTER_API_KEY
└── critic/
    ├── config.yaml    # Qwen3.5-27B-Sushi-Coder, Ollama endpoint, no memory
    └── .env           # Ollama endpoint only
```

## Pending Setup Checklist

- [ ] Create 1 Discord bot token (hermes-orchestrator)
- [ ] Set up Discord server + invite bot
- [ ] SSH to RTX 3090 → ollama pull + create both models
- [ ] Confirm Ollama networking (SSH tunnel or OLLAMA_HOST=0.0.0.0)
- [ ] Fill API keys: MINIMAX_API_KEY, OPENROUTER_API_KEY
- [ ] Fill DISCORD_BOT_TOKEN + DISCORD_ALLOWED_USERS
- [ ] Orchestrator delegation system prompt
- [ ] First live test run

## Key Reference Files

- `~/Documents/x1n4te-workstation/scripts/setup-4agents.sh`
- `~/.hermes/profiles/{orchestrator,builder,tester,critic}/`
- `~/.hermes/skills/hermes-4agent-discord-setup/`
