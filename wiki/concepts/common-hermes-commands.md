---
id: common-hermes-commands-001
type: concept
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-07-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - entities/hermes-agent-setup
  - entities/hermes-agent-v2-reference
status: active
tags:
  - hermes
  - commands
  - quick-reference
related:
  - entities/hermes-agent-setup
---

# Common Hermes Commands — Quick Reference

---

## Session Management

```bash
hermes chat                          # Start new CLI session (see [[entities/hermes-agent-setup]])
hermes chat --resume                 # Resume a previous session (interactive picker)
hermes chat --session <id>           # Resume specific session by ID
hermes /new                         # New session (inside chat)
hermes /resume                      # Resume session (inside chat)
hermes /status                      # Show current session status
```

## Gateway

```bash
hermes gateway start telegram        # Start Telegram bot
hermes gateway stop telegram         # Stop Telegram bot
hermes gateway status                # Show gateway status
hermes gateway restart telegram      # Restart Telegram bot
```

## Model & Provider

```bash
hermes /model                        # Switch model/provider (interactive)
hermes /models                       # List available models
```

## Auth

```bash
hermes auth login                    # Login to provider
hermes auth logout                   # Logout
hermes auth status                   # Check auth status
hermes auth remove                   # Remove credentials permanently
```

## Cron Jobs

```bash
hermes cron list                     # List scheduled jobs
hermes cron create                   # Create a cron job
hermes cron pause <id>               # Pause a job
hermes cron resume <id>              # Resume a job
hermes cron remove <id>              # Remove a job
```

## Skills

```bash
hermes skills list                   # See [[concepts/procedural-memory]] for skill management                   # List available skills
hermes skills install <skill>        # Install a skill
hermes skills remove <skill>         # Remove a skill
```

## System

```bash
hermes doctor                        # Diagnostics check
hermes logs                          # Tail logs from ~/.hermes/logs/
hermes update                        # Update hermes to latest
hermes /help                         # Show all commands
```

## Approval (in-chat)

```
/approve                             # Approve pending action
/deny                                # Deny pending action
/stop                                # Stop current operation
```

## Background Processes

```
terminal(background=true, notify_on_complete=true)  # Run task in background with auto-notify
process(action="list")                               # List background processes
process(action="poll", session_id="...")             # Check process status
process(action="wait", session_id="...", timeout=60) # Wait for completion
process(action="kill", session_id="...")             # Kill a process
```

---

*Last updated: 2026-04-08. Verify against `hermes /help` for latest.*
