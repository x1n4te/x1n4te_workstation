---
id: llm-transformers-learning-path-001
type: concept
created: 2026-04-09
updated: 2026-04-09
last_verified: 2026-04-09
review_after: 2026-07-09
stale_after: 2026-10-09
confidence: high
source_refs:
  - https://www.3blue1brown.com/
  - https://karpathy.ai/2025/01/16/llmwiki/
status: active
tags:
  - llm
  - learning
  - transformers
  - attention
  - deep-learning
related:
  - concepts/llm-foundations-learning-path
  - concepts/llm-papers-learning-path
  - concepts/llm-security-learning-path
---

# LLM Transformers & Attention — The Architecture Behind LLMs

**Category 2 of 5** in the LLM Learning Pathway (Cybersecurity-Aligned)
**Prerequisite:** [[concepts/llm-foundations-learning-path]] — Category 1
**Goal:** Understand the transformer architecture, attention mechanism, and why it replaced RNNs.

---

## The Core Question

Why did "Attention Is All You Need" (Vaswani et al., 2017) change everything?

**Before transformers:** RNNs and LSTMs processed tokens sequentially — one at a time, left to right. Slow, hard to parallelize, struggled with long-range dependencies.

**After transformers:** Process ALL tokens in parallel. Use attention to let every token "look at" every other token. Scale to billions of parameters. This is why GPT, Claude, Gemini, and every modern LLM exists.

---

## The Transformer Architecture (Decoder-Only, as used in GPT)

```
Input tokens
    ↓
Token Embedding (each token → dense vector)
    ↓
+ Positional Encoding (injects sequence order)
    ↓
┌─────────────────────────────┐
│  Transformer Block (×N)     │
│                             │
│  ┌───────────────────────┐  │
│  │ Multi-Head Self-Attn  │  │ ← Each token attends to all others
│  │ Q = XWq, K = XWk,    │  │
│  │ V = XWv               │  │
│  │ Attention(Q,K,V) =    │  │
│  │ softmax(QKᵀ/√dk)V    │  │
│  └───────────┬───────────┘  │
│              + (residual)   │
│              ↓              │
│         Layer Norm          │
│              ↓              │
│  ┌───────────────────────┐  │
│  │ Feed-Forward (MLP)    │  │ ← Processes each position independently
│  │ Linear → ReLU → Linear│  │
│  └───────────┬───────────┘  │
│              + (residual)   │
│              ↓              │
│         Layer Norm          │
└─────────────────────────────┘
    ↓
Linear → Softmax → Next token probability
```

**Key insight:** The transformer block repeats N times (GPT-3: 96 layers, GPT-4: rumored 100+). Each layer adds more capacity to capture complex patterns.

---

## Resources

### 3Blue1Brown — Deep Learning Series (Ch 5-7)

The best visual introduction to transformers. Grant Sanderson's animations make attention intuitive.

| Video | Duration | What You Learn |
|---|---|---|
| Large Language Models explained briefly | 8 min | Lightweight intro — what LLMs are, how they generate text |
| Transformers, the tech behind LLMs (Ch 5) | 27 min | Overall transformer structure, word embeddings, positional encoding |
| Attention in transformers, step-by-step (Ch 6) | 26 min | The attention mechanism — queries, keys, values, softmax weighting |
| How might LLMs store facts (Ch 7) | 58 min | MLP layers as key-value stores, knowledge localization |

**Watch order:** Ch 5 → Ch 6 → Ch 7. The "briefly" video is optional if you already know what LLMs are.

**Why Ch 6 matters most:** Attention is THE mechanism. If you understand Q/K/V and softmax weighting, you understand transformers. Everything else is engineering around this core idea.

**Link:** https://www.youtube.com/playlist?list=PLsrWLF95_TpcRzOjrRSX1-T2f6se2MFb4

---

### Andrej Karpathy — "Let's build GPT: from scratch, in code, spelled out"

The definitive hands-on tutorial. You code a GPT following the "Attention is All You Need" paper. ~2 hours.

**What you build (in order):**

| Section | Timestamp | What |
|---|---|---|
| Bigram baseline | 0:22:11 | Simplest model — predict next char from current char |
| Self-attention v1 | 0:42:13 | Averaging past context with for loops (weakest form) |
| Self-attention v2 | 0:51:54 | Using matrix multiply as weighted aggregation |
| Self-attention v3 | 0:54:42 | Adding softmax |
| Self-attention v4 | 1:02:00 | **THE CRUX** — full self-attention with Q/K/V |
| Multi-headed attention | 1:21:59 | Multiple attention heads in parallel |
| Feedforward layers | 1:24:25 | MLP inside transformer block |
| Residual connections | 1:26:48 | Skip connections for gradient flow |
| Layer normalization | 1:32:51 | Stabilizing training |
| Dropout + scaling up | 1:37:49 | Regularization and model size |

**Why this matters:** After watching 3B1B, this makes it real. You write the attention mechanism in PyTorch. By the end, you understand what every line of a transformer does.

**Link:** https://www.youtube.com/watch?v=kCc8FmEb1nY
**Code:** https://github.com/karpathy/nanoGPT
**Colab:** https://colab.research.google.com/drive/1JMLa53HDuA-i7ZBmqV7ZnA3c_fvtXnx

---

### Andrej Karpathy — "Let's build the GPT Tokenizer"

