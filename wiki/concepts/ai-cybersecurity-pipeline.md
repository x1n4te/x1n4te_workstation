---
id: ai-cybersecurity-pipeline-001
type: concept
created: 2026-04-12
updated: 2026-04-12
last_verified: 2026-04-12
review_after: 2026-06-12
stale_after: 2026-10-12
confidence: high
source_refs:
  - raw/articles/aisle-jagged-frontier-2026-04-12
status: active
tags:
  - cybersecurity
  - ai-research
  - agents
  - design
related:
  - entities/aisle
  - concepts/jagged-frontier-ai-capability
  - concepts/secure-coding-practices
  - concepts/slm-log-reading-pipeline
---

# AI Cybersecurity Pipeline — 5-Stage Decomposition

## Definition

AI-powered cybersecurity is NOT a single monolithic capability. It's a **modular pipeline** of 5 distinct tasks, each with vastly different scaling properties, model requirements, and difficulty levels.

This decomposition was articulated by AISLE (Stanislav Fort) in response to Anthropic's Mythos announcement, which presented AI cybersecurity as a single integrated capability.

## The 5 Stages

### Stage 1: Broad-Spectrum Scanning
- **What:** Navigate a large codebase (hundreds of thousands of files) to identify which functions are worth examining
- **Difficulty:** Medium
- **Model requirement:** Moderate — needs understanding of code structure, attack surface mapping
- **Scaling:** Highly parallelizable — cheap models can scan broadly
- **WIMS-BFP analog:** Suricata network scanning, Celery task distribution

### Stage 2: Vulnerability Detection
- **What:** Given the right code, spot what's wrong (buffer overflow, injection, logic bugs)
- **Difficulty:** Varies wildly (buffer overflow = easy, signed integer overflow = hard)
- **Model requirement:** Task-dependent — straightforward bugs need small models, subtle bugs need reasoning
- **Scaling:** Jagged — see [[concepts/jagged-frontier-ai-capability]]
- **WIMS-BFP analog:** SLM log reading for threat detection

### Stage 3: Triage and Verification
- **What:** Distinguish true positives from false positives, assess severity and exploitability
- **Difficulty:** HIGH — this is where most AI systems fail
- **Model requirement:** Needs both sensitivity (find real bugs) AND specificity (don't flag safe code)
- **Scaling:** The hardest stage to automate — most models false-positive on patched code
- **Key insight:** "A tool that flags everything as vulnerable is useless at scale. It drowns reviewers in noise."
- **WIMS-BFP analog:** NATIONAL_VALIDATOR review step, human-in-the-loop

### Stage 4: Patch Generation
- **What:** Fix the vulnerability correctly without introducing regressions
- **Difficulty:** Medium-High
- **Model requirement:** Needs understanding of code context, side effects, related code paths
- **Scaling:** Moderate — patch quality varies by model, but scaffolding helps
- **WIMS-BFP analog:** N/A (defense-focused, not patch-focused)

### Stage 5: Exploit Construction
- **What:** Build working exploits (ROP chains, heap sprays, privilege escalation)
- **Difficulty:** VERY HIGH — the genuinely creative step
- **Model requirement:** Needs creative engineering (multi-round delivery, gadget sequencing)
- **Scaling:** This is where frontier models genuinely separate from small models
- **Key insight:** Mythos's multi-round RPC delivery (15 requests, 32 bytes each) was not replicated by any small model
- **WIMS-BFP analog:** Not applicable (defensive system)

## Scaling Properties by Stage

| Stage | Difficulty | Model Needed | Parallelizable | Moat Location |
|---|---|---|---|---|
| 1. Scanning | Medium | Cheap/small | Highly | System |
| 2. Detection | Variable | Task-dependent | Yes | System |
| 3. Triage | HIGH | Needs specificity | Partially | System + expertise |
| 4. Patching | Medium-High | Moderate | Somewhat | System |
| 5. Exploitation | VERY HIGH | Frontier | No | Model |

**Critical insight:** Stages 1-3 (the defensive core) are accessible with current cheap models. Stage 5 (offensive) is where frontier models genuinely excel — but defenders don't need Stage 5 nearly as often.

## AISLE's Production Scaffold

```
Container → Prompt model to scan → Hypothesize/test → ASan crash oracle
→ Rank files by attack surface → Validate → Triage → Patch → Maintainer trust
```

This scaffold works with multiple model families. The value is in the orchestration, not the model.

## Production Function for AI Cybersecurity

Four inputs, not one:
1. **Intelligence per token** — what frontier models maximize
2. **Tokens per dollar** — what cheap models maximize
3. **Tokens per second** — throughput for broad scanning
4. **Security expertise in the scaffold** — the actual moat

Anthropic maximizes input #1. AISLE's experience shows inputs #2-4 matter just as much, sometimes more.

## Implications for System Designers

1. **Start with Stages 1-3** — these are accessible now, no Mythos needed
2. **Build model-agnostic scaffolding** — don't couple to one provider
3. **Invest in triage** — specificity matters more than sensitivity at scale
4. **Deploy cheap models broadly** — coverage > per-token intelligence
5. **Maintainer trust is the metric** — not CVE count, not benchmark scores

## WIMS-BFP Parallels

WIMS-BFP's architecture maps cleanly to this decomposition:
- **Suricata** = Stage 1 (broad network scanning)
- **Celery workers** = Stage 1 parallelization
- **Qwen 2.5-3B SLM** = Stage 2 (detection on isolated log entries)
- **NATIONAL_VALIDATOR** = Stage 3 (human triage)
- **Dashboard alerts** = Output of the pipeline

The key insight: WIMS-BFP already follows the "system > model" principle by using a cheap SLM for detection and relying on system architecture (Suricata → Celery → SLM → human review) for the defensive pipeline.

## Sources

- [[raw/articles/aisle-jagged-frontier-2026-04-12]]
- [[entities/aisle]]
- [[concepts/jagged-frontier-ai-capability]]
- [[concepts/slm-log-reading-pipeline]] — WIMS-BFP's SLM detection layer
