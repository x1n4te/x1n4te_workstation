---
id: llm-papers-learning-path-001
type: concept
created: 2026-04-09
updated: 2026-04-09
last_verified: 2026-04-09
review_after: 2026-07-09
stale_after: 2026-10-09
confidence: high
status: active
tags:
  - llm
  - papers
  - research
  - transformers
  - learning
related:
  - concepts/llm-foundations-learning-path
  - concepts/llm-transformers-learning-path
  - concepts/llm-applied-learning-path
  - concepts/llm-security-learning-path
---

# LLM Papers — The Canon

**Category 3 of 5** in the LLM Learning Pathway (Cybersecurity-Aligned)
**Prerequisites:** [[concepts/llm-foundations-learning-path]] + [[concepts/llm-transformers-learning-path]]
**Goal:** Read and understand the 8 papers that define modern LLMs. Know the remaining 18 by title and significance.

---

## How to Read Papers

Don't read front-to-back. Use this strategy:

```
1. Title + Abstract     → What did they do?
2. Figures + Tables     → What did they find?
3. Architecture diagram → How does it work?
4. Results section      → Does it work?
5. Intro (last)         → Why does it matter?
```

**Time per paper:** 1-2 hours for deep read, 30 min for skim. Code the key idea if possible.

---

## The 8 Essential Papers

### Paper 1: Attention Is All You Need (Vaswani et al., 2017)

**The paper that started everything.**

- **What:** Introduced the Transformer architecture — self-attention replacing recurrence
- **Key idea:** Process all tokens in parallel using attention. No RNNs, no CNNs.
- **Architecture:** Encoder-decoder with multi-head attention, positional encoding, layer norm
- **Result:** 28.4 BLEU on WMT English-German translation, 41.8 on English-French
- **Why it matters:** Every modern LLM (GPT, Claude, Gemini, LLaMA, Qwen) is built on this
- **arXiv:** 1706.03762

**Read this AFTER:** [[concepts/llm-transformers-learning-path]] — you need the attention mechanism intuition first.

**Cybersecurity angle:** The parallel processing that makes transformers powerful also creates new attack surfaces — attention manipulation, positional encoding exploits.

---

### Paper 2: BERT (Devlin et al., 2018)

**Bidirectional context changed NLP.**

- **What:** Pre-train a transformer encoder on masked language modeling, then fine-tune for tasks
- **Key idea:** Mask random tokens, predict them from both left AND right context (bidirectional)
- **Architecture:** Transformer encoder only (not decoder). Uses [CLS] token for classification.
- **Result:** State-of-the-art on 11 NLP tasks (GLUE, SQuAD, MultiNLI)
- **Why it matters:** Showed that pre-training + fine-tuning beats task-specific architectures
- **arXiv:** 1810.04805

**Key concept:** Masked Language Modeling (MLM) — hide 15% of tokens, predict them. This forces the model to learn bidirectional context.

**Cybersecurity angle:** BERT-style models are used in security NLP — log analysis, threat intelligence extraction, phishing detection.

---

### Paper 3: GPT-2 (Radford et al., 2019)

**Language models as unsupervised multitask learners.**

- **What:** 1.5B parameter decoder-only transformer trained on 40GB of internet text
- **Key idea:** Zero-shot task transfer — no fine-tuning, just prompt the model
- **Architecture:** Decoder-only transformer (causal attention, left-to-right)
- **Result:** State-of-the-art on 7 of 8 language modeling benchmarks without fine-tuning
- **Why it matters:** Showed scaling works. OpenAI initially withheld the model due to misuse concerns.
- **Paper:** "Language Models are Unsupervised Multitask Learners"

**Key concept:** Zero-shot — the model performs tasks it was never explicitly trained for, just by being given the right prompt.

**Cybersecurity angle:** GPT-2's misuse concerns were the first public debate about LLM safety — generating fake news, phishing emails, social engineering at scale.

---

### Paper 4: GPT-3 (Brown et al., 2020)

**In-context learning emerged at scale.**

- **What:** 175B parameter model — 100x larger than GPT-2
- **Key idea:** Few-shot learning via in-context examples. No gradient updates. Just show examples in the prompt.
- **Architecture:** Same as GPT-2 but scaled up 100x
- **Result:** Competitive with fine-tuned models on many tasks using only a few examples
- **Why it matters:** Proved that scale creates emergent capabilities. In-context learning wasn't designed — it emerged.
- **arXiv:** 2005.14165