How text becomes tokens. Critical for understanding:
- Why models struggle with spelling and counting
- Why token limits exist
- How adversarial token smuggling works (security relevance)

**What you learn:**
- Byte Pair Encoding (BPE) — how vocabularies are built
- Unicode handling — why "café" might be 2 tokens but "cafe" is 1
- Special tokens — BOS, EOS, padding
- Token boundaries — where models "see" breaks in text

**Link:** https://www.youtube.com/watch?v=zduSFxRajkE

---

### Welch Labs — How DeepSeek Rewrote the Transformer (MLA)

Modern transformer variant — Multi-head Latent Attention (MLA). Shows how the architecture is still evolving in 2026. DeepSeek compressed the KV cache, enabling longer contexts with less memory.

**Why it matters:** Understanding MLA helps you understand why newer models (DeepSeek, Qwen) can handle longer contexts than older GPT architectures.

**Link:** Search "Welch Labs DeepSeek MLA" on YouTube

---

## The Attention Mechanism — Step by Step

This is the most important concept in modern AI. Understand this and everything else follows.

```
1. Each token has three vectors: Query (Q), Key (K), Value (V)
   - Q = "What am I looking for?"
   - K = "What do I contain?"
   - V = "What information do I provide?"

2. Attention score = how relevant is token j to token i?
   score(i,j) = Q_i · K_j / √d_k
   (dot product of query and key, scaled by dimension)

3. Softmax converts scores to probabilities (weights)
   weights = softmax(scores)
   (all weights sum to 1.0)

4. Output = weighted sum of values
   output_i = Σ weights(i,j) × V_j

5. Multi-head: do this H times with different Q/K/V projections
   → captures different relationship types
   → concatenate heads → linear projection → output
```

**In plain English:** Each token asks "which other tokens are relevant to me?" via its query. Other tokens answer "here's what I offer" via their keys. The attention score measures relevance. The output is a weighted blend of values from relevant tokens.

---

## Key Concepts to Nail

| Concept | One-liner | Why It Matters |
|---|---|---|
| Tokenization | Splitting text into model-processable units (subwords) | Explains context limits, token costs, adversarial input crafting |
| Embedding | Mapping tokens to dense vectors in continuous space | Semantic similarity — "king" - "man" + "woman" ≈ "queen" |
| Positional encoding | Injecting sequence order (transformers have no inherent order) | Sinusoidal or learned — tells model "this word comes third" |
| Self-attention | Each token computes weighted relevance to every other token | The core mechanism — O(n²) complexity, why long context is expensive |
| Query/Key/Value | Three projections — what to look for, what to offer, what to retrieve | Q/K determine attention weights, V carries actual information |
| Multi-head attention | Multiple attention "heads" capture different relationship types | Head 1 might capture syntax, Head 2 captures semantics |
| Residual connection | Skip connection that helps gradients flow through deep networks | Without this, deep transformers can't train |
| Layer normalization | Stabilizes training by normalizing activations | Prevents internal covariate shift |
| Feed-forward (MLP) | Per-position processing between attention layers | Where "knowledge" is stored (see Ch 7 by 3B1B) |
| KV cache | Stores computed K/V from previous tokens during generation | Why inference memory grows with context length |
| Context window | Max tokens the model can attend to | GPT-4: 128K, Claude: 200K, Qwen2.5: 128K |

---

## The RNN → Transformer Transition

| Aspect | RNN/LSTM | Transformer |
|---|---|---|
| Processing | Sequential (one token at a time) | Parallel (all tokens at once) |
| Long-range dependencies | Struggles (vanishing gradients) | Handles well (direct attention) |
| Training speed | Slow (sequential) | Fast (parallelizable on GPUs) |
| Scaling | Hard to scale past ~100M params | Scales to 100B+ params |
| Memory at inference | Fixed (hidden state) | Grows with context (KV cache) |
| Used by | Old NLP models (2014-2017) | Every modern LLM (2017-present) |

---

## Cybersecurity Connection

### 1. Token Smuggling
Adversarial inputs use Unicode tricks to bypass token-level filters. Understanding tokenization helps you detect these attacks.

### 2. Context Window Attacks
Filling the context window with irrelevant content to push system prompts out of scope. Understanding attention helps you design prompts that resist this.

### 3. Attention Analysis for XAI
Your Qwen2.5-3B XAI pipeline generates narratives from Suricata alerts. Attention weights show what the model "focused on" — useful for verifying narrative quality and detecting hallucination.

### 4. KV Cache Side Channels
Research has shown that KV cache memory patterns can leak information about the conversation. Relevant if you're evaluating LLM deployment security.

### 5. Prompt Injection via Attention
Crafting inputs that hijack attention away from system instructions. Understanding Q/K/V helps you understand why prompt injection works and how to defend against it.

---

## Estimated Time

| Resource | Time |
|---|---|
| 3Blue1Brown (Ch 5-7) | ~2 hours |
| Karpathy "build GPT" | ~2.5 hours (watch + code along) |
| Karpathy tokenizer | ~1.5 hours |
| Key concepts review | 30 min |
| **Total** | **~6.5 hours** |

One weekend of focused study (continuation of Category 1).

---

## Next Step

After completing this category: [[concepts/llm-papers-learning-path]] — Papers (Category 3). Start with "Attention Is All You Need" — you'll have the context to actually read it now.

---

*Part of the LLM Learning Pathway — 5 categories from foundations to LLM security.*
