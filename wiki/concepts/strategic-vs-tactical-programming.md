---
id: strategic-vs-tactical-programming-001
type: concept
created: 2026-04-30
updated: 2026-04-30
last_verified: 2026-04-30
review_after: 2026-07-30
stale_after: 2026-10-30
confidence: high
source_refs:
  - raw/transcripts/matt-pocock-improve-codebase-architecture-2026.md
status: active
tags:
  - software-dev
  - agents
  - ai-coding
  - architecture
  - pocock
related:
  - concepts/improve-codebase-architecture-skill
  - concepts/deep-modules-ai-navigation
  - concepts/feedback-loops-ai-coding
  - concepts/cognitive-overload-ai-coding
---

# Strategic vs. Tactical Programming

## Definition

**Strategic programming** and **tactical programming** describe two fundamentally different orientations toward software development work — one oriented toward long-term system health, the other toward immediate task completion. Matt Pocock's `improve-codebase-architecture` skill makes this distinction operational: agents execute tactical work; humans direct strategic work.

## The Core Frame

| | Tactical Programmer | Strategic Programmer |
|---|---|---|
| **Who** | AI coding agent (Claude Code, etc.) | Human programmer |
| **Orientation** | Ground-level, immediate changes | Aerial view, long-term health |
| **Speed** | Fast execution | Slow direction-setting |
| **Strength** | Making changes quickly | Deciding what changes to make |
| **Weakness** | No concept of codebase-wide consequences | Can't execute changes themselves |
| **Analogy** | Sergeant — runs around the codebase making things happen | General — decides what's worth fighting for |

> "I think of agents as really, really good tactical programmers. They're able to get on the ground and make changes quickly. But they need someone on the level above them who is the strategic programmer."

## Why the Distinction Matters Now

Before AI coding agents, the same distinction existed but humans did both. A programmer could be tactical when under pressure and strategic when they had time. The result was gradual codebase erosion — the strategic thinking never had protected time.

**With AI agents**, the split is now clean and enforceable:
- Agents can do pure tactical work — implementing features, refactoring, writing tests
- Humans can focus entirely on strategic work — architecture, prioritization, quality bar

**But this only works if the human actually performs the strategic role.** If a human treats an agent like a full-stack autonomous developer and walks away, the agent will necessarily make tactical decisions that serve immediate goals at the expense of long-term health.

## The `improve-codebase-architecture` Skill as Strategic Work

Running the `improve-codebase-architecture` skill IS the strategic work:

1. **The skill scans the codebase** — identifies shallow module candidates (tactical gap)
2. **The human reviews the candidates** — exercises judgment about which to prioritize
3. **The human participates in the grilling session** — validates proposed designs
4. **The human creates GitHub issues** — translates findings into agent-executable tasks
5. **Agents execute the issues** — pure tactical implementation

```
Strategic: run skill → review candidates → grill design → create issues
Tactical: agents execute issues → implement refactors
```

## The "Harness" Requirement for Legacy Codebases

> "A legacy codebase is probably going to have a lot of shallow modules. What you really need before you start making changes in a legacy codebase is a harness around the codebase to make sure that your changes don't mess anything up."

The harness = **tests around deep modules**. Before refactoring legacy code:

1. Run `improve-codebase-architecture`
2. Identify which modules are deep enough to test reliably
3. Write boundary tests around those modules
4. THEN start making changes with confidence

**Without this harness:** every change risks introducing regressions that won't be caught until production.

## The Feedback Loop Between Strategy and Tactics

Pocock's key insight: **better modules → better tests → better agent output**

> "If you have a set of really nice clear seams in your codebase, then you're going to be able to write really nice tests around those nice deep modules. And the better your tests are, the better the output from the agent is going to be."

This creates an upward spiral:
- Strategic investment in deep modules → enables tactical test writing
- Better tests → agents produce better code
- Better code → codebase stays structured → next cycle is easier

Without strategic investment, the spiral is downward:
- Shallow modules → hard to test
- No tests → agents degrade code freely
- Degraded code → harder to test → next cycle is worse

## Practical Implications

### For Project Leads

- You are the strategic programmer for your team
- Your job is to run architecture scans, review candidates, and create issues
- Don't write code yourself — direct the agents through well-scoped issues
- Protect time for strategic work (architecture reviews, not implementation)

### For Solo Developers

- Time-box tactical sessions (implement feature X)
- After each session: run `improve-codebase-architecture` and address top candidates
- Never let more than a few days pass without strategic architecture review
- The longer you go without deepening, the more expensive the next session

### For AI Coding Workflows

- The agent should never be making architectural decisions unsupervised
- Every refactoring should start with a strategic scan, not gut feeling
- The output of strategic work (issues) is the input to tactical work (agents)

## Connection to Other Concepts

| Concept | Relationship |
|---------|-------------|
| [[concepts/improve-codebase-architecture-skill]] | The skill IS the strategic tool — it surfaces what needs strategic attention |
| [[concepts/deep-modules-ai-navigation]] | Deep modules are the target of strategic refactoring |
| [[concepts/feedback-loops-ai-coding]] | Better modules → better tests → better feedback → better agent output |
| [[concepts/cognitive-overload-ai-coding]] | Strategic thinking is cognitively expensive; agents free humans to focus on it |

## The Human Judgment That Can't Be Outsourced

Pocock emphasizes that the skill "demands a judgment call from you, the programmer, sitting above the LLM." Specifically, the human must decide:

- Which shallow module candidate to address first
- Whether a proposed design is actually better
- What the interface should look like
- When consolidation is complete vs. when it needs more work
- What "good enough" means for the current sprint

Agents can propose, compare, and implement — but they cannot set the goal.

## Key Takeaway

> "I think of agents as really, really good tactical programmers. They're able to get on the ground and make changes quickly. But they need someone on the level above them who is the strategic programmer."

The strategic programmer is not a luxury — it's the role that prevents software entropy from winning. Run the architecture skill every few days, make the judgment calls, create the issues. Let the agents execute.

## References

- [[raw/transcripts/matt-pocock-improve-codebase-architecture-2026.md]] — full transcript with timestamps
- Matt Pocock, `improve-codebase-architecture` skill — GitHub: `mattpocock/skills`
- John Ousterhout, *A Philosophy of Software Design* — deep modules theory
- [[concepts/improve-codebase-architecture-skill]] — the skill this framing operationalizes
- [[concepts/deep-modules-ai-navigation]] — what strategic refactoring produces
