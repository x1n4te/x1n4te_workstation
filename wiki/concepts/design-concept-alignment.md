---
id: design-concept-alignment-001
type: concept
created: 2026-04-26
updated: 2026-04-26
last_verified: 2026-04-26
review_after: 2026-05-26
stale_after: 2026-07-26
confidence: high
source_refs:
  - raw/transcripts/mac-poynton-software-fundamentals-matter-more-2026.md
  - raw/transcripts/matt-pocock-ai-coding-advanced-techniques-2026.md
  - raw/articles/smart-parenting-app-codebase-2026-04-12.md
status: active
tags:
  - software-dev
  - design
  - ai-research
  - agents
  - foundations
related:
  - concepts/multi-agent-orchestrator-template
  - concepts/secure-coding-practices
  - concepts/agentic-ai-soc-2026-trends
  - entities/hermes-agent
  - concepts/cognitive-overload-ai-coding
  - concepts/slopcodebench-iterative-degradation
  - concepts/smart-zone-dumb-zone
  - concepts/sand-castle-parallelization
---

# Design Concept Alignment — Why AI and Humans Diverge

## Definition

The **design concept** (Frederick P. Brooks, *The Design of Design*, 2010) is the
ephemeral, shared mental model of what is being built between collaborators.
It is not an artifact — not a PRD, not a spec, not a markdown file. It is the
invisible theory of the system that lives in the overlap of understanding between
the people (or agents) building it.

When the design concept is not shared, collaborators work from **conflicting
implicit assumptions** and the result degrades with every iteration.

## The Failure Mode

### How It Manifests with AI Coding

1. Human has a mental model of what they want
2. AI has a different interpretation (even if the spec is written)
3. AI generates code based on its interpretation
4. Human iterates on the spec, but the gap **widens** with each cycle
5. Code quality degrades — more verbose, more eroded, harder to change

This is the #1 failure mode in AI-assisted coding (Mac Poynton, "Software
Fundamentals Matter More Than Ever," 2026): **the AI didn't do what I wanted.**

### Empirical Evidence: SlopCodeBench (2026)

The SlopCodeBench paper (arXiv:2603.24755) provides rigorous empirical validation:

- **89.8%** of iterative AI coding trajectories show **increasing verbosity**
- **80%** of trajectories show **increasing structural erosion**
- Agent code is **2.2x more verbose** than maintained human repositories
- Mean high-cyclomatic-complexity functions rise from **4.1 → 37.0** over iterations
- Prompt interventions ("anti-slop") shift the intercept but **do not change the degradation slope**
- No agent solves any problem end-to-end in the benchmark

**Key finding:** Early design decisions compound. Agents that hardcode assumptions
at checkpoint 1 face cascading rewrites; those with extensible architectures
avoid slop accumulation.

### Brooks' Insight (Ch. 9, *The Design of Design*)

> "If the team does not draft a common set of explicit assumptions, each designer
> will work with a distinct set of implicit ones."

In AI-assisted development, the AI is the second "designer." Without explicit
alignment, it will generate code from its own implicit model — which diverges
from the human's model on every iteration.

### Ousterhout's Complexity Definition (*A Philosophy of Software Design*)

> "Complexity is anything related to the structure of a software system that
> makes it hard to understand and modify the system."

A bad codebase is one that's hard to change. AI performs **exceptionally well**
in good codebases and **terribly in bad ones**. This creates a compounding effect:
bad design → AI makes it worse → harder to change → AI makes it even worse.

### Software Entropy (The Pragmatic Programmer)

Every change to a codebase that only considers the change itself (not the
system design) increases entropy. The codebase gets worse and worse. The
"specs to code" approach — run the compiler again and again without design
investment — is entropy-maximizing.

## The Fix: Pre-Code Alignment

### The "Grill Me" Protocol

The primary fix is to **reach shared understanding before writing any code.**
The "Grill Me" skill (Matt Pocock, 13k+ GitHub stars) operationalizes this:

1. AI interviews the user about their plan/design
2. Questions walk the decision tree depth-first, resolving dependencies
3. AI provides recommended answers (speeds up convergence)
4. Convergence checks every 5-10 questions
5. Final design summary captures the shared understanding

**Typical session:** 40-100 questions, 30-45 minutes, produces rich context
that can be turned into a PRD or implementation plan.

### Why It Works

- Forces the human to articulate implicit assumptions
- AI asks questions the human didn't think to ask
- Dependencies between decisions are resolved before they cause conflicts
- The conversation itself becomes the "design concept" artifact
- Better than default plan mode (which is too eager to create an asset)

## The Session Phases Model

Matt Pocock (2026) describes every LLM session as cycling through four phases:

```
┌─────────────────────────────────────────────────────────┐
│ SYSTEM PROMPT (always in context — keep TINY)           │
│  ↓                                                     │
│ EXPLORATORY (agent maps the codebase)                   │
│  ↓                                                     │
│ IMPLEMENTATION (write the code)                         │
│  ↓                                                     │
│ TESTING (run feedback loops: types, tests, lint)        │
│  ↓                                                     │
│ CLEAR → back to system prompt                           │
└─────────────────────────────────────────────────────────┘
```

**Key properties:**
- System prompt should be as small as possible — 250k tokens in system prompt = straight into dumb zone without doing anything
- Clear context returns you to the system prompt (same state every time)
- Compacting compresses session history into a summary but Pocock prefers clear because: "This state is always the same. Always the same."

### Sub-Agent Token Efficiency

During the grill-me demo, Pocock invoked a sub-agent for exploration:

> "Even though the sub-agent burned a ton of tokens — 93.7k on Opus — I hadn't actually increased my token usage that much."

**Sub-agents** have isolated context windows. They can do expensive exploration work and report a summary back. The main session stays in the smart zone. This is critical for the WIMS-BFP orchestrator: use sub-agents for exploration, keep the orchestrator's context lean.

### Kent Beck's Principle

> "Invest in the design of the system every day."

The specs-to-code movement **divests** from design. The correct approach is
continuous design investment — and that starts with alignment.

## Relationship to Other Concepts

| Concept | Relationship |
|---------|-------------|
| [[concepts/multi-agent-orchestrator-template]] | Orchestrator must align specialists via explicit task specs |
| [[concepts/secure-coding-practices]] | Security decisions are design decisions — must be aligned early |
| [[concepts/agentic-soc-trends-2026]] | Agentic systems amplify the alignment problem (multiple agents) |
| [[entities/hermes-agent]] | Hermes skills encode alignment patterns (grill-me, ultraplan) |

## Practical Application

### For WIMS-BFP

The orchestrator's Phase 1 (context injection + task decomposition) is where
design concept alignment happens. The `grill-me` skill should be used before
any major feature implementation to ensure the architect and the AI agents
share the same mental model.

### For Any AI-Assisted Project

1. **Before coding:** Use grill-me or equivalent to reach shared understanding
2. **Before iterating:** Check alignment hasn't drifted (convergence checks)
3. **When code degrades:** Return to the design concept — the gap has widened
4. **For multi-agent systems:** Each specialist needs explicit assumptions, not implicit ones

## Key Takeaway

> Code is not cheap. Bad code is the most expensive it's ever been.
> AI is a tactical programmer — a sergeant on the ground. You are the
> strategic thinker. That requires software fundamentals, and it starts
> with shared understanding.

— Mac Poynton, 2026