**Key concepts:**
- Zero-shot: no examples, just instructions
- One-shot: one example in the prompt
- Few-shot: a few examples in the prompt
- Emergent abilities: capabilities that appear at scale but not in smaller models

**Cybersecurity angle:** In-context learning is what your WIMS-BFP XAI pipeline uses — the "Sovereign Forensic Template" provides examples for Qwen2.5-3B to follow.

---

### Paper 5: Scaling Laws (Kaplan et al., 2020)

**Why bigger models work — and when to stop.**

- **What:** Empirical study of how loss scales with model size, dataset size, and compute
- **Key idea:** Loss follows power laws. Three axes: parameters, data, compute. Each has diminishing returns.
- **Key finding:** Performance depends strongly on scale (parameters, data, compute) but weakly on shape (depth vs width)
- **Why it matters:** Guides training decisions. "Should I make the model bigger or train longer?"
- **arXiv:** 2001.08361

**Key concept:** Compute-optimal training (Chinchilla, 2022, extended this) — train smaller models on more data rather than larger models on less data.

**Cybersecurity angle:** Understanding scaling helps you evaluate model claims. A vendor saying "our model is bigger" doesn't automatically mean "better" — depends on data quality and compute.

---

### Paper 6: InstructGPT / RLHF (Ouyang et al., 2022)

**Making models follow instructions — the ChatGPT foundation.**

- **What:** Fine-tune GPT-3 with human feedback to follow instructions safely
- **Key idea:** Three-step process:
  1. Supervised fine-tuning (SFT) on human demonstrations
  2. Train a reward model (RM) from human comparisons
  3. Optimize the policy using PPO against the reward model (RLHF)
- **Result:** 1.3B InstructGPT preferred over 175B GPT-3 by humans
- **Why it matters:** This is the training recipe behind ChatGPT, Claude, and every instruction-tuned model
- **arXiv:** 2203.02155

**Key concepts:**
- RLHF: Reinforcement Learning from Human Feedback
- Reward model: learns human preferences from comparisons
- Alignment tax: aligned models may sacrifice some benchmark performance for safety
- Helpful, harmless, honest (3H): the alignment goals

**Cybersecurity angle:** RLHF alignment is a security boundary. Jailbreaking works by exploiting the gap between the reward model's training distribution and adversarial inputs.

---

### Paper 7: LLaMA (Touvron et al., 2023)

**Open-weight models democratized LLMs.**

- **What:** 7B-65B parameter models trained on publicly available data
- **Key idea:** Smaller models trained on more data can match larger models (Chinchilla-optimal)
- **Architecture:** Standard transformer with pre-normalization (RMSNorm), SwiGLU activation, rotary embeddings
- **Result:** LLaMA-13B outperforms GPT-3 (175B) on most benchmarks
- **Why it matters:** Open weights enabled fine-tuning, local deployment, and the entire open-source LLM ecosystem
- **arXiv:** 2302.13971

**Key concept:** Chinchilla-optimal training — for a fixed compute budget, train a smaller model on more data.

**Cybersecurity angle:** Open-weight models mean organizations can run LLMs on-premise (like your WIMS-BFP Qwen2.5-3B). No data leaves the network. Critical for government/defense applications.

---

### Paper 8: DeepSeek-R1 / GRPO (DeepSeek, 2025)

**Reinforcement learning for reasoning — the current frontier.**

- **What:** Train LLMs to reason via reinforcement learning with verifiable rewards
- **Key idea:** Group Relative Policy Optimization (GRPO) — generate multiple completions, score them with a verifier, optimize toward correct reasoning paths
- **Architecture:** Standard transformer + RL training loop
- **Result:** Competitive with OpenAI o1 on reasoning benchmarks, using pure RL
- **Why it matters:** Shows reasoning can be learned through RL, not just scale. Open-source alternative to closed reasoning models.
- **arXiv:** 2501.12948

