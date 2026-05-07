---
id: local-llm-finetuning-roadmap-001
type: concept
created: 2026-04-12
updated: 2026-04-12
last_verified: 2026-04-12
review_after: 2026-05-12
stale_after: 2026-10-12
confidence: high
source_refs:
  - sources/operational/2026-04-12-local-llm-setup-finetuning-journey
status: active
tags:
  - llm
  - training
  - agents
  - design
related:
  - concepts/karpathy-loop-autoresearch
  - concepts/jagged-frontier-ai-capability
  - entities/andrej-karpathy
---

# Local LLM Fine-Tuning Roadmap — x1n4te's Coding Assistant

## Overview

A 5-phase plan to build a personalized coding assistant that runs entirely on a GTX 1050 3GB, using knowledge distillation from MiniMax M2.7 (teacher) to Qwen2.5-Coder-3B (student).

## Architecture

```
MiniMax M2.7 (cloud API)          Qwen2.5-Coder-3B (local, GTX 1050)
  ┌─────────────────┐               ┌─────────────────┐
  │ Teacher model   │──synthetic──▶ │ Student model   │
  │ 230B / 10B act  │   data gen    │ 3B, Q4_K_M GGUF │
  │ $0.30/M tokens  │               │ 17.4 t/s, ₱0    │
  └─────────────────┘               └─────────────────┘
         │                                   │
         ▼                                   ▼
  Generates 5K Q&A pairs           Fine-tuned with Unsloth
  in x1n4te's coding style         + LoRA (rank 16, 2 epochs)
```

## Phase 1: Base Inference ✅ COMPLETE

| Metric | Value |
|---|---|
| Model | Qwen2.5-Coder-3B-Instruct (Q4_K_M) |
| Backend | Ollama (GGUF + llama.cpp) |
| Speed | 17.4 t/s |
| VRAM | ~1.8GB / 3.16GB |
| Cost | ₱0 |

Daily command: `ollama run qwen2.5-coder:3b-instruct`

## Phase 2: IDE Integration

- Continue.dev plugin for VS Code
- Connects to local Ollama API at `http://localhost:11434`
- Inline code completion (FIM — fill in the middle)
- Chat sidebar for code questions
- Zero config — Ollama auto-detects installed models

## Phase 3: SFT on Coding Patterns (Week 1)

### Step 1: Collect source material
- 50-100 samples of x1n4te's code (functions, naming conventions, patterns)
- From: WIMS-BFP, Smart Parenting App, CTF writeups, pentest scripts

### Step 2: Generate synthetic data via M2.7
- Feed M2.7 the samples as style examples
- Prompt: "Generate 5000 coding Q&A pairs in this style"
- Format: Unsloth chat template (system/user/assistant)
- Cost: ~$5-10 of M2.7 API tokens

### Step 3: Fine-tune with Unsloth + LoRA
- Base: Qwen2.5-Coder-3B (loaded from HuggingFace)
- LoRA: rank=16, alpha=32, target=all linear layers
- Epochs: 2
- Learning rate: 2e-4
- Hardware: GTX 1050 3GB (4-6 hours)
- Output: LoRA adapter (~30MB)

### Expected result
- Model writes code that looks like x1n4te's
- Follows x1n4te's naming conventions
- Uses x1n4te's preferred patterns

## Phase 4: RL Polish via Karpathy Loop (Week 2)

Based on [[concepts/karpathy-loop-autoresearch]]:

| Component | Implementation |
|---|---|
| Single file | `train_rl.py` — GRPO training script |
| Single metric | pass@1 on code execution (does it compile? pass tests?) |
| Fixed time | 30 min per experiment |

### Experiment grid
- LoRA rank: 8, 16, 32, 64
- Learning rate: 1e-4, 2e-4, 5e-4
- Epochs: 1, 2, 3
- Data augmentation: prompt variations
- Total: 72 experiments
- Time: 36 hours on Vast.ai RTX 3090
- Cost: ~$7

### Expected result
- Optimal training config found by agent, not by guessing
- Model generates code that actually compiles
- Self-correcting behavior (retries on failure)

## Phase 5: Sushi Coder Distillation (Future)

Full replication of the Sushi Coder training recipe at 3B scale:

1. **SFT** on `open-r1/codeforces-cots` (CodeForces chain-of-thought)
2. **RL** via NousResearch/atropos (same framework Sushi Coder used)
3. **Export** as GGUF Q4_K_M for distribution

Compare: x1n4te's personal fine-tune vs Sushi Coder recipe vs generic Qwen2.5-Coder-3B

## Hardware Requirements

| Component | Spec | Used |
|---|---|---|
| GPU | GTX 1050 3GB (sm_61) | SFT training + inference |
| RAM | 20GB | Model loading + data processing |
| Python | 3.12 (via uv) | Training environment |
| venv | `~/pentest-llm/` | PyTorch 2.6.0+cu124, Unsloth, bitsandbytes |

### Known issue: Triton sm_61
Triton kernels use `.evict_first` PTX instruction which requires sm_70+. GTX 1050 is sm_61.

**Solution:** Ollama for inference (GGUF + llama.cpp, no Triton). Unsloth for training (uses different code path).

## Cost Summary

| Phase | Cost | Time |
|---|---|---|
| 1. Base inference | ₱0 | Done |
| 2. IDE integration | ₱0 | 30 min |
| 3. SFT (M2.7 data gen) | ~$5-10 | 1 week |
| 4. RL (Karpathy Loop) | ~$7 | 1 week |
| 5. Sushi Coder distillation | ~$7 | 1 week |
| **Total** | **~$15-25** | **3 weeks** |

## Sources

- [[sources/operational/2026-04-12-local-llm-setup-finetuning-journey]]
- [[concepts/karpathy-loop-autoresearch]]
- [[concepts/jagged-frontier-ai-capability]]
- [[entities/andrej-karpathy]]
