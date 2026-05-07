---
id: deep-modules-ai-navigation-001
type: concept
created: 2026-04-26
updated: 2026-04-26
last_verified: 2026-04-26
review_after: 2026-06-26
stale_after: 2026-10-26
confidence: high
source_refs:
  - raw/transcripts/mac-poynton-software-fundamentals-matter-more-2026.md
status: active
tags:
  - software-dev
  - design
  - ai-research
  - agents
  - foundations
related:
  - concepts/design-concept-alignment
  - concepts/ubiquitous-language-ddd
  - concepts/feedback-loops-ai-coding
  - concepts/multi-agent-orchestrator-template
  - entities/hermes-agent
  - concepts/cognitive-overload-ai-coding
  - concepts/slopcodebench-iterative-degradation
---

# Deep Modules & AI Codebase Navigation

## Definition

A **deep module** (John Ousterhout, *A Philosophy of Software Design*) provides
powerful functionality through a simple interface, hiding significant complexity
in its implementation. A **shallow module** has a complex interface but little
functionality, not hiding much complexity.

| Property | Deep Module | Shallow Module |
|----------|-----------|----------------|
| Interface | Simple, few entry points | Complex, many entry points |
| Implementation | Rich, hides complexity | Thin, doesn't hide much |
| Leverage | High — small interface, big behavior | Low — interface ≈ implementation |
| Testability | Easy — test at boundary | Hard — many entry points |
| AI navigation | Easy — clear boundaries | Hard — many small blobs |
| Example | Unix file I/O (5 calls) | Java I/O (many classes) |
| Example | `git` CLI (few commands, many flags) | A typical "utils" package |

## The Failure Mode

### How It Manifests with AI Coding

Mac Poynton (2026): "A codebase full of shallow modules kind of looks like a
ton of different tiny little blobs that the AI has to walk through and navigate.
This is really hard for the AI to explore. The AI doesn't understand what your
code is doing. It will attempt to explore the code, but because it's poorly
laid out, filled with shallow modules, it doesn't maybe get to the right module
in time or doesn't understand all the dependencies."

This is failure mode #4: **AI can't understand your codebase.**

### The Hill-Climbing Tax (Stoneforge, 2026)

AI coding agents waste significant context window capacity on **orientation and
search** before they can begin actual coding. This process, called **hill-climbing**,
involves numerous tool calls (grep, file reads, glob) to build sufficient context.

| Metric | Shallow Codebase | Deep Codebase |
|--------|-----------------|---------------|
| Tool calls to orient | 15-20 | 1-3 |
| Context window on navigation | 20-40% | <10% |
| Context window on reasoning | 40% | 70%+ |
| Code quality | Degraded (attention depleted) | Higher (more reasoning capacity) |

**Key insight:** The searching happens at the **start of the context window**,
when the model's reasoning is sharpest. This expensive real estate is spent on
grep results instead of coding.

Research ("Lost in the Middle") shows LLM attention degrades as context fills.
Agents that orient in 3 tool calls produce **noticeably better code** than those
that take 20, as they have more capacity for reasoning about edge cases.

### Why AI Creates Shallow Codebases

Ironically, AI is exceptionally good at creating shallow codebases:
- Generates many small files with thin wrappers
- Extracts utility functions prematurely
- Creates pass-through methods that add interface complexity
- Follows "single responsibility" too literally (one function per file)
- Each iteration adds more shallow modules (entropy)

**SlopCodeBench (2026):** Mean high-cyclomatic-complexity functions rise from
4.1 → 37.0 over iterations. The codebase becomes a web of interconnected,
shallow modules.

## The Three Causes of Complexity (Ousterhout)

### 1. Change Amplification
A simple change requires modifications in many places.
- **Shallow:** Change a data format → update 15 files
- **Deep:** Change a data format → update 1 module's implementation

### 2. Cognitive Load
A developer (or AI) must know too many things to complete a task.
- **Shallow:** To use module X, you need to understand modules A, B, C, D
- **Deep:** To use module X, you need to understand X's interface (5 minutes)

### 3. Unknown Unknowns
It's unclear what to do or if a solution will work.
- **Shallow:** "I changed this but I don't know what else breaks"
- **Deep:** "I changed the implementation; the interface contract is unchanged"

## How Deep Modules Fix AI Navigation

### The Deletion Test

Imagine deleting the module. If complexity vanishes, it was a pass-through.
If complexity reappears across N callers, it was earning its keep.

```
Shallow module: delete it → callers barely notice (it was a wrapper)
Deep module:    delete it → callers collapse (they depended on its power)
```

### The Interface Is the Test Surface

Deep modules have simple interfaces. Simple interfaces mean:
- Fewer test cases to write
- Tests verify behavior, not implementation
- Tests survive refactoring (interface is stable)
- AI can reason about the module from the interface alone

### Gray-Box Delegation

With deep modules, you can treat them as gray boxes:
- **You design the interface** (human architect)
- **AI implements the internals** (tactical programmer)
- **Tests verify the boundary** (feedback loop)
- **You don't need to read the implementation** (cognitive load reduction)

**Mac Pocock:** "Design the interface, delegate the implementation. You can
kind of say 'the AI, I'll let you handle what's inside the big blob, I'm
just going to test from the outside and verify it.'"

## The Three-Layer Documentation System

Stoneforge (2026) proposes a documentation hierarchy that complements deep
modules for AI navigation:

