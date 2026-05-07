---
id: local-llm-setup-finetuning-journey-001
type: source
created: 2026-04-12
updated: 2026-04-12
last_verified: 2026-04-12
review_after: 2026-05-12
stale_after: 2026-07-12
confidence: high
source_refs: []
status: active
tags:
  - llm
  - training
  - agents
  - mobile-dev
  - cybersecurity
related:
  - concepts/local-llm-finetuning-roadmap
  - concepts/karpathy-loop-autoresearch
  - concepts/jagged-frontier-ai-capability
  - concepts/ai-cybersecurity-pipeline
---

# Local LLM Setup + Fine-Tuning Journey — Session Log (2026-04-12)

**Duration:** ~3 hours
**Goal:** Set up a local coding LLM and plan fine-tuning pipeline

---

## What We Did

### 1. Trend Radar Setup
- Installed blogwatcher-cli (17 RSS feeds: Karpathy, Simon Willison, Hugging Face, r/LocalLLaMA, r/MachineLearning, arxiv cs.AI/cs.CL, Google DeepMind, etc.)
- Created GitHub trending scanner (`github-trending.py`) — detects AI/ML repos from daily Python trending
- Created RSS trend radar script (`trend-radar.py`) — filters feeds for AI/LLM relevance
- Set up cron job: runs 8AM + 8PM daily, delivers to Telegram
- Baselined 1,038 historical articles (marked as read)

### 2. AISLE Jagged Frontier Ingestion
- Ingested: https://aisle.com/blog/ai-cybersecurity-after-mythos-the-jagged-frontier
- Key finding: Small open models (3.6B params, $0.11/M tokens) match Mythos on cybersecurity detection
- The moat is the system scaffolding, not the model
- Created 3 wiki pages (entity: AISLE, concept: jagged frontier, concept: AI cybersecurity pipeline)

### 3. Karpathy AutoResearch Ingestion
- Ingested Fortune article on "The Karpathy Loop"
- 3-component recipe: single file + single metric + fixed time
- 700 experiments in 2 days, 20 optimizations found
- Applied to WIMS-BFP: 72 experiments × 30 min × $7 on Vast.ai
- Created 3 wiki pages (raw source, entity: Karpathy, concept: Karpathy Loop)

### 4. Model Selection Research
Evaluated models for local fine-tuning on GTX 1050 3GB:

| Model | Params | Decision |
|---|---|---|
| Qwen3.5-4B-Base | 4B | Multimodal — rejected (vision overhead) |
| Gemma 3 4B | 4B | Not coding-specialized — rejected |
| Qwen2.5-Coder-3B | 3B | Coding-specialized, fits GPU — SELECTED |
| StarCoder2-3B | 3B | Base completion only, weak instructions — rejected |
| MiniMax M2.7 | 230B/10B active | Too big for local — use as TEACHER via API |
| Sushi Coder 27B | 27B | Too big for local — use distillation approach |

**Decision:** Qwen2.5-Coder-3B as student, MiniMax M2.7 as teacher (knowledge distillation)

### 5. Environment Setup
- Python 3.12 via uv (Python 3.14 too new for PyTorch)
- Created venv: `~/pentest-llm/`
- Installed: PyTorch 2.6.0+cu124, Unsloth 2026.4.4, bitsandbytes, transformers
- CUDA confirmed working on GTX 1050 (sm_61)
- Issue: Triton kernels incompatible with sm_61 (`.evict_first` requires sm_70+)
- Fix: Use Ollama for inference (GGUF + llama.cpp), keep Unsloth for training only

### 6. Model Inference — Phase 1 Complete
- Downloaded Qwen2.5-Coder-3B-Instruct (Q4_K_M via Ollama)
- Result: **17.4 t/s** average (15x faster than bitsandbytes at 1.2 t/s)
- VRAM: ~1.8GB (comfortable fit on 3GB GPU)
- Tests passed: Python function, SQL query, bug fix, shell command
- Quality: Clean code output, Instruct variant follows prompts well

---

## Fine-Tuning Roadmap Established

### Phase 1: Base inference ✅ DONE
- Qwen2.5-Coder-3B-Instruct via Ollama
- 17.4 t/s on GTX 1050
- Daily command: `ollama run qwen2.5-coder:3b-instruct`

### Phase 2: IDE integration (next)
- Continue.dev plugin for VS Code
- Connects to Ollama API automatically
- Inline code completion + chat

### Phase 3: SFT on coding patterns (week 1)
- Collect 50-100 samples of x1n4te's code
- Use MiniMax M2.7 API to generate 3,000-5,000 synthetic Q&A pairs in that style
- Fine-tune Qwen2.5-Coder-3B with Unsloth + LoRA (rank 16, 2 epochs, ~4-6 hrs on GTX 1050)
- Cost: ~$5-10 of M2.7 tokens
- Result: model that codes like x1n4te

### Phase 4: RL polish via Karpathy Loop (week 2)
- Take SFT model
- Run GRPO training via NousResearch/atropos
- Reward: does generated code compile? Pass tests?
- 72 experiments on Vast.ai RTX 3090
- Cost: ~$7
- Result: model that's both YOUR style AND correct

### Phase 5: Sushi Coder distillation (future)
- Distill full Sushi Coder recipe (SFT + RL) at 3B scale
- Use open-r1/codeforces-cots dataset for SFT
- Use atropos for RL
- Export as GGUF for distribution

---

## Key Decisions Made
1. **Ollama for inference, Unsloth for training** — split architecture to avoid Triton sm_61 issue
2. **Qwen2.5-Coder-3B over Qwen3.5-4B** — fits 3GB GPU, coding-specialized, proven for fine-tuning
3. **M2.7 as teacher, not local model** — knowledge distillation beats trying to run 230B locally
4. **Karpathy Loop for hyperparameter search** — 72 experiments automated vs manual guessing
5. **GGUF Q4_K_M quantization** — best quality/speed balance for 3GB GPU

## Files Created
- `~/local-llm/test_inference.py` — Ollama inference test script
- `~/pentest-llm/` — Python 3.12 venv with PyTorch + Unsloth
- `~/.hermes/scripts/trend-radar.py` — RSS feed scanner
- `~/.hermes/scripts/github-trending.py` — GitHub trending scanner
