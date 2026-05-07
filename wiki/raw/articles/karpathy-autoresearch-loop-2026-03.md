# The Karpathy Loop: 700 Experiments in 2 Days

**Source:** https://fortune.com/2026/03/17/andrej-karpathy-loop-autonomous-ai-agents-future/
**Published:** March 17, 2026
**Author:** Jeremy Kahn (Fortune)

---

## Summary

Andrej Karpathy (founding OpenAI employee, ex-Tesla AI lead) built "autoresearch" — an autonomous AI agent system that runs ML experiments without human intervention. In one run, it executed 700 experiments in 2 days, discovering 20 training optimizations that yielded an 11% training speedup on a larger model.

## What is AutoResearch

An agentic loop for ML experimentation:
1. Agent has access to a single file (training script, ~630 lines of Python)
2. Agent has a single objective metric to optimize (loss, training speed, accuracy)
3. Agent has a fixed time limit per experiment
4. Agent proposes code change → runs experiment → evaluates metric → proposes next change
5. Repeat until time runs out

## Key Results

- Karpathy's run: 700 experiments, 2 days, 20 optimizations found, 11% training speedup
- Shopify CEO Tobias Lütke tried it: 37 experiments overnight, 19% performance gain
- "All LLM frontier labs will do this. It's the final boss battle." — Karpathy

## Karpathy's Vision

**Current state:** Single agent, single path, sequential experiments.

**Future state:** "Asynchronously massively collaborative for agents." Multiple agents exploring different optimizations in parallel. "The goal is not to emulate a single PhD student, it's to emulate a research community of them."

**General applicability:** "\*any\* metric you care about that is reasonably efficient to evaluate can be autoresearched by an agent swarm."

## The 3-Component Recipe (The Karpathy Loop)

1. **Single file** — agent can modify one file (training code)
2. **Single metric** — objectively testable, efficient to evaluate
3. **Fixed time** — each experiment has a time limit

This creates a tight feedback loop: change → measure → learn → repeat.

## Implications

- Self-improving AI systems are closer than expected
- "Recursive self-improvement" is not yet reality (agent improves OTHER models, not itself)
- But the pattern accelerates AI lab research significantly
- "It's just engineering and it's going to work" — Karpathy
- Concerns about "hard takeoff" / "intelligence explosion" are premature but the pattern is real

## GitHub

https://github.com/karpathy/autoresearch
