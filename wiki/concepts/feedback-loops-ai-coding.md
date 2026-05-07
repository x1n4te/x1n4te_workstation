---
id: feedback-loops-ai-coding-001
type: concept
created: 2026-04-26
updated: 2026-04-26
last_verified: 2026-04-26
review_after: 2026-06-26
stale_after: 2026-10-26
confidence: high
source_refs:
  - raw/transcripts/mac-poynton-software-fundamentals-matter-more-2026.md
  - raw/transcripts/matt-pocock-ai-coding-advanced-techniques-2026.md
  - sources/operational/2026-04-26-spa-mainapplication-iterative-corruption-fix
status: active
tags:
  - software-dev
  - design
  - testing
  - ai-research
  - agents
  - foundations
related:
  - concepts/design-concept-alignment
  - concepts/ubiquitous-language-ddd
  - concepts/multi-agent-orchestrator-template
  - entities/hermes-agent
  - concepts/cognitive-overload-ai-coding
  - concepts/slopcodebench-iterative-degradation
---

# Feedback Loops in AI-Assisted Development

## Definition

A **feedback loop** in AI-assisted development is any mechanism that independently
confirms or disproves the AI's output before it accumulates. The rate of feedback
is the speed limit for safe development — exceed it and code quality degrades.

The Pragmatic Programmer (Tip 42): **"Take small steps — always. The rate of
feedback is your speed limit."**

Mac Poynton (2026): "The LLM doesn't use feedback loops very well. It does way
too much at once. It will produce huge amounts of code and then think, 'Oh, I
should probably type check that.' The rate of feedback is your speed limit."

## The Failure Mode

### How It Manifests

1. AI generates a large chunk of code (multiple files, hundreds of lines)
2. Only after generating does it think to check types, run tests, or lint
3. Errors are found — but the AI now has to reason about the entire chunk
4. Fix attempts introduce new errors (cascading failures)
5. Code quality degrades with each iteration

This is failure mode #3 from Mac Poynton: **"The AI built the right thing but
it doesn't work."**

### Why AI Agents Are Especially Bad at This

- **No frustration:** AI doesn't get tired of failing, so it iterates endlessly
  without stepping back to reconsider the approach
- **Context pollution:** Once broken code enters the context, the AI predicts
  further changes based on that flawed foundation (Jason Gorman, Codemanship)
- **Training data bias:** Most training data shows completed, working code — not
  the failing intermediate states of TDD (Emily Bache, Coding Is Like Cooking)
- **Large step preference:** AI defaults to generating as much as possible per
  token, which maximizes the distance between action and feedback

### Empirical Evidence: SlopCodeBench (2026)

From the same paper that validated failure mode #1:
- Agent code is **2.2x more verbose** than human code
- **89.8%** of trajectories show increasing verbosity
- **80%** show increasing structural erosion
- Prompt interventions ("anti-slop") shift the intercept but **do not change
  the degradation slope**
- **Cost grows 2.9x** over checkpoints without improving correctness

The degradation is inherent to the agent architecture. The only fix is
external feedback constraints.

## The Feedback Loop Stack

### Layer 1: Static Types (milliseconds)

The fastest feedback loop. TypeScript, Rust, and other typed languages catch
errors at compile time before any code runs.

**Why it matters for AI:**
- 94% of LLM-generated compilation errors are type-check failures (GitHub Blog,
  Cassidy Williams)
- TypeScript's type system + tests create a **dual feedback loop** that LLMs
  respond to extremely well (Thomas Landgraf)
- **Branded types** (e.g., `BuildingID` vs `string`) encode domain semantics
  that the LLM can reason about

**Matt Pocock (AI Hero, 2026):**
> "TypeScript is essentially free feedback for your AI. TypeScript catches errors
> the AI would never find without testing in a browser."

**Implementation:**
```json
{
  "scripts": {
    "typecheck": "tsc --noEmit"
  }
}
```

### Layer 2: Linting & Formatting (milliseconds)

Catches style violations, unused imports, potential bugs, and enforces
consistent formatting.

**Implementation:**
```json
{
  "scripts": {
    "lint": "eslint . --max-warnings 0",
    "format": "prettier --write ."
  }
}
```

### Layer 3: Unit Tests (seconds)

Catches logical errors that type checking misses. The core of TDD.

**Emily Bache (Coding Is Like Cooking, 2026):**
> "The agent writes all code. A more interesting question is whether people are
> *reading* the code the LLMs produce."

**Jason Gorman (Codemanship, 2026):**
> "An LLM is more likely to generate breaking changes than a skilled programmer,
> so frequent testing is even more essential to keep us close to working code."

### Layer 4: Integration Tests (seconds to minutes)

Verifies that modules work together correctly. Catches interface mismatches
and data flow errors.

### Layer 5: Browser / Runtime Access (seconds to minutes)

