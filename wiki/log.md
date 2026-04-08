# Wiki Log

Append-only activity log. Newest entries first.

---

## 2026-04-08

**2026-04-08 | step-1 | Orchestrator config → Nous Portal (OAuth)**
- Changed: provider: nous, default: mimo-v2-pro
- Auth: hermes login --provider nous

**2026-04-08 | step-4 | RTX 3090 Ollama networking documented in builder .env**
- SSH tunnel: ssh -p 62473 root@1.34.114.64 -L 11434:localhost:11434
- Only builder needs tunnel (Critic uses Nous Portal, not Ollama)
- base_url already correct: http://localhost:11434/v1

**2026-04-08 | step-3 | Discord bot token wired into orchestrator .env**
- DISCORD_TOKEN_ORCHESTRATOR, DISCORD_BOT_PERMISSIONS, DISCORD_USER_ID set manually by user

**2026-04-08 | step-2 | Critic config → Nous Portal (OAuth)**
- Changed: provider: nous, default: mimo-v2-pro
- Auth: hermes login --provider nous

---

## 2026-04-07

**2026-04-07 | ingest | Hermes-Agent deep research paper → 9 wiki pages**
- Sources: wiki/sources/ai-research/hermes-agent.md
- Entity: wiki/entities/hermes-agent.md
- Concepts: wiki/concepts/closed-learning-loop.md, wiki/concepts/procedural-memory.md, wiki/concepts/delegate-task-architecture.md, wiki/concepts/model-routing.md, wiki/concepts/context-caching.md, wiki/concepts/hermes-production-stack.md
- Index: updated (total pages: 20)
- Raw: raw/ai-research/HERMES-AGENT.md

**2026-04-07 | session | 4-agent Discord architecture designed + Hermés-Agent wiki ingest | Skill saved | Pending: Discord tokens, RTX networking**
- Entity: wiki/entities/wims-bfp-agentic-workflow.md
- Script: scripts/setup-4agents.sh
- Skill: hermes-4agent-discord-setup (saved to ~/.hermes/skills/)
- Configs: ~/.hermes/profiles/{orchestrator,builder,tester,critic}/
- Modelfiles: builder + critic (Ollama GPU optimization)
- Pending: Discord bot tokens, RTX networking, API keys, Honcho PostgreSQL

**2026-04-07 | ingest | DSPy paper (2604.04869v1) + entity backfill → 7 wiki pages**
- Sources: wiki/sources/ai-research/dspy-declarative-prompt-optimization.md
- Entities: wiki/entities/dspy.md, wiki/entities/mem0.md, wiki/entities/mastras.md, wiki/entities/memgpt.md
- MOC: wiki/mocs/ai-research.md (AI Research reading path)
- Index: updated

**2026-04-07 | ingest | MemMachine paper (2604.04853v1) → 6 wiki pages created**
- Sources: wiki/sources/ai-research/memmachine.md
- Entities: wiki/entities/memmachine.md
- Concepts: wiki/concepts/episodic-vs-semantic-memory.md, wiki/concepts/agent-memory-taxonomy.md
- Analyses: wiki/analyses/memory-systems-comparison.md
- Note: MemMachine introduced as new entity in memory-systems comparison

**2026-04-07 | session | Phase 1 vault skeleton complete | 6 files created | 4 commits**
- HERMES.md written (396 lines, ~3,400 tokens)
- 5 workflow files created (ingest-source, update-concept, full-compile, wiki-sweep, session-close)
- 3 scripts created (token-budget.py, wipe-and-recompile.py, wiki-sweep.py)
- Session template created
- Git history: 6 commits on master
