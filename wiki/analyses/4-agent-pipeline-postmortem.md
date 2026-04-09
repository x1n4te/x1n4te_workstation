---
id: 4-agent-pipeline-postmortem-001
type: analysis
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-10-08
stale_after: 2027-04-08
confidence: high
source_refs:
  - sessions/2026-04-08.md
  - raw/ai-research/HERMES-AGENT.md
status: archived
tags:
  - hermes-agent
  - multi-agent
  - postmortem
  - wims-bfp
  - lessons-learned
  - archived
related:
  - entities/hermes-agent-setup
  - concepts/decisions-and-rationale
  - concepts/delegate-task-architecture
---

# 4-Agent Pipeline: Lessons Learned (Archived)

**Date:** 2026-04-08
**Status:** ARCHIVED — multi-agent architecture abandoned
**Replaced by:** Single-agent with Telegram + CLI → [[entities/hermes-agent-setup]]
**Decision rationale:** [[concepts/decisions-and-rationale]]

---

> **This document is preserved as a lessons-learned artifact.** The multi-agent Discord architecture was attempted and failed. The failure analysis below is retained for future reference if multi-agent is ever reconsidered.

**Key lesson:** Single-agent with good tools beats multi-agent with coordination overhead.

---

## What Was Planned

---

## What Was Planned

A 4-agent Discord-based pipeline for WIMS-BFP development:

```
Discord (@orchestrator)
  → delegate_task → Builder (Qwen3.5-27B-Sushi-Coder, RTX 3090 Ollama)
  → delegate_task → Tester (DeepSeek V3.2, Ollama Cloud free)
  → delegate_task → Critic (MiMo-V2-Pro, Nous Portal)
  → Orchestrator synthesizes → responds to Discord
```

**1 Discord bot. 3 delegate_task children. Hybrid cloud + local GPU.**

---

## Model Assignments (Finalized, Never Tested)

| Role | Model | Provider | Status |
|---|---|---|---|
| Orchestrator | MiMo-V2-Pro | Nous Portal (OAuth) | ✅ Config verified |
| Builder | Qwen3.5-27B-Sushi-Coder-RL-GGUF:Q4_K_M | RTX 3090 Ollama | ❌ Never served |
| Tester | DeepSeek V3.2 | Ollama Cloud (free) | ✅ Config ready |
| Critic | MiMo-V2-Pro | Nous Portal (OAuth) | ✅ Config verified |

---

## What Was Completed

1. Profile configs created (orchestrator, builder, tester, critic)
2. Discord bot created + token wired
3. Orchestrator running on Discord (gateway confirmed)
4. Modelfiles designed with `{{ .Tools }}` template for Hermes tool-calling
5. SSH tunnel strategy defined for RTX 3090 Ollama access

---

## What Failed (Root Causes)

### 1. RTX 3090 Ollama Never Served Models

The Builder depends on Ollama running on the remote RTX 3090 with the Sushi-Coder model loaded. This never happened:
- SSH tunnel was defined but never established
- `ollama pull` + `ollama create` steps were documented but not executed
- No verification that Ollama was serving on port 11434

**Impact:** Builder agent completely non-functional. 50% of the pipeline dead on arrival.

### 2. Discord Inter-Bot Communication Is Impossible

Original design had 4 separate Discord bots (one per agent). Discovery: **bots cannot @mention other bots in Discord.** This killed the 4-bot architecture and forced the pivot to 1 bot + delegate_task.

**Impact:** Architecture redesign required. Added complexity to orchestrator's delegation logic.

### 3. Sushi-Coder Training Data Mismatch

Qwen3.5-27B-Sushi-Coder was trained on Codeforces competitive programming (`open-r1/codeforces-cots`), not production code patterns. Strengths: algorithmic problem solving. Weaknesses: FastAPI, SQLAlchemy, RLS policies, security audit patterns.

**Impact:** Even if the model was served, Builder output quality for WIMS-BFP-specific patterns (RLS, Celery RLS context, Keycloak JWT) would be poor. Critic (MiMo-V2-Pro) was intended to compensate, but untested.

