---
id: hermes-agent-v2-reference-001
type: entity
created: 2026-04-10
updated: 2026-04-10
last_verified: 2026-04-10
review_after: 2026-07-10
stale_after: 2026-10-10
confidence: high
source_refs:
  - entities/hermes-agent-setup
status: active
tags:
  - hermes
  - reference
  - cli
  - configuration
  - tools
  - skills
related:
  - entities/hermes-agent-setup
  - concepts/decisions-and-rationale
  - mocs/skills
---

# Hermes Agent v0.8.0 — Full Reference

**Source:** hermes-agent skill (v2.0.0)
**Version:** v0.8.0 (v2026.4.8)
**Docs:** https://hermes-agent.nousresearch.com/docs/
**Repo:** https://github.com/NousResearch/hermes-agent

---

## What Makes Hermes Different

- **Self-improving through skills** — saves reusable procedures as SKILL.md files that load into future sessions
- **Persistent memory** — remembers user preferences, environment, lessons learned across sessions
- **Multi-platform gateway** — same agent runs on Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Email, and 8+ platforms
- **Provider-agnostic** — swap models/providers mid-workflow, credential pools rotate API keys
- **Profiles** — multiple independent instances with isolated configs, sessions, skills, memory
- **Extensible** — plugins, MCP servers, custom tools, webhooks, cron scheduling

---

## Key Paths

```
~/.hermes/config.yaml       Main configuration
~/.hermes/.env              API keys and secrets
~/.hermes/skills/           Installed skills
~/.hermes/sessions/         Session transcripts
~/.hermes/logs/             Gateway and error logs
~/.hermes/auth.json         OAuth tokens and credential pools
~/.hermes/profiles/<name>/  Per-profile isolated configs
```

---

## CLI Commands

### Core

```
hermes                          Start interactive chat (default)
hermes chat -q "question"       Single query, non-interactive
hermes setup                    Interactive setup wizard
hermes model                    Interactive model/provider picker
hermes doctor                   Check dependencies and config
hermes config                   View current config
hermes config edit              Open config.yaml in $EDITOR
hermes config set KEY VAL       Set a config value
```

### Session Management

```
hermes sessions list            List recent sessions
hermes sessions browse          Interactive picker
hermes --resume SESSION_ID      Resume by ID
hermes --continue               Resume most recent
hermes --skills SKILL           Preload skills
hermes --profile NAME           Use named profile
```

### Skills

```
hermes skills list              List installed skills
hermes skills search QUERY      Search skills hub
hermes skills install ID        Install a skill
hermes skills uninstall NAME    Remove a skill
hermes skills browse            Browse all available
```

### Gateway

```
hermes gateway start telegram   Start Telegram bot
hermes gateway stop telegram    Stop Telegram bot
hermes gateway status           Show gateway status
hermes gateway restart telegram Restart Telegram bot
hermes gateway setup            Configure platforms
```

### MCP Servers

```
hermes mcp add NAME             Add MCP server
hermes mcp remove NAME          Remove MCP server
hermes mcp list                 List configured servers
hermes mcp test NAME            Test connection
```

---

## Slash Commands (In-Session)

### Session Control
```
/new                    Fresh session
/retry                  Resend last message
/undo                   Remove last exchange
/title [name]           Name the session
/compress               Manually compress context
/stop                   Kill background processes
/background <prompt>    Run prompt in background
/queue <prompt>         Queue for next turn
/resume [name]          Resume named session
```

### Configuration
```
/model [name]           Show or change model
/reasoning [level]      Set reasoning (none|low|medium|high|xhigh)
/verbose                Cycle: off → new → all → verbose
/voice [on|off|tts]     Voice mode
/yolo                   Toggle approval bypass
/skin [name]            Change theme
```

### Tools & Skills
```
/tools                  Manage tools
/skill <name>           Load a skill into session
/cron                   Manage cron jobs
/reload-mcp             Reload MCP servers
```

### Info
```
/help                   Show commands
/usage                  Token usage
/status                 Session info
/quit                   Exit
```

---

## Config Sections

| Section | Key Options |
|---------|-------------|
| `model` | `default`, `provider`, `base_url`, `api_key`, `context_length` |
| `agent` | `max_turns` (90), `tool_use_enforcement` |
| `terminal` | `backend` (local/docker/ssh/modal), `cwd`, `timeout` (180) |
| `compression` | `enabled`, `threshold` (0.50), `target_ratio` (0.20) |
| `display` | `skin`, `tool_progress`, `show_reasoning`, `show_cost` |
| `stt` | `enabled`, `provider` (local/groq/openai) |
| `tts` | `provider` (edge/elevenlabs/openai/kokoro/fish) |
| `memory` | `memory_enabled`, `user_profile_enabled`, `provider` |
| `security` | `tirith_enabled`, `website_blocklist` |
| `delegation` | `model`, `provider`, `max_iterations` (50) |
| `checkpoints` | `enabled`, `max_snapshots` (50) |

