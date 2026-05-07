# Raw Transcript — How to Fix Any Codebase (Improve Codebase Architecture Deep Dive)

**Source:** https://www.youtube.com/watch?v=3MP8D-mdheA
**Speaker:** Matt Pocock
**Duration:** ~11 minutes
**Transcribed:** 2026-04-30

---

## Core Thesis

AI has accelerated software entropy — codebases fall apart faster than ever because every change that doesn't account for the entire system introduces small imperfections that snowball. The solution isn't just prevention; it's **curative**: use the `improve-codebase-architecture` skill with human strategic judgment to systematically deepen shallow modules.

---

## Key Quotes

- "AI has simply accelerated software entropy. Codebases are falling apart faster than they ever have before."
- "This skill demands a judgment call from you, the programmer, sitting above the LLM."
- "I think of agents as really, really good tactical programmers. They're able to get on the ground and make changes quickly. But they need someone on the level above them who is the strategic programmer."
- "If you have a set of really nice clear seams in your codebase, then you're going to be able to write really nice tests around those nice deep modules. And the better your tests are, the better the output from the agent is going to be."
- "What we really mean by legacy codebases are bad codebases — codebases that are hard to make changes in. And what you really need before you start making changes in a legacy codebase is a harness around the codebase."

---

## Timestamps

| Time | Topic |
|------|-------|
| 0:00 | Software entropy — AI accelerates codebases falling apart |
| 1:00 | GitHub skills repo (41.5K stars) + glossary of terminology |
| 1:43 | Modules, interfaces, implementations — core primitives |
| 2:43 | Deep modules vs. shallow modules (Ousterhout) |
| 3:40 | Seams — gaps between modules where testing happens |
| 4:14 | Adapters — concrete implementations at a seam (hexagonal architecture) |
| 4:44 | Two benefits: locality (for maintainers) + leverage (for users) |
| 5:25 | Live demo — course video manager codebase (1,500 commits) |
| 6:18 | Skill identifies 6 deepening candidates |
| 6:37 | Example: untested seam where frontend/backend implementations can go out of sync |
| 7:28 | The grilling session — human reviews proposed design decisions |
| 8:54 | Turning outputs into GitHub issues for AFK agents |
| 9:17 | Strategic vs. tactical programmer — the human sits above the agent |
| 9:58 | Recommendation: run this skill every couple of days |
| 10:25 | Legacy codebases need a harness first — tests around deep modules |

---

## Glossary of Terminology (Key Additions from This Video)

These terms form a shared vocabulary between human and AI:

- **Module** — a unit of something in your application (components, functions, a logger)
- **Interface** — everything a caller must know to use the module correctly (methods + documentation + how to call)
- **Implementation** — what the module actually does when called
- **Deep module** — hides lots of implementation behind a relatively simple interface
- **Shallow module** — complex interface, not much implementation behind it
- **Seam** — the location at which the module's interface lives; where unit/integration testing happens
- **Adapter** — a concrete module that satisfies an interface at a seam (hexagonal architecture term)

## Key Insight: Strategic vs. Tactical Programming

```
Agent (Claude Code) = Tactical Programmer
- Gets on the ground quickly
- Makes changes fast
- Needs direction

Human = Strategic Programmer  
- Sits above the agent
- Makes judgment calls
- Decides long-term health of the codebase
- Runs improve-codebase-architecture to find opportunities
- Answers the grilling session questions
- Creates GitHub issues for AFK agents
```

## Live Demo Finding

**Untested seam across frontend/backend boundary:**
- A concept had two parallel implementations (frontend + backend)
- The seam where they must agree is completely untested
- Frontend could make changes that backend wouldn't reflect, and vice versa
- Consolidation into a single module would gain **locality** (ordering rule lives in one place)

## The Legacy Codebase Protocol

1. **First:** Run `improve-codebase-architecture` to find shallow modules
2. **Then:** Build a test harness around the deep modules (you need tests BEFORE you refactor)
3. **Then:** Use the output as GitHub issues for agents to pick up

---

## Concepts Extracted

1. **[[concepts/strategic-vs-tactical-programming]]** — The human-as-strategist/agent-as-tactician framework; this is the unique new framing from this video
