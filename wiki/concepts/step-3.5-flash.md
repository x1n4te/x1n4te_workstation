---
id: step-3.5-flash-001
title: Step 3.5 Flash — Deep Reasoning & Agentic Coding at Scale
created: 2026-04-22
updated: 2026-04-22
type: concept
tags:
  - model
  - reasoning
  - agentic-ai
  - coding
  - moe
  - multi-token-prediction
  - hardware-efficient
sources:
  - arxiv:2602.10604
  - stepfun-blog:step-3.5-flash
  - siliconflow-blog:step-3.5-flash
  - nvidia-nim:step-3-5-flash
confidence: high
status: active
---

# Step 3.5 Flash — Deep Reasoning & Agentic Coding at Scale

**Model:** StepFun Step-3.5-Flash (open-source, 196B total parameters, 11B active per token)
**Architecture:** Sparse Mixture-of-Experts (MoE) + 3:1 Sliding Window Attention + Multi-Token Prediction (MTP-3)
**Context:** 256K tokens (cost-efficient via SWA ratio)
**Speed:** 100–300 tok/s typical, 350 tok/s peak (coding tasks)
**Strengths:** Deep reasoning, agentic coding, long-context orchestration, local deployment friendly
**Weaknesses:** No native multimodal vision (separate Step3-VL model), occasional MTP finishing bugs, Muon optimizer sensitivity
**Cost:** $0.10/M input | $0.30/M output (SiliconFlow; local free via vLLM/llama.cpp)

> **TL;DR:** Step 3.5 Flash is a **coding-orchestration specialist** that combines frontier-level reasoning (AIME 97.3%, SWE-bench 74.4%) with real-time speed. It's the best open-source model for **agentic workflows** involving code generation, tool use, and long-context synthesis. It is **NOT** a vision model — use Step3-VL for that.

## 1. Core Strengths

### 1.1 Agentic Coding & Tool Orchestration

Step 3.5 Flash shines at multi-step coding with external execution:

- **SWE-bench Verified:** 74.4%
- **Terminal-Bench 2.0:** 51.0% (best-in-class open-source)
- **LiveCodeBench-V6:** 86.4%
- **PaCoRe boost:** +2–3 points across math/coding

The model writes code, runs it in a sandbox, reads output, and iterates within a single Chain-of-Thought — it doesn't just generate, it **executes reasoning loops**.

**Ideal tasks:**
- Autonomous repository documentation generation (deep-tracing logic across thousands of LOC)
- Multi-file refactoring where changes ripple across codebase
- Data pipelines: CSV → cleaning → stats → Plotly viz → HTML report
- CLI tools with arg parsing, error handling, tests

**Real example:** Analyzed European supply chain data, integrated real-time weather APIs, calculated multi-factor risk scores, created Leaflet.js geospatial dashboard + Plotly charts, produced HTML report — all autonomous.

### 1.2 Deep Reasoning at Speed (Math/Logic)

Powered by **3-way Multi-Token Prediction (MTP-3)** — predicts 3 future tokens in parallel during generation:

- **AIME 2025:** 97.3% (99.9% with PaCoRe process reward)
- **HMMT 2025:** 96.2% (98.9% with PaCoRe)
- **IMOAnswerBench:** 85.4% (88.8% with PaCoRe)

MTP enables speculative decoding: the model predicts ahead and self-verifies, yielding both accuracy and 100–300 tok/s throughput.

**Ideal tasks:**
- Competitive math (Olympiad-grade reasoning)
- Formal logic proofs, theorem derivation
- Algorithm design with correctness guarantees
- Constraint-satisfaction puzzles (scheduling, pathfinding)

### 1.3 Long-Context Synthesis (up to 256K)

The **3:1 Sliding Window Attention (SWA)** ratio means: 3 SWA layers (local window W=512) + 1 Full Global Attention layer.

- 256K context window (enough for 50K+ words)
- Stable retrieval from document middles (no "lost-in-the-middle" collapse)
- Efficient for research synthesis, codebase auditing, multi-document Q&A

**Ideal tasks:**
- Reading entire codebase (thousands of LOC) for architectural Q&A
- Ingesting thesis (60+ .qmd chapters) → cross-referenced summaries
- Contract review across multiple drafts, highlighting discrepancies
- Academic literature review across 50+ papers with citation synthesis

