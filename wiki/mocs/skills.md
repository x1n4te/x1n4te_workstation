---
id: skills-moc-001
type: MOC
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-07-08
stale_after: 2026-10-08
confidence: high
source_refs: []
status: active
tags:
  - skills
  - hermes
  - MOC
related:
  - entities/hermes-agent-setup
---

# Skills — Map of Content

**Total:** ~88 skills across 19 categories
**Full inventory:** [[sources/software-dev/hermes-skills-inventory]]
**Location:** `~/.hermes/skills/`
**Last inventory:** 2026-04-08

---

## WIMS-BFP Specific (Custom)

| Skill | Purpose |
|-------|---------|
| `devops/wims-bfp-security-review` | Security audit gates for WIMS-BFP |
| `devops/wims-bfp-two-agent-refactor` | Refactoring workflow |
| `wims-bfp-codebase-audit` | Codebase audit methodology |
| `devops/specter-audit-remediation` | Audit remediation workflow |
| `rls-null-bypass-fix` | PostgreSQL RLS null bypass fix |
| `phase-1-crit-fixes` | Critical fixes phase |
| `nextjs-ts-strict-fixes` | TypeScript strict mode fixes |

## Software Development

|| Skill | Purpose |
||-------|---------|
|| `software-development/code-review` | Code review methodology |
|| `software-development/design-an-interface` | Parallel interface design exploration via sub-agents (Design It Twice) |
|| `software-development/docs-vs-code-discrepancy-scan` | 5-phase: extract claims → scan evidence → cross-reference → severity → resolution |
|| `software-development/grill-me` | Iterative 5-domain design alignment — ask 5 questions per round until shared understanding |
|| `software-development/improve-codebase-architecture` | Refactor shallow modules into deep modules for better AI navigation |
|| `software-development/plan` | Planning methodology |
|| `software-development/requesting-code-review` | Request review workflow |
|| `software-development/subagent-driven-development` | Multi-agent dev workflow |
|| `software-development/systematic-debugging` | Debugging methodology |
|| `software-development/tdd-triple-agent` | TDD with 3 agents |
|| `software-development/test-driven-development` | TDD workflow — red-green-refactor with AI-specific adjustments |
|| `software-development/thesis-grounded-review` | Review against thesis claims |
|| `software-development/ultraplan` | Deep planning with iterative refinement |
|| `software-development/ubiquitous-language` | Extract DDD-style domain glossary — shared terminology for AI + team |
|| `software-development/writing-plans` | Plan writing methodology |

## Autonomous AI Agents

| Skill | Purpose |
|-------|---------|
| `autonomous-ai-agents/claude-code` | Claude Code integration |
| `autonomous-ai-agents/codex` | OpenAI Codex integration |
| `autonomous-ai-agents/hermes-agent` | Hermes agent workflows |
| `autonomous-ai-agents/opencode` | OpenCode Go integration |

## LLM Wiki / Ingestion

| Skill | Purpose |
|-------|---------|
| `llm-wiki/llm-wiki-ingest-blog` | Blog ingestion into wiki |
| `llm-wiki/llm-wiki-ingest-cve` | CVE ingestion into wiki |
| `llm-wiki/llm-wiki-ingest-github` | GitHub repo ingestion |
| `llm-wiki/llm-wiki-ingest-pdf` | PDF ingestion into wiki |
| `research/llm-wiki` | LLM wiki research |

## GitHub

| Skill | Purpose |
|-------|---------|
| `github/codebase-inspection` | Codebase inspection |
| `github/github-auth` | GitHub authentication |
| `github/github-code-review` | GitHub code review |
| `github/github-issues` | Issue management |
| `github/github-pr-workflow` | PR workflow |
| `github/github-repo-management` | Repo management |
| `github-release-notes-api` | Release notes via API |

## MLOps

| Skill | Purpose |
|-------|---------|
| `mlops/cloud/modal` | Modal cloud platform |
| `mlops/evaluation/lm-evaluation-harness` | LM eval harness |
| `mlops/evaluation/weights-and-biases` | W&B tracking |
| `mlops/huggingface-hub` | HF Hub integration |
| `mlops/inference/gguf` | GGUF quantization |
| `mlops/inference/guidance` | Guidance library |
| `mlops/inference/llama-cpp` | Llama.cpp inference |
| `mlops/inference/vllm` | vLLM inference |
| `mlops/models/stable-diffusion` | SD image generation |
| `mlops/models/whisper` | Whisper transcription |
| `mlops/training/unsloth` | Unsloth fine-tuning |
| `mlops/training/trl-fine-tuning` | TRL fine-tuning |
| `mlops/training/grpo-rl-training` | GRPO RL training |

## Creative

| Skill | Purpose |
|-------|---------|
| `creative/ascii-art` | ASCII art generation |
| `creative/ascii-video` | ASCII video |
| `creative/excalidraw` | Diagram creation |
| `creative/manim-video` | Math animations |
| `creative/p5js` | p5.js sketches |
| `creative/popular-web-designs` | Web design patterns |
| `creative/songwriting-and-ai-music` | Music generation |

## Research

| Skill | Purpose |
|-------|---------|
| `research/arxiv` | Arxiv paper search |
| `research/blogwatcher` | Blog monitoring |
| `research/ml-paper-writing` | ML paper writing |
| `research/polymarket` | Polymarket prediction |
| `research/research-paper-writing` | Research paper writing |

## Productivity

| Skill | Purpose |
|-------|---------|
| `productivity/google-workspace` | Google Docs/Sheets/Slides |
| `productivity/notion` | Notion integration |
| `productivity/ocr-and-documents` | OCR document processing |
| `productivity/powerpoint` | PowerPoint creation |

## DevOps

| Skill | Purpose |
|-------|---------|
| `devops/webhook-subscriptions` | Webhook management |

## MCP

| Skill | Purpose |
|-------|---------|
| `mcp/mcporter` | MCP server management |
| `mcp/native-mcp` | Native MCP integration |

## Other

| Skill | Purpose |
|-------|---------|
| `note-taking/obsidian` | Obsidian integration |
| `desktop-environment/hyprland-nvidia-arch-setup` | Hyprland + NVIDIA on Arch |
| `red-teaming/godmode` | Red teaming |
| `media/gif-search` | GIF search |
| `media/youtube-content` | YouTube content |
| `leisure/find-nearby` | Location search |

---

## Skills to Review for Cleanup

| Skill | Issue |
|-------|-------|
| `hermes-4agent-discord-setup` | Multi-agent Discord abandoned |
| `devops/wims-bfp-two-agent-refactor` | May be stale — verify relevance |
| `mlops/vastai-vllm-multi-gpu` | Not using Vast.ai currently |