---

## Providers (18 Supported)

| Provider | Auth | Key Env Var |
|----------|------|-------------|
| OpenRouter | API key | `OPENROUTER_API_KEY` |
| Anthropic | API key | `ANTHROPIC_API_KEY` |
| Nous Portal | OAuth | `hermes login --provider nous` |
| OpenAI Codex | OAuth | `hermes login --provider openai-codex` |
| GitHub Copilot | Token | `COPILOT_GITHUB_TOKEN` |
| DeepSeek | API key | `DEEPSEEK_API_KEY` |
| Hugging Face | Token | `HF_TOKEN` |
| Z.AI / GLM | API key | `GLM_API_KEY` |
| MiniMax | API key | `MINIMAX_API_KEY` |
| Kimi / Moonshot | API key | `KIMI_API_KEY` |
| Alibaba / DashScope | API key | `DASHSCOPE_API_KEY` |

---

## Toolsets

| Toolset | What It Does |
|---------|-------------|
| `web` | Web search and content extraction |
| `browser` | Browser automation (Browserbase, Camofox, local Chromium) |
| `terminal` | Shell commands and process management |
| `file` | File read/write/search/patch |
| `code_execution` | Sandboxed Python execution |
| `vision` | Image analysis |
| `image_gen` | AI image generation |
| `tts` | Text-to-speech |
| `skills` | Skill browsing and management |
| `memory` | Persistent cross-session memory |
| `session_search` | Search past conversations |
| `delegation` | Subagent task delegation |
| `cronjob` | Scheduled task management |
| `clarify` | Ask user clarifying questions |
| `moa` | Mixture of Agents (off by default) |

---

## Spawning Additional Hermes Instances

### One-Shot (Non-Interactive)
```
hermes chat -q 'Build a FastAPI auth service'    # foreground
hermes chat -q 'Set up CI/CD' &                   # background
```

### Interactive (PTY via tmux)
```
tmux new-session -d -s agent1 'hermes'
sleep 8
tmux send-keys -t agent1 'Build REST API' Enter
tmux capture-pane -t agent1 -p           # read output
tmux send-keys -t agent1 'Add middleware' Enter  # follow-up
tmux send-keys -t agent1 '/exit' Enter   # exit
```

### Multi-Agent Coordination
```
tmux new-session -d -s backend 'hermes -w'    # worktree mode
tmux new-session -d -s frontend 'hermes -w'
# Send tasks, capture output, relay context between them
```

### When to Use What

| Method | Best For |
|--------|----------|
| `delegate_task` | Quick parallel subtasks (minutes) |
| `hermes chat -q` | Fire-and-forget one-shots |
| tmux interactive | Long autonomous missions (hours) |
| `cronjob` tool | Scheduled recurring tasks |

---

## Voice & Transcription

### STT (Voice → Text)
| Provider | Cost | Setup |
|----------|------|-------|
| Local faster-whisper | Free | `pip install faster-whisper` |
| Groq Whisper | Free tier | Set `GROQ_API_KEY` |
| OpenAI Whisper | Paid | Set `VOICE_TOOLS_OPENAI_KEY` |

### TTS (Text → Voice)
| Provider | Cost | Setup |
|----------|------|-------|
| Edge TTS | Free (default) | None |
| ElevenLabs | Free tier | Set `ELEVENLABS_API_KEY` |
| Kokoro (local) | Free | None |
| Fish Audio | Free tier | Set `FISH_AUDIO_API_KEY` |

Voice commands: `/voice on` (voice-to-voice), `/voice tts` (always voice), `/voice off`.

---

## Agent Loop (How It Works)

```
1. Build system prompt (HERMES.md + skills + memory)
2. Loop while iterations < max_turns:
   a. Call LLM (OpenAI-format messages + tool schemas)
   b. If tool_calls → dispatch each via handle_function_call()
      → append results → continue loop
   c. If text response → return to user
3. Context compression triggers automatically near token limit
```

**Key rule:** Never break prompt caching — don't change context, tools, or system prompt mid-conversation.

---

## Related

- [[entities/hermes-agent-setup]] — Personal setup (MiMo v2 Pro, Telegram, CLI)
- [[concepts/decisions-and-rationale]] — Why this setup was chosen
- [[mocs/skills]] — Installed skills inventory
- [[concepts/skill-md-standard]] — Open standard for agent skills
- [[concepts/signs-of-ai-writing]] — Detecting AI-generated code patterns