### 1.4 Agentic Capabilities (Tool Use + Autonomy)

Top scores on agent benchmarks demonstrate **intent-aligned tool orchestration**:

- **τ²-Bench:** 88.2%
- **BrowseComp (w/ Context Manager):** 69.0%
- **xbench-DeepSearch:** 56.3%

The model seamlessly pivots between code execution and API protocols, bridging internal reasoning with external impact. It can:
- Call external tools (shell, HTTP, DB queries)
- Persist state across turns
- Recognize failure and retry with alternatives
- Manage context limits by summarizing intermediates

**Ideal tasks:**
- AI agent that browses, reads, synthesizes web research
- Automated incident monitoring (query DB → analyze patterns → generate report)
- Multi-tool workflows (CSV ingest → stats → plot → email)

---

## 2. Technical Architecture Deep-Dive

Understanding the **why** behind strengths helps you prompt effectively.

### 2.1 Sparse MoE (Mixture-of-Experts)

**196B total parameters, but only 11B active per token.**

Each layer has **288 routed experts + 1 shared expert**. A gating network selects top-k=8 experts per token. The rest sit idle.

**Implication:** The model can hold vast specialized knowledge (math expert, code expert, chemistry expert) without full inference cost. Naturally **multi-domain**.

**Prompt leverage:** Structure queries by domain. Mix coding + chemistry → label subtasks: `[CODE]` and `[CHEMISTRY]` — the router activates different expert subsets.

### 2.2 Multi-Token Prediction (MTP-3)

Instead of one token at a time, MTP-3 predicts **3 future tokens in parallel** via lightweight SWA+MTP heads.

**Implication:** The model "sees ahead" during generation, reducing latency through speculative decoding. It also self-verifies — if the three predictions diverge wildly, it knows it's uncertain.

**Prompt leverage:** For high-certainty tasks (code, math), **force 3-token chunk predictions**. Example: Predict next 3 tokens in `"def factorial(n):\n    if n == 0:\n        return "` — MTP heads will jointly decide `1` + newline + indentation.

### 2.3 Hybrid Attention (S³F¹ — 3:1 SWA:Full)

Three Sliding Window Attention layers (window size 512) followed by one Full Global Attention layer.

- **SWA layers:** Cheap, local only (like reading a paragraph)
- **Full layer:** Expensive, sees entire 256K (like stepping back to see the whole chapter)

**Implication:** Coarse-to-fine representation. Full layers act as global anchors preventing drift.

**Prompt leverage:** For very long inputs (>100K tokens), **place critical facts near BOTH beginning AND end** — they land in full-attention layers. Facts buried in middle retrieved via SWA with lower fidelity.

### 2.4 EP-Group Balanced Routing

Expert Parallelism with load-balancing across GPU ranks ensures no straggler experts.

**Implication:** The model **scales linearly** across GPUs. Good for distributed inference.

**Practical takeaway:** Using vLLM or SGLang? Throughput scales predictably with GPU count.

---

## 3. Prompt Engineering Best Practices

### 3.1 System Prompt Templates by Task

#### [CODE GENERATION / REFACTORING]

```
You are an expert software engineer with 15 years in production systems.
Architecture principles: KISS, YAGNI, separation of concerns, fail-fast validation.
Your code must be: type-safe, error-handled, well-commented, idiomatic.

Context: {architecture diagram or codebase overview}

Task: {specific coding task}

Requirements:
- No new dependencies unless absolutely necessary
- Preserve existing API contracts
- Add unit tests for every new function (mock external calls)
- If modifying, do not change the function signature

Output format:
1. Brief plan (2–3 sentences)
2. Code changes (exact file paths and diff-style patches)
3. Test additions/updates
```

**Why it works:** Step 3.5 Flash was trained extensively on GitHub PR data and responds well to **role priming** + **explicit constraints**. "Expert with 15 years" sets quality bar. Mentioning KISS/YAGNI activates clean-code training.

#### [DEEP RESEARCH SYNTHESIS]

