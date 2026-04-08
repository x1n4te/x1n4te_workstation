---
id: hermes-skills-inventory-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - ~/.hermes/skills/
status: active
tags:
  - hermes-agent
  - skills
  - procedural-memory
  - inventory
related:
  - entities/hermes-agent
  - concepts/procedural-memory
---

# Hermes Skills Inventory

**Location:** `~/.hermes/skills/`
**Last audited:** 2026-04-08
**Total skill directories:** 23
**Total individual skills:** ~80+

---

## WIMS-BFP Core (6 dirs, 9 skills)

User-created skills specific to WIMS-BFP development.

| Category | Skill | Purpose |
|---|---|---|
| devops/ | specter-audit-remediation | Apply Specter security audit patches to WIMS-BFP |
| devops/ | wims-bfp-security-review | Security review checklist — FRS roles, RLS, JWT, DMZ |
| devops/ | wims-bfp-two-agent-refactor | Critic+Builder workflow for WIMS-BFP refactoring |
| devops/ | webhook-subscriptions | Event-driven agent activation via webhooks |
| root | phase-1-crit-fixes | Fix CRIT-01 through CRIT-05 (duplicate router, Redis URL, model drift, Keycloak, missing RLS) |
| root | rls-null-bypass-fix | PostgreSQL RLS NULL-in-IN coercion bypass |
| root | nextjs-ts-strict-fixes | Next.js TypeScript strict-mode build failures |
| root | wims-bfp-codebase-audit | Reusable codebase audit — SQL schema, RLS, API routes, Celery, role enforcement |
| root | hermes-4agent-discord-setup | 4-agent pipeline docs (FAILED — see postmortem) |

---

## Agent Infrastructure (3 dirs, 13 skills)

Core agent orchestration and development workflow.

| Category | Skill | Purpose |
|---|---|---|
| autonomous-ai-agents/ | claude-code | Delegate tasks to Claude Code CLI |
| autonomous-ai-agents/ | codex | Delegate tasks to OpenAI Codex CLI |
| autonomous-ai-agents/ | opencode | Delegate tasks to OpenCode CLI |
| autonomous-ai-agents/ | hermes-agent | Full guide to using/extending Hermes Agent |
| software-development/ | code-review | Code review with security/quality focus |
| software-development/ | requesting-code-review | Pre-commit verification pipeline |
| software-development/ | plan | Plan mode — inspect context, write markdown plans |
| software-development/ | writing-plans | Multi-step implementation plans |
| software-development/ | test-driven-development | RED-GREEN-REFACTOR cycle |
| software-development/ | tdd-triple-agent | 3-agent TDD (critic+builder+tester) |
| software-development/ | subagent-driven-development | Parallel delegate_task execution |
| software-development/ | systematic-debugging | 4-phase root cause investigation |
| llm-wiki/ | llm-wiki-ingest-pdf | Ingest PDFs into LLM Wiki |
| llm-wiki/ | llm-wiki-ingest-blog | Ingest blog posts into LLM Wiki |
| llm-wiki/ | llm-wiki-ingest-github | Ingest GitHub repos into LLM Wiki |
| llm-wiki/ | llm-wiki-ingest-cve | Ingest CVE records into LLM Wiki |

---

## ML/AI (2 dirs, 29 skills)

Model training, inference, evaluation, and research tools.

### mlops/ (25 skills)

**Inference (6):**
| Skill | Purpose |
|---|---|
| inference/vllm | Serve LLMs with PagedAttention, continuous batching |
| inference/gguf | GGUF quantization via llama.cpp |
| inference/llama-cpp | CPU/Apple Silicon/consumer GPU inference |
| inference/outlines | Guarantee valid JSON/XML/code structure |
| inference/guidance | Control output with regex/grammars |
| inference/obliteratus | Remove refusal behaviors from LLMs |

**Training (6):**
| Skill | Purpose |
|---|---|
| training/unsloth | Fast fine-tuning (2-5x speed, 50-80% less memory) |
| training/axolotl | Fine-tuning with YAML configs, 100+ models |
| training/peft | LoRA, QLoRA, 25+ parameter-efficient methods |
| training/trl-fine-tuning | RL fine-tuning — SFT, DPO, PPO, GRPO |
| training/grpo-rl-training | GRPO reasoning training |
| training/pytorch-fsdp | Fully Sharded Data Parallel training |

