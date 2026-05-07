---
id: verifiability-agentic-ai-001
type: concept
created: 2026-04-30
updated: 2026-04-30
last_verified: 2026-04-30
review_after: 2026-07-30
stale_after: 2026-10-30
confidence: high
source_refs:
  - raw/transcripts/karpathy-software-3-llms-new-computer-2026-04
status: active
tags:
  - agentic-ai
  - llm
  - reinforcement-learning
  - alignment
related:
  - concepts/software-3-llm-computing-paradigm
  - concepts/jagged-frontier-ai-capability
  - concepts/vibe-coding-vs-agentic-ai
  - entities/andrej-karpathy
---

# Verifiability as the Key Constraint on LLM Capability

## Definition

**Verifiability** is the property that determines whether a task can be automated by current frontier LLMs. Tasks where outputs can be objectively verified (math, code, formal proofs) are tractable for RL-trained models. Tasks without clear verification signals stagnate.

## The Core Mechanism

Frontier labs train LLMs using **giant reinforcement learning environments**:

1. A task is given a **verification reward** (e.g., "is the code correct?", "is the math answer right?")
2. The model is optimized to maximize verification reward
3. The model peaks in capability in verifiable domains, stagnates in non-verifiable ones

This is why LLMs are **jagged** — not uniformly intelligent across all tasks, but highly capable in domains that happen to be:
1. **Verifiable** — outputs can be checked programmatically
2. **Valuable in the economy** — labs deliberately included training data for them (e.g., chess data in GPT-3.5 → GPT-4 chess improvement)

## Why Models Are Jagged

Karpathy's hypothesis:

> "When you're in the circuits that were part of the RL, you fly. When you're in the circuits that are out of the data distribution, you struggle."

**Example — the car wash problem:**
- State-of-the-art Opus 4.7 can simultaneously:
  - Refactor a 100,000-line codebase
  - Find zero-day vulnerabilities
  - Correctly count letters in "strawberry"
- But tells you to **walk** to a car wash 50 meters away because... it "feels" close

This isn't a reasoning failure — it's a **verifiability gap**. Distance estimation wasn't part of the RL reward signal; code correctness is.

## Chess as a Case Study

From GPT-3.5 to GPT-4, chess improved dramatically. Many assumed this was just general capability scaling.

Karpathy's analysis: **A huge amount of chess data was deliberately added to the pre-training set.** Someone at OpenAI decided to include it → the model dramatically peaked in that domain.

This proves: **capability is partially at the mercy of what labs happen to put into the mix.** It's not purely emergent.

## Implications

### 1. What Moves Faster Than People Realize

Verifiable domains where RL environments can be constructed. The foundation technology (fine-tuning, RL) "just works" if you have diverse RL environments.

Examples that could accelerate rapidly:
- Code generation + verification loops
- Mathematical proof verification
- Formal specification matching
- Any domain with objective test suites

### 2. What's Still Slow

Non-verifiable tasks that lack objective reward signals:
- Writing with taste/aesthetics (no RL circuit for "beautiful prose")
- Novel reasoning in domains not in training data
- "Common sense" physical reasoning (walking distance)
- Cross-domain synthesis without verification feedback

### 3. The "Circuits" Metaphor

Think of an LLM as a set of overlapping circuits — some trained for specific RL tasks, others inherited from pre-training. Whether your application falls inside or outside the relevant circuits determines how well the model performs **out of the box**.

If you're outside the circuits: you need fine-tuning.

### 4. Humans Remain in the Loop for Non-Verifiable Tasks

Even in code — arguably the most verifiable domain — agents still make bizarre correlation errors:
- Agent tried to match Stripe and Google email addresses to correlate user funds
- It used email addresses as user IDs (they can be arbitrary, different emails can map to the same user)
- This is a spec/design error no RL training would catch

**Key quote:** "You have to be in charge of the spec, the plan, the top-level categories. The agents are doing the fill in the blanks."

## Verifiability + Karpathy Loop Connection

The [[concepts/karpathy-loop-autoresearch]] project is a **proof of verifiability as the lever**. ML experiment verification is highly automatable: run experiment → measure loss/accuracy → compare to baseline → record. This is exactly the kind of RL-friendly reward signal that makes autonomous experimentation tractable.

## Key Takeaway

> "You can outsource your thinking but you can't outsource your understanding."

Verifiability defines what's tractable. Understanding (knowing whether the goal is correct, whether the spec is right, whether the approach makes sense) remains the human bottleneck.

## References

- [[raw/transcripts/karpathy-software-3-llms-new-computer-2026-04]] — full transcript with timestamp
- [[entities/andrej-karpathy]] — speaker profile
- [[concepts/jagged-frontier-ai-capability]] — jaggedness as empirical evidence of the verifiability hypothesis
- [[concepts/karpathy-loop-autoresearch]] — verifiable ML experimentation as a case study
