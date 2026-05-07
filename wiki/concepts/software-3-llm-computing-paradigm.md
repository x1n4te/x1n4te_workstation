---
id: software-3-llm-computing-paradigm-001
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
  - software-dev
  - paradigm-shift
related:
  - concepts/vibe-coding-vs-agentic-engineering
  - concepts/verifiability-agentic-ai
  - concepts/agent-native-infrastructure
  - concepts/jagged-frontier-ai-capability
  - entities/andrej-karpathy
---

# Software 3.0 — LLMs as a New Computing Paradigm

## Definition

**Software 3.0** is a computing paradigm where natural language prompting replaces explicit code as the primary interface for programming computation. The LLM functions as an interpreter, and the **context window** functions as the lever (program) that directs it.

## The Three Software Eras

| Era | Programming Medium | Human Role |
|-----|-------------------|-----------|
| **Software 1.0** | Explicit code (C, Python, SQL) | Writing precise instructions |
| **Software 2.0** | Training datasets + objectives + architectures | Curating data, designing architectures |
| **Software 3.0** | Prompts + context window | Writing natural language specs |

## The Key Analogy

Software 2.0: programming by arranging datasets and training neural networks.

Software 3.0: your programming now turns to **prompting**, and **what's in the context window is your lever over the interpreter** — the LLM interprets your context and performs computation in the digital information space.

## Concrete Examples

### OpenClaw Installation (Old vs. New Paradigm)

**Old paradigm (Software 1.0):**
- A bash script that must account for every platform, OS version, dependency combination
- Scripts balloon in complexity due to platform diversity
- Human must write and maintain each conditional branch

**New paradigm (Software 3.0):**
- A single natural language instruction: "copy-paste this to your agent, it will install OpenClaw"
- The agent inspects the environment, uses tool use, debugs in the loop
- No platform-specific code required

**Key quote:** "What is the piece of text to copy-paste to your agent? That's the programming paradigm."

### Menu Genen (App That Shouldn't Exist)

**Old paradigm (Software 1.0):**
- Build an app on Vercel
- OCR the menu to extract items
- Call an image generator API for each item
- Render the menu with images
- Deploy across multiple services

**Software 3.0 paradigm:**
- Take a photo of the menu
- Give it to Gemini with the instruction: "Use Nanobanana to overlay the items onto the menu"
- Gemini outputs an image that **is** the menu with actual food photos embedded in the pixels
- No code, no API calls, no app — just a photo and a prompt

**Key quote:** "Menu Genen shouldn't exist. It's working in the old paradigm. The app shouldn't exist."

## New Opportunities That Weren't Possible Before

Software 3.0 enables things that had **no prior code path**:

- **LLM knowledge bases:** Take documents, recompile and reorder them into a new wiki structure — no code that "creates a knowledge base from facts" existed before
- **Raw image → structured output:** Feed a photo to a model, get a fully restructured version
- **Information re-framing:** Any document can be reinterpreted, reformatted, and expanded without a predetermined algorithm

**Key quote:** "Not just what existed that is faster now — new opportunities of things that couldn't be possible before."

## Implications for Software Development

1. **The unit of work shifts from code to specification.** Instead of "write me a function," the paradigm is "describe what you want and give it to an agent."
2. **Agent tool use is an "appendage"** — deterministic tasks that the neural network delegates to when needed, not the core of computation.
3. **The neural net becomes the host process; CPUs become the co-processor** — an extrapolation of the current trend where LLMs do the heavy lifting and classical computing handles tool calls.
4. **Everything still written for humans must be rewritten** — documentation, APIs, CLIs all assume human comprehension; agent-native interfaces are fundamentally different.

## Relevance to WIMS-BFP

The WIMS-BFP agentic workflow (Orchestrator + Builder + Tester + Critic) is a **Software 3.0 system**:
- The orchestrator issues natural language directives to sub-agents
- Each agent operates on context + tool use
- The human retains oversight (taste, judgment, spec ownership)
- The workflow does NOT write code in the traditional sense — it writes specs and delegates implementation

This aligns with Karpathy's observation that the best engineers in 2026 are those who know how to direct agentic workflows, not those who write code fastest.

## Key Takeaway

> "What is the piece of text to copy-paste to your agent? That's the programming paradigm."

Software 3.0 shifts the bottleneck from **writing code** to **writing good specifications** — understanding what you want remains the uniquely human contribution.

## References

- [[raw/transcripts/karpathy-software-3-llms-new-computer-2026-04]] — full transcript with timestamps
- [[entities/andrej-karpathy]] — speaker profile
- [[concepts/vibe-coding-vs-agentic-engineering]] — follow-up concept on floor vs. ceiling