**Models (5):**
| Skill | Purpose |
|---|---|
| models/whisper | Speech recognition (99 languages) |
| models/clip | Vision-language (zero-shot classification) |
| models/audiocraft | Audio generation (MusicGen, AudioGen) |
| models/stable-diffusion | Text-to-image generation |
| models/segment-anything | Zero-shot image segmentation |

**Cloud/Eval/Research (8):**
| Skill | Purpose |
|---|---|
| cloud/modal | Serverless GPU platform |
| vastai-vllm-multi-gpu | Deploy vLLM on Vast.ai (single/multi-GPU) |
| huggingface-hub | HF CLI — search, download, upload models |
| evaluation/lm-evaluation-harness | 60+ academic benchmarks |
| evaluation/weights-and-biases | Experiment tracking |
| research/dspy | Declarative AI programming |

### research/ (4 skills)
| Skill | Purpose |
|---|---|
| arxiv | Search/retrieve academic papers |
| blogwatcher | Monitor RSS/Atom feeds |
| llm-wiki | Karpathy's LLM Wiki pattern |
| ml-paper-writing | Publication-ready ML papers |
| research-paper-writing | End-to-end paper pipeline |
| polymarket | Prediction market data |

---

## GitHub (1 dir, 6 skills)

CI/CD and repository management.

| Skill | Purpose |
|---|---|
| github-auth | Set up git/gh authentication |
| github-issues | Create, manage, triage issues |
| github-pr-workflow | Full PR lifecycle |
| github-code-review | Analyze diffs, leave PR comments |
| github-repo-management | Clone, create, fork, configure repos |
| codebase-inspection | LOC counting, language breakdown |

---

## MCP (1 dir, 2 skills)

Model Context Protocol integration.

| Skill | Purpose |
|---|---|
| mcporter | CLI to list/configure/call MCP servers |
| native-mcp | Built-in MCP client — auto-discovers server tools |

---

## Creative (1 dir, 7 skills)

Content generation tools.

| Skill | Purpose |
|---|---|
| ascii-art | ASCII art via pyfiglet (571 fonts) |
| ascii-video | ASCII art video pipeline |
| excalidraw | Hand-drawn style diagrams |
| manim-video | Math/technical animations (3Blue1Brown style) |
| p5js | Interactive generative visual art |
| popular-web-designs | 54 production-quality design systems |
| songwriting-and-ai-music | AI music generation (Suno) |

---

## Productivity (1 dir, 7 skills)

Document and workspace integration.

| Skill | Purpose |
|---|---|
| google-workspace | Gmail, Calendar, Drive, Sheets, Docs |
| notion | Notion API — pages, databases, blocks |
| linear | Linear issue management (GraphQL) |
| canvas | Canvas LMS integration |
| powerpoint | .pptx creation/editing |
| nano-pdf | Edit PDFs with natural language |
| ocr-and-documents | OCR, PDF text extraction |

---

## Other Bundled (6 dirs, 7 skills)

Low-frequency utilities.

| Category | Skill | Purpose |
|---|---|---|
| desktop-environment/ | hyprland-nvidia-arch-setup | Hyprland on Arch + NVIDIA Optimus |
| note-taking/ | obsidian | Read/search/create Obsidian notes |
| red-teaming/ | godmode | LLM jailbreak techniques (G0DM0D3) |
| media/ | youtube-content | YouTube transcripts |
| media/ | heartmula | Music generation (HeartMuLa) |
| media/ | songsee | Audio spectrograms |
| leisure/ | find-nearby | Find nearby places (OpenStreetMap) |
| feeds/ | blogwatcher | RSS monitoring (duplicate of research/) |
| diagramming/ | (empty) | No skills |
| domain/ | (empty) | No skills |

---

## Skill Counts by Priority

| Tier | Dirs | Skills | Description |
|---|---|---|---|
| WIMS-BFP Core | 6 | 9 | Project-specific, user-created |
| Agent Infra | 3 | 16 | Orchestration, dev workflow, wiki |
| ML/AI | 2 | 29 | Training, inference, research |
| GitHub | 1 | 6 | CI/CD, PRs, repos |
| Creative | 1 | 7 | Content generation |
| Productivity | 1 | 7 | Docs, workspace |
| MCP | 1 | 2 | Protocol integration |
| Other | 6 | 7 | Desktop, media, niche |
| **Total** | **23** | **~83** | |
