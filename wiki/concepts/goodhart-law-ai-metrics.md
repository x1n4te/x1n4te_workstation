---
id: goodhart-law-ai-metrics-001
type: concept
created: 2026-04-18
updated: 2026-04-18
last_verified: 2026-04-18
review_after: 2026-05-18
stale_after: 2026-10-18
confidence: high
source_refs:
  - raw/transcripts/primetime-everything-is-fake-2026-04-18.md
status: active
tags:
  - ai-research
  - analysis
  - foundations
related:
  - concepts/ai-benchmark-exploitation
  - sources/ai-research/primetime-ai-benchmarks-broken
  - concepts/jagged-frontier-ai-capability
---

# Goodhart's Law in AI — When Metrics Become Targets

## Definition

**Goodhart's Law** (Charles Goodhart, 1975): "When a measure becomes a target, it ceases to be a good measure."

Originally an observation about monetary policy — once a central bank targets a specific money supply metric, financial actors restructure behavior to optimize that metric rather than the underlying economic health it was supposed to reflect.

## Manifestations in AI/ML (2025-2026)

| Original Measure | Became Target | Result |
|---|---|---|
| Benchmark scores | Model ranking | Reward hacking, test manipulation, 100% scores via trivial exploits |
| Token burn rate | Developer productivity | 281B tokens/month at Meta; money out the door for no measurable output |
| GitHub stars | Project popularity | Fake star campaigns (GStack, OpenClaw); one-interaction accounts |
| Lines of code | Developer output | Universally deprecated; trivially gameable |
| Commit count | Contribution activity | Commit squashing, empty commits, dependency bumps |
| Safety evaluations | Trust score | Anthropic chart crimes; Mythos permission escalation |

## The Campbell-Goodhart Corollary

Donald Campbell's extension: "The more any quantitative social indicator is used for social decision-making, the more subject it will be to corruption pressures and the more apt it will be to distort and corrupt the social processes it is intended to monitor."

Applied to AI:
- Benchmark scores drive funding → labs optimize for scores → benchmarks lose validity
- Safety evaluations drive trust → companies game evaluations → safety trust erodes
- Open-source metrics drive VC funding → projects inflate metrics → community trust breaks

## Structural Solutions

1. **Unverifiable metrics** — evaluate things that can't be easily gamed (real-world deployment outcomes, user satisfaction, incident reduction)
2. **Rotating benchmarks** — use held-out, never-published evaluation sets
3. **Adversarial evaluation** — red-team the evaluator, not just the model
4. **Multi-dimensional assessment** — don't collapse capability to a single number
5. **Expert judgment** — human domain experts as final arbiter, not automated scores

## Connection to WIMS-BFP

WIMS-BFP explicitly addresses Goodhart's Law in its evaluation design:
- XAI explanations evaluated by BFP domain experts (can't be gamed by model)
- Suricata IDS tested with adversarial traffic (not static benchmark packets)
- System evaluated on real incident data, not synthetic test cases

This is a **thesis differentiator** — most AI security papers cite benchmark scores; WIMS-BFP uses Goodhart-aware evaluation methodology.

## Sources

- Goodhart, C.A.E. (1975). "Problems of Monetary Management: The UK Experience"
- Campbell, D.T. (1979). "Assessing the Impact of Planned Social Change"
- [[sources/ai-research/primetime-ai-benchmarks-broken]]
- [[concepts/ai-benchmark-exploitation]]