For frontend: let the AI see the running application. For backend: let the AI
make API calls and inspect responses.

**Matt Pocock:**
> "If you're building a front-end app and you're not giving the LLM access to
> the browser so it can look around, absolutely needs that."

### Layer 6: Pre-commit Hooks (enforcement)

Gate all commits through type checking + tests + linting. If any step fails,
the commit is blocked and the AI gets an error message.

**Implementation (`.husky/pre-commit`):**
```bash
npx lint-staged
npm run typecheck
npm run test
```

> "AI agents don't get frustrated by repetition. When code fails type checking
> or tests, the agent simply tries again. This makes feedback loops (and
> pre-commit hooks, especially) incredibly powerful for AI-driven development."
> — Matt Pocock, AI Hero

## TDD as the Meta-Feedback-Loop

TDD is not just a testing technique — it is the **meta-feedback-loop** that
constrains the AI to take small steps.

### The Red-Green-Refactor Cycle

```
RED:   Write a failing test (specify one behavior)
       ↓ Run test → verify it FAILS
GREEN: Write minimal code to pass
       ↓ Run test → verify it PASSES
       ↓ Run ALL tests → verify no regressions
REFACTOR: Clean up without changing behavior
       ↓ Run tests → still GREEN
REPEAT: Next behavior
```

### Why TDD Works for AI

| TDD Principle | AI Benefit |
|---------------|-----------|
| Small steps | Constrains AI to one behavior per cycle |
| Test first | Defines expected output BEFORE generation |
| Minimal code | Prevents AI from over-engineering |
| Continuous verification | Catches errors before they pollute context |
| Clean code at each step | Keeps the codebase in the LLM's effective context |

### The "Cognitive Debt" Problem

Emily Bache identifies a new risk: **cognitive debt** — when the AI writes all
the code and the human doesn't read it, the human loses the mental model of
the design. Two schools of thought:

1. **Spec-as-source:** Stop reading code; the detailed markdown spec IS the
   source code, the LLM is the compiler
2. **Quality-via-tools:** Keep reading code, but use linters, static analysis,
   and AI-generated code reviews to augment

**Risk:** Not reading code may lead to accumulating cognitive debt. TDD mitigates
this because each test describes expected behavior — even if you don't read the
implementation, you can read the tests.

## Deep Modules and Testability

John Ousterhout (*A Philosophy of Software Design*):

> "Complexity is anything related to the structure of a software system that
> makes it hard to understand and modify the system."

### Deep vs Shallow Modules

| Property | Deep Module | Shallow Module |
|----------|-----------|----------------|
| Interface | Simple, few functions | Complex, many functions |
| Implementation | Rich, hides complexity | Thin, doesn't hide much |
| Testability | Easy — test at interface | Hard — many entry points |
| AI navigation | Easy — clear boundaries | Hard — many small blobs |
| Example | Unix file I/O (5 calls) | Java I/O (many classes) |

### Why Deep Modules Matter for AI Feedback

- **Simple interfaces** = fewer test cases to write = faster feedback
- **Clear boundaries** = tests verify behavior, not implementation
- **Gray-box approach** = you can treat the module as opaque from outside,
  only verifying the interface (reduces cognitive load)

**Mac Poynton:**
> "Design the interface, delegate the implementation. You can kind of say
> 'the AI, I'll let you handle what's inside the big blob, I'm just going
> to test from the outside and verify it.'"

## The Harness Concept

Emily Bache introduces the **harness** — all the constraints you put around
the AI to guide it:

- **Type system** — the compiler catches type errors
- **Tests** — the test suite catches logic errors
- **Linters** — static analysis catches style and potential bugs
- **Pre-commit hooks** — enforce all of the above before any commit
- **Skills / markdown files** — behavioral guidelines for the AI
- **Domain language** — ubiquitous language glossary

> "The LLM is the horse; the harness ensures it pulls the cart forward correctly."

## Practical Implementation for Hermes Agent

### Current State

The `test-driven-development` skill already enforces the Red-Green-Refactor
cycle. What's missing is the **feedback loop stack** — the layers of
verification that wrap around TDD.

### Recommended Additions

1. **TypeScript/type checking** — add `typecheck` script to package.json
2. **Pre-commit hooks** — enforce typecheck + tests + lint before every commit
3. **Browser access** — for Next.js/React, give the LLM access to the dev server
4. **Pre-commit skill** — create a skill that sets up the full feedback loop stack
5. **Deep module design** — add to the `improve-codebase-architecture` workflow

### For WIMS-BFP Orchestrator

The orchestrator's execution phase should enforce feedback loops per task:
1. Specialist writes failing test
2. Specialist writes minimal code
3. Test suite runs automatically (pre-commit hook or orchestrator check)
4. Only green commits are accepted
5. Orchestrator verifies no regressions across the full suite