### 4. Nous Portal OAuth Scope Uncertainty

MiMo-V2-Pro via Nous Portal uses OAuth (`hermes login --provider nous`). Token stored in `~/.hermes/auth.json` and shared across profiles. Behavior under concurrent multi-profile access (orchestrator + critic simultaneously) was never tested.

**Impact:** Unknown. Could cause auth conflicts if both profiles hit Nous Portal simultaneously.

### 5. No Integration Test Executed

The pipeline was designed top-down but never tested bottom-up:
- No individual profile smoke test (can each profile talk to its model?)
- No delegate_task dry run (can orchestrator spawn a child?)
- No end-to-end test (Discord → orchestrator → child → response)

**Impact:** Unknown unknowns. Every integration boundary is unverified.

---

## Implementation Steps (All 🔴)

| Step | Task | Status |
|---|---|---|
| 1 | Fix Orchestrator config → Nous Portal provider | 🔴 |
| 2 | Fix Critic config → Nous Portal provider | 🔴 |
| 3 | Create 1 Discord bot (hermes-orchestrator) + invite | ✅ Done |
| 4 | Confirm RTX 3090 Ollama networking | 🔴 |
| 5 | Create orchestrator delegation system prompt | 🔴 |
| 6 | First live test run (4 agents) | 🔴 |
| 7 | Set up Honcho PostgreSQL for cross-agent memory | 🔴 |

---

## Lessons Learned

### Architecture Insights

1. **Discord is a control plane, not a data plane.** Good for human-in-the-loop oversight, bad for agent-to-agent high-frequency communication. delegate_task is the correct inter-agent mechanism.

2. **Bottom-up verification is mandatory.** Test each model endpoint individually before wiring them into a pipeline. The pipeline is only as strong as its weakest integration point.

3. **Model selection matters more than model size.** A 27B model trained on competitive programming is worse than a 7B model trained on production code for WIMS-BFP tasks. Training data domain match > parameter count.

4. **SSH tunnels are fragile infrastructure.** A development pipeline that depends on a persistent SSH tunnel to a rented GPU is inherently brittle. Consider: self-hosted Ollama, Modal/Daytona serverless, or cloud-native inference APIs.

5. **Hermes profiles share auth state.** `~/.hermes/auth.json` is shared across profiles. This is a feature (single OAuth flow) but a risk (concurrent access contention).

### Process Insights

1. **Skill documentation != working system.** The `hermes-4agent-discord-setup` skill is comprehensive (14KB of setup docs) but the system was never operational. Documentation quality doesn't predict execution quality.

2. **Session planning without execution tracking.** The implementation steps were defined but never tracked in a task manager. No automated checks for "is step N complete?"

---

## Recommended Next Steps (If Resuming)

1. **Bottom-up smoke tests:**
   - Verify orchestrator can call MiMo-V2-Pro (single prompt)
   - Verify SSH tunnel to RTX 3090 works
   - Verify Ollama serves Sushi-Coder on RTX 3090
   - Verify builder profile can talk to Ollama through tunnel
   - Verify delegate_task can spawn a child agent

2. **Replace Sushi-Coder with production-focused model:**
   - Option A: `qwen3-coder` on Ollama Cloud (free, production-trained)
   - Option B: `deepseek-v3.2` for Builder too (strong reasoning + code)
   - Option C: Carnice-27b-GGUF (if vLLM serves it, but that's a separate infra)

3. **Eliminate SSH tunnel dependency:**
   - Run Ollama on Vast.ai with `--host 0.0.0.0`
   - Or use Ollama Cloud API directly (no local tunnel needed)

4. **Automate pipeline verification:**
   - Script: `scripts/smoke-test-4agents.sh`
   - Tests each model endpoint, each profile, delegate_task spawn

---

## Related

- [[entities/hermes-agent]] — Framework entity
- [[concepts/delegate-task-architecture]] — Child agent spawning mechanism
- [[concepts/hermes-production-stack]] — Infrastructure stack (never deployed)
- Skill: `hermes-4agent-discord-setup` — Full setup documentation (comprehensive but untested)