**Key concepts:**
- RLVR: Reinforcement Learning with Verifiable Rewards
- Chain-of-thought: model generates reasoning steps before answers
- Inference-time compute: spending more compute at generation time improves accuracy
- Distillation: training smaller models on reasoning traces from larger ones

**Cybersecurity angle:** Reasoning models are more capable but also more dangerous — they can plan multi-step attacks. Understanding RLVR helps you anticipate future AI threats.

---

## The Extended Reading List (18 more)

These fill gaps between the 8 essential papers. Read as needed.

| Paper | Year | Focus | arXiv |
|---|---|---|---|
| Transformer-XL (Dai et al.) | 2019 | Longer context via segment recurrence | 1901.02860 |
| RoBERTa (Liu et al.) | 2019 | Better BERT training (more data, longer) | 1907.11692 |
| T5 (Raffel et al.) | 2019 | Text-to-text framework, unified NLP | 1910.10683 |
| GPT-3 paper (Brown et al.) | 2020 | In-context learning, 175B params | 2005.14165 |
| Chinchilla (Hoffmann et al.) | 2022 | Compute-optimal training | 2203.15556 |
| PaLM (Chowdhery et al.) | 2022 | 540B model, scaling analysis | 2204.02311 |
| Chain-of-Thought (Wei et al.) | 2022 | Prompting for reasoning steps | 2201.11903 |
| LLaMA 2 (Touvron et al.) | 2023 | Open weights + safety tuning | 2307.09288 |
| Mistral 7B (Jiang et al.) | 2023 | Efficient architecture (sliding window) | 2310.06825 |
| Mixtral 8x7B (Jiang et al.) | 2024 | Mixture of experts | 2401.04088 |
| Mamba (Gu & Dao) | 2023 | State-space model alternative to attention | 2312.00752 |
| LoRA (Hu et al.) | 2021 | Low-rank adaptation for fine-tuning | 2106.09685 |
| RAG (Lewis et al.) | 2020 | Retrieval-augmented generation | 2005.11401 |
| Constitutional AI (Bai et al.) | 2022 | Self-alignment via AI feedback | 2212.08073 |
| DPO (Rafailov et al.) | 2023 | Direct preference optimization (simpler RLHF) | 2305.18290 |
| Qwen2 (Yang et al.) | 2024 | Your XAI model's architecture family | 2407.10671 |
| GRPO (DeepSeek) | 2025 | Group relative policy optimization | 2501.12948 |
| RLVR (DeepSeek) | 2025 | Verifiable rewards for reasoning | 2502.12009 |

**Full 26-paper list with summaries:** Algo Insights — medium.com/@algoinsights/the-only-26-papers-you-need-to-understand-modern-llms

---

## Reading Strategy

```
Week 1: Papers 1-2 (Attention + BERT)
  → You now understand the architecture and pre-training paradigm

Week 2: Papers 3-4 (GPT-2 + GPT-3)
  → You now understand scaling, zero-shot, and in-context learning

Week 3: Papers 5-6 (Scaling Laws + InstructGPT)
  → You now understand training economics and alignment

Week 4: Papers 7-8 (LLaMA + DeepSeek-R1)
  → You now understand the current landscape and open-source frontier
```

---

## Cybersecurity Connection — Per Paper

| Paper | Security Relevance |
|---|---|
| Attention Is All You Need | Attention manipulation attacks, positional encoding exploits |
| BERT | Security NLP (log analysis, phishing detection, threat intel) |
| GPT-2 | First public AI safety debate — misuse at scale |
| GPT-3 | In-context learning = your XAI pipeline's mechanism |
| Scaling Laws | Evaluate model vendor claims, compute security |
| InstructGPT/RLHF | Jailbreaking exploits reward model gaps |
| LLaMA | On-premise deployment = data sovereignty |
| DeepSeek-R1 | Reasoning models can plan multi-step attacks |

---

## Estimated Time

| Phase | Time |
|---|---|
| 8 essential papers (deep read) | ~12 hours |
| 18 extended papers (skim) | ~9 hours |
| **Total** | **~21 hours** |

Spread across 4 weeks at 5 hours/week.

---

## Next Step

After completing this category: [[concepts/llm-applied-learning-path]] — Applied LLMs (Category 4). Start coding.

---

*Part of the LLM Learning Pathway — 5 categories from foundations to LLM security.*