### Layer 1: The Index (`AGENTS.md`)
- Single file read first by the agent
- Maps common tasks to specific documentation files
- Includes repository structure, key decisions, top gotchas
- **Result:** Replaces 10+ tool calls with one

### Layer 2: Intent-Based Documentation
- Organized by task intent (Diátaxis framework: how-to, reference, explanation)
- File names act as search keywords
- Directory indexes list keywords next to links
- **Result:** Agent finds the right doc path without reading every file

### Layer 3: Right-Sized References
- Index: map only, no implementation details
- How-to: pattern with code examples, enough to execute
- Reference: full API surfaces for complex tasks
- **Result:** Agent loads only what it needs, preserving context window

### Outcome
- Orientation: 15-20 tool calls → 1-3
- Context on navigation: 20-40% → <10%
- Context on reasoning: 40% → 70%+

## Information Hiding (Ousterhout)

The principle behind deep modules:

> "Modules should encapsulate a few pieces of knowledge that represent design
> decisions. This creates change amplification or coupling because making a
> change in the design decision will force you to make changes in multiple
> modules."

**Good information hiding:**
- Unix file I/O: 5 functions hide buffer management, file system navigation,
  device drivers, caching, locking
- A database client: `query()` hides connection pooling, retry logic,
  SQL parsing, result serialization

**Bad information hiding (shallow):**
- A "utils" package: 50 functions, no coherent responsibility
- A "service" layer: thin wrappers that just call the repository layer
- A "helper" class: delegates everything to 3 other helpers

## Refactoring from Shallow to Deep

### Identify Shallow Modules

Look for these patterns:
- **Pass-through methods:** Functions that just call another function
- **Wrapper classes:** Classes that add interface complexity without functionality
- **Utils packages:** Grab-bags of unrelated functions
- **Service layers:** Thin wrappers over repositories with no business logic
- **Many small files:** Understanding requires bouncing between 10+ files

### The Consolidation Process

1. **Find clusters** of tightly-coupled shallow modules
2. **Identify the seam** — where behavior can be altered without editing in place
3. **Design a deep interface** — 1-3 entry points that hide the cluster's complexity
4. **Move implementation behind the interface** — consolidate files
5. **Test at the boundary** — replace N shallow tests with boundary tests
6. **Verify the deletion test** — delete the old modules, complexity should stay hidden

### Design Constraints for Deep Interfaces

When designing a deep module's interface:

| Constraint | Goal |
|-----------|------|
| Minimize entry points | 1-3 functions maximum |
| Hide implementation details | Caller shouldn't know about internals |
| Encapsulate design decisions | Changes to decisions don't affect callers |
| General-purpose methods | Not overly specialized |
| Eliminate pass-through | No functions that just call other functions |
| Pull complexity downward | Handle complexity in implementation, not interface |

## Relationship to Other Concepts

| Concept | Relationship |
|---------|-------------|
| [[concepts/design-concept-alignment]] | Deep modules make the design concept tangible (interface = shared understanding) |
| [[concepts/ubiquitous-language-ddd]] | Module names should be ubiquitous language terms |
| [[concepts/feedback-loops-ai-coding]] | Deep modules enable boundary testing (the best feedback loop) |
| [[concepts/multi-agent-orchestrator-template]] | Orchestrator tasks map to deep module boundaries |
| [[concepts/karpathy-loop-autoresearch]] | Karpathy Loop applies deep module thinking to ML experimentation |

## Practical Application

### For WIMS-BFP

The codebase already has some deep modules (RLS model, XAI pipeline, auth flow).
Potential shallow areas to investigate:
- Frontend: are there many small components that could be consolidated?
- API layer: are there thin wrapper functions around database calls?
- Utility packages: are there grab-bag files that should be split by domain?

### For Any AI-Assisted Project

1. **Before coding:** Design the interface first (human), delegate implementation (AI)
2. **After a coding sprint:** Run `improve-codebase-architecture` to find shallow modules
3. **When AI can't understand the codebase:** The modules are too shallow — consolidate
4. **When tests are brittle:** The modules are too shallow — test at deeper boundaries

## Key Takeaway

> "If you have a garbage codebase, the AI will produce garbage within that
> codebase."
> — Matt Pocock, 2026

Deep modules are the structural foundation that makes everything else work:
alignment (the interface IS the shared understanding), language (module names
ARE the ubiquitous language), feedback loops (boundary tests ARE the speed
limit), and AI navigation (simple interfaces ARE the map).

## References

- John Ousterhout, *A Philosophy of Software Design* (2nd Ed.) — Deep modules, information hiding, complexity
- Matt Pocock, [improve-codebase-architecture skill](https://github.com/mattpocock/skills/improve-codebase-architecture) (GitHub)
- Matt Pocock, "Your Codebase is NOT Ready for AI" (YouTube, 2026)
- Stoneforge, "Why AI Coding Agents Waste Half Their Context Window" (2026) — Hill-climbing tax, 3-layer docs
- Emily Bache, "Test-Driven Development with Agentic AI" (Coding Is Like Cooking, 2026)
- Jason Gorman, "Why Does TDD Work So Well in AI-Assisted Programming?" (Codemanship, 2026)
- Mac Poynton, "Software Fundamentals Matter More Than Ever" — failure mode #4 (YouTube, 2026)
- SlopCodeBench (arXiv:2603.24755) — AI creates shallow codebases through iteration