## Relationship to Other Concepts

|| Concept | Relationship |
|---------|-------------|
| [[concepts/design-concept-alignment]] | Alignment happens before coding; feedback loops happen during |
| [[concepts/ubiquitous-language-ddd]] | Types encode the ubiquitous language into the compiler |
| [[concepts/multi-agent-orchestrator-template]] | Orchestrator enforces feedback loops per specialist task |
| [[concepts/karpathy-loop-autoresearch]] | Karpathy Loop is TDD applied to ML experimentation |
| [[concepts/smart-zone-dumb-zone]] | Smart zone sets the token budget; feedback loops spend it efficiently |
| [[concepts/sand-castle-parallelization]] | Sand Castle parallelizes feedback loops across agents |

## Doc Rot — The Danger of Stale Documentation

Pocock raises a specific risk of markdown artifacts in the repo:

> "What I'm really scared of with any documentation decision is that we have a PRD for the gamification system. We keep it in the repo. We go on, go on, go on. A month later, we want some edits and we go in with Claude and it finds this old PRD and says, 'Yes, I found the original documentation.' Well, it turns out the actual code has changed so much from the original PRD that it's almost unrecognizable. The names have changed. The file structure has changed. Even the requirements may have changed."

**Doc rot** (Pocock's term): documentation that misleads future AI sessions by presenting an outdated view of the system.

**His resolution:** Don't keep completed PRDs in the repo. GitHub issues with a "closed" status serve the same navigational purpose without the rot risk — the closed visual indicator signals obsolescence.

**Implication for WIMS-BFP:** When the orchestrator generates a task spec (PRD equivalent), it should be ephemeral — used for that task cycle, then discarded. Do not persist it as a reference document for future tasks.

## Compacting vs Clear — Prefer Clear

Two options when approaching the smart zone limit:

| Option | Mechanism | Pocock's Verdict |
|--------|-----------|-----------------|
| **Compacting** | Compress conversation history into a summary; keep context | "Devs love it, but I hate it" |
| **Clear** | Delete session history; return to system prompt fresh | "This state is always the same. Always the same." |

**Why clear wins:**
- Compacting loses fine-grained history — the specific decisions made at each step
- Clear guarantees you return to the optimal starting state
- Optimization for clear is achievable — design the system prompt to carry all essential context
- Compacting is a crutch that delays the inevitable reset

**Practical rule:** Design the system prompt as the only persistent state. Session history is RAM — it gets cleared. If a decision matters, it lives in the system prompt (or a skill file), not in the session.

## QA With Human Taste

Automated feedback loops catch errors. But Pocock argues they do not catch **taste**:

> "There are teams out there who are trying to automate everything — automate the creation of the idea, automate the QA, automate the research, automate the prototype. And they will tend to, if you try to automate every part of this process, you end up with apps that I feel just lack taste and are bad. Maybe they just don't work or they don't even work as intended. There's just no AI. You need a human touch when you're building this stuff because without that you just end up with slop."

The QA phase is where the human:
1. Reviews the implementation for taste (not just correctness)
2. Imposes their aesthetic and architectural preferences
3. Catches things that are technically correct but semantically wrong

**QA is not a gate to pass — it is a design continuation.** The issues discovered in QA feed back into the Kanban board as new items. The loop continues.

**Implication for WIMS-BFP:** The human review gate in the orchestrator is not just about blocking bad code — it is the moment of taste imposition. Specialists produce technically-correct code; the architect shapes it with taste. Neither alone produces quality.

## Key Takeaway

> "The rate of feedback is your speed limit."
> — The Pragmatic Programmer, Tip 42

The AI will always try to go faster than its headlights allow. Your job is to
build the feedback infrastructure that forces it to slow down. Types, tests,
linters, and pre-commit hooks are not optional — they are the speed limit
signs that prevent the AI from driving off a cliff.

## References

- Hunt & Thomas, *The Pragmatic Programmer* (20th Anniversary Ed.) — Tip 42: Don't Outrun Your Headlights
- John Ousterhout, *A Philosophy of Software Design* — Deep modules, complexity definition
- Mac Poynton, "Software Fundamentals Matter More Than Ever" — failure mode #3 (YouTube, 2026)
- Emily Bache, "Test-Driven Development with Agentic AI" (Coding Is Like Cooking, 2026)
- Jason Gorman, "Why Does TDD Work So Well in AI-Assisted Programming?" (Codemanship, 2026)
- Matt Pocock, "Essential AI Coding Feedback Loops for TypeScript Projects" (AI Hero, 2026)
- Thomas Landgraf, "Why I Choose TypeScript for LLM-Based Coding" (Medium, 2026)
- Cassidy Williams, GitHub Blog — 94% of LLM compilation errors are type-check failures
- SlopCodeBench (arXiv:2603.24755) — empirical code degradation evidence