```
You are a research analyst synthesizing findings from multiple sources.

Source documents (numbered):
{1. Source A...}
{2. Source B...}
...

Task: {research question}

Constraints:
- Cite sources inline as [Source N]
- Distinguish factual claims from speculation
- When sources disagree, present both viewpoints with dates/authors
- No external knowledge beyond provided sources

Output structure:
1. Executive Summary (1 paragraph)
2. Key Findings with source citations
3. Areas of Disagreement
4. Knowledge Gaps (what's not answered)
```

**Why it works:** Step 3.5 Flash excels at long-context integration. Explicit citation format prevents hallucination. "Knowledge Gaps" leverages its meta-reasoning ability.

#### [MULTI-STEP AGENTIC TASKS (TOOL USE)]

```
You are an autonomous agent with access to:
- run_python(code: str): Execute Python in sandbox
- web_search(query: str): Search web (max 5 results)
- read_file(path: str): Read filesystem
- write_file(path, content): Write files

Guidelines:
1. Think step-by-step. Before each action, explain your rationale.
2. After each tool call, verify output. If unexpected, reason about why and adjust.
3. Persist intermediate results in variables for later steps.
4. After 2 failures with same approach, pivot to alternative.

Task: {description}
```

**Why it works:** Step 3.5 Flash achieves **51.0% on Terminal-Bench 2.0** — it understands tool protocols. Explicit step-by-step reasoning + error recovery instructions yield higher autonomy success.

### 3.2 Temperature Settings by Task

| Task Type | Temperature | Rationale |
|-----------|-------------|-----------|
| Code generation | 0.0–0.2 | Deterministic output, reproducible |
| Math proof | 0.0–0.3 | Precise reasoning, minimal randomness |
| Research synthesis | 0.3–0.5 | Mild creativity in phrasing, stay factual |
| Creative writing | 0.7–0.9 | High diversity (lower fact precision) |
| Agentic exploration | 0.5–0.7 | Balance determinism + creative problem-solving |

### 3.3 Top-P and Top-K

- **Top-P (nucleus):** 0.90–0.95 recommended. Lower (0.8) for code if you want tighter selection.
- **Top-K:** 40–50 (default). Leave at default unless extreme determinism needed.

### 3.4 Context Management for >200K Tokens

Step 3.5 Flash handles 256K but performance degrades after ~200K due to SWA memory overhead.

**Two-pass strategy:**
1. Split source material into logical chunks (by file/chapter)
2. **Pass 1:** Ask Step to produce structured summary (YAML/JSON) per chunk
3. **Pass 2:** Synthesize summaries

Chunk summary prompt:

```
Summarize this file in exactly this JSON structure:
{{
  "filename": "...",
  "purpose": "...",
  "public_api": ["func1", "func2"],
  "dependencies": ["libA", "libB"],
  "key_implementation_details": ["..."]
}}
Only output valid JSON. No extra text.
```

### 3.5 Few-Shot Examples (Sparingly)

For specialized output formats (Mermaid diagrams, structured YAML), provide 1–2 examples.

**Caution:** Each example consumes context budget. Use only when zero-shot fails repeatedly.

---

## 4. Known Limitations & Mitigations

### 4.1 No Native Vision

Step 3.5 Flash is text-only. Use **Step3-VL-10B** for image understanding.

**Workaround:** Use captioning model (BLIP-2) to extract text descriptions → feed to Step 3.5 Flash.

### 4.2 MTP Finishing Indicator Bug (Nous Provider)

**Issue:** Occasionally fails to emit proper "thinking complete" token, causing **truncated outputs** on the `nous` provider (your Hermes environment).

**Symptoms:** Response stops mid-sentence or mid-code block without error.

**Mitigation:**
- Set `max_tokens` higher than expected (e.g., request 4096 even if expecting ~500)
- If truncation occurs, retry with `temperature=0.3`
- For code generation, append: "After writing the code, output 'DONE.' on a new line."

### 4.3 Context Window Quality Drop After ~200K

Despite 256K window, retrieval accuracy degrades after ~200K tokens.

**Mitigation:**
- Two-pass approach: extract entities/keyphrases first, then second-pass focused retrieval
- Or use edge-cloud collaboration pattern: Step 3.5 Flash (cloud) orchestrates Step-GUI (edge)

### 4.4 Knowledge Cutoff

Cutoff: **early 2025** (pre-June 2025 events unknown).

**Mitigation:** Pair with `web_search` tool (via API) for current events; Step will reason over fresh data within same session.

### 4.5 Muon Optimizer Sensitivity (Fine-Tuning Only)

From the paper: training used **Muon optimizer** with special handling — Polar Express iteration cast to `float16` to avoid loss spikes.

**Practical implication:** Only matters if **fine-tuning**. If loss suddenly spikes 10–100× during training:
- Cause: Muon precision instability
- Fix: **Activation clipping** inside MoE FFN layers (weight clipping ineffective)
- For inference-only users: ignore

---

## 5. Your WIMS-BFP Project Applications

### 5.1 Automated Codebase Wiki Generation

**Task:** Ingest entire WIMS-BFP repository → structured Karpathy Wiki (exactly what we just did).

**Why Step 3.5 Flash excels:**
- 256K context holds 10+ source files + schema simultaneously
- Deep reasoning understands architectural patterns (RLS policies, offline queue patterns)
- Agentic capability: writes markdown, generates directory structure, updates index.md in one pass

**Prompt structure:**
```
You are building a Karpathy-style LLM Wiki from a codebase.

Repo tree: {tree}

Read in order:
1. schema.sql — data model
2. API routes — backend endpoints
3. Frontend screens — UI flow
4. Config — environment

For each entity (table, API, screen), create wiki page:
- YAML frontmatter (title, created, updated, type, tags, sources)
- Purpose summary
- Data flow diagram (textual)
- Related wikilinks

Finally, update index.md with all pages alphabetically.
```

### 5.2 Sprint Plan Task Breakdown

Convert user stories into 2-week sprints with effort estimates, dependencies, acceptance criteria.

**Prompt:**
```
You are a Scrum Master for a 4-person thesis team.

User stories:
{feature list}

Convert each into tasks with:
- Task ID (T-001 format)
- Description (actionable, VERB-first)
- Estimated hours (Fibonacci: 1,2,3,5,8,13)
- Dependencies (task IDs)
- Acceptance criteria (Given/When/Then)

Group tasks into sprints (10 days × 6h/day × 4 people = 240 person-hours capacity).
Ensure sprint load ≤ 200 person-hours (buffer for meetings/overhead).

Output: markdown table, sprints as H2 headings.
```

### 5.3 Security Policy Review (RLS / RBAC)

```
You are a database security auditor specializing in Row-Level Security (RLS).

Schema:
{SQL CREATE TABLE statements}

Existing policies:
{SHOW RLS policies}

Check each policy for:
1. Role inclusion — does it accidentally include unauthorized roles? (e.g., national_analyst in regional policy)
2. Clause coverage — are all DML paths (INSERT/UPDATE/DELETE/SELECT) covered?
3. Restrictivity — is this the minimum necessary privilege? (Principle of least privilege)
4. Bypass vectors — can users circumvent via JOINs, CTEs, or function calls?

Output a table:
| Policy | Issue | Severity (High/Medium/Low) | Recommendation |
```

**Why it works:** Step 3.5 Flash's reasoning depth (IMO 85.4%) catches subtle logical gaps across multi-table permission flows.

---

## 6. Cost & Deployment

### Cloud Pricing (SiliconFlow — Recommended)

- **Input:** $0.10 per million tokens
- **Output:** $0.30 per million tokens

**Other providers:**
- OpenRouter: ~$0.12/M in, ~$0.35/M out (aggregator with fallbacks)
- StepFun API: $0.15/M in, $0.45/M out (direct from vendor)

### Local Inference (Free)

**Requirements:**
- Minimum: 40GB VRAM (11B active + KV cache overhead)
- Recommended: 2× H100 (80GB each) for batch inference
- Consumer option: Mac Studio M4 Max (64GB unified memory) — runs, slower

**Backends:** vLLM, SGLang, llama.cpp (GGUF quantized). Quantization: Q4_K_M causes minimal quality drop for most tasks.

### Hybrid Cost Optimization

For heavy-use (daily codebase ingestion, thesis summarization):
1. Cache common queries in vector DB (your Hindsight setup is perfect)
2. Run local for repetitive tasks (formatting, refactoring patterns)
3. Use cloud for one-off deep research (high-value, low-frequency)

---

## 7. Prompt Template Library

Store in `wiki/templates/step-3.5-flash-prompts.md`:

```
## Code Review
{paste code}
Review for: security vulnerabilities, performance issues, API misuses, project convention violations.
Output: bullet-point findings with severity + line numbers.

## Architecture Decision Record (ADR)
Problem: {description}
Options: {list alternatives}
Decision: {chosen}
Rationale: {why}
Consequences: {upsides/downsides}
Write as structured ADR in markdown.

## Test Plan
Feature: {name}
Acceptance: {criteria}
Write pytest file covering all criteria with fixtures and mocks.

## Git Commit Message
Diff:
{paste git diff}
Write conventional commit (feat/fix/docs/chore) with body explaining the why.
```

---

## 8. When NOT to Use Step 3.5 Flash

| Scenario | Better Alternative | Reason |
|----------|--------------------|--------|
| Simple factual lookup (API docs, one-liners) | Claude Sonnet 3.5 / GPT-4o-mini | Cheaper, faster, sufficient |
| Image analysis / chart reading | Step3-VL-10B or GPT-4o Vision | Native multimodal |
| Long-form creative writing (novels) | Claude Sonnet 3.5 | Better stylistic coherence |
| Real-time streaming chat (<200ms) | Phi-3, Gemma-2B | Optimized for raw speed |
| Fine-tuning on domain corpus | Dense 7–13B model | MoE fine-tuning complex; dense adapts faster |

---

## 9. Integration with Your Stack

### Claude Code / Codex

`~/.claude.json`:

```json
{
  "models": ["step-3.5-flash"],
  "stepfun-api,step-3.5-flash": {
    "use": ["OpenAI"],
    "ApiKey": "YOUR_SILICONFLOW_KEY"
  }
}
```

### Hermes Agent

`~/.hermes/config.yaml`:

```yaml
model: stepfun/step-3.5-flash
provider: openrouter  # or stepfun-api
```

Now all subagent tasks default to Step 3.5 Flash.

---

## 10. Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│ Step 3.5 Flash — Cheat Sheet                               │
├─────────────────────────────────────────────────────────────┤
│ Architecture:   Sparse MoE (196B total, 11B active)         │
│ Context:        256K (3:1 SWA:Full ratio)                   │
│ Speed:          100–300 tok/s typ, 350 tok/s peak (code)    │
│ Best at:        Coding, Math, Long-context reasoning       │
│                                            │
│ Benchmark highlights:                                       │
│   • AIME 2025:      97.3% (99.9% w/ PaCoRe)                │
│   • SWE-bench:      74.4%                                   │
│   • τ²-Bench:       88.2% (multi-tool agentic)             │
│   • LiveCodeBench:  86.4%                                   │
│                                            │
│ Pricing (cloud): $0.10/M in | $0.30/M out                   │
│ Local:           vLLM, llama.cpp, SGLang                    │
│ Multimodal?      No (use Step3-VL-10B)                       │
│ Knowledge cut:   Early 2025                                 │
├─────────────────────────────────────────────────────────────┤
│ Prompting tips:                                             │
│   • Role priming: "expert with 15 years"                   │
│   • Structure: "Output: plan, code, tests"                 │
│   • Code: temp=0.0–0.2, generous max_tokens               │
│   • Research: require inline [Source N] citations          │
│   • Long docs: chunk→summarize→synthesize                  │
├─────────────────────────────────────────────────────────────┤
│ Gotchas:                                                    │
│   • MTP finish bug (nous): truncation; retry if needed     │
│   • Muon sensitivity: fine-tuning only                      │
│   • Context degrades after ~200K tokens                     │
│   • No native vision; pair with Step3-VL if needed          │
└─────────────────────────────────────────────────────────────┘
```

---

## Related

- `[[concepts/step-3.5-flash]]` — side-by-side vs GPT-5.2, Claude Opus 4.5, DeepSeek V3.2
- `[[concepts/step-3.5-flash]]` — sparse MoE routing dynamics
- `[[concepts/step-3.5-flash]]` — vLLM/llama.cpp setup
- `**prompt engineering patterns**` — reusable system prompts
- `[[wims-bfp/automation/agentic-tasks]]` — Step 3.5 Flash applied to WIMS-BFP workflows
