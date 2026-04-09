---
id: llm-foundations-learning-path-001
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
  - learning
  - neural-networks
  - foundations
  - deep-learning
related:
  - concepts/llm-transformers-learning-path
  - concepts/llm-security-learning-path
  - entities/hermes-agent-setup
---

# LLM Foundations — How Neural Networks Learn

**Category 1 of 5** in the LLM Learning Pathway (Cybersecurity-Aligned)
**Goal:** Build intuition for how neural networks learn, optimize, and generalize. No skipping — everything else builds on this.

---

## The Core Question

How does a pile of numbers (weights) learn to recognize patterns, generate text, or detect threats?

Answer in 4 steps:
1. **Neurons** — simple functions that take inputs, multiply by weights, sum, and activate
2. **Loss** — a score measuring how wrong the model's predictions are
3. **Gradient descent** — adjusting weights to reduce loss (the "learning" part)
4. **Backpropagation** — efficiently computing how each weight contributed to the error

---

## Resources

### 3Blue1Brown — Neural Networks Series (Ch 1-4)

The single best visual introduction to neural networks. Grant Sanderson's animations make the math intuitive.

| Video                                       | Duration | What You Learn                                                              |
| ------------------------------------------- | -------- | --------------------------------------------------------------------------- |
| But what is a Neural Network?               | 19 min   | Neurons, layers, weights — introduced through handwritten digit recognition |
| Gradient descent, how neural networks learn | 21 min   | Loss functions, learning rate, why models converge (or don't)               |
| What is backpropagation really doing?       | 13 min   | The chain rule applied to neural nets — how errors flow backward            |
| Backpropagation calculus                    | 11 min   | The actual math — partial derivatives, weight updates                       |

**Watch order:** Sequential (Ch 1 → 2 → 3 → 4). Each builds on the previous.

**Why it matters for cybersecurity:** Understanding gradient descent helps you understand adversarial attacks — perturbing inputs in the direction of steepest loss increase to fool classifiers.

**Link:** https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi

---

### Andrej Karpathy — micrograd (Building micrograd)

Build a tiny autograd engine (automatic differentiation) from scratch in ~1 hour. This is what PyTorch does internally, scaled down.

**What you build:**
- A `Value` class that tracks operations and computes gradients
- Backward pass through a computational graph
- A small neural network trained with your engine

**Why it matters:** After watching 3B1B, this makes it real. You write the math in code. By the end, you understand what `loss.backward()` does in PyTorch.

**Link:** https://www.youtube.com/watch?v=VMj-3S1tku0
**Code:** https://github.com/karpathy/micrograd

---

### Andrej Karpathy — "The spelled-out intro to neural networks and backpropagation"

Same content as micrograd but in lecture format with more explanation. Pick this OR micrograd — both cover the same ground.

**Link:** https://www.youtube.com/watch?v=VMj-3S1tku0

---

### Welch Labs — How Models Learn (Parts 1-3)

More visual intuition, complementary to 3B1B. Welch Labs focuses on WHY deep learning works, not just HOW.

| Video | Focus |
|---|---|
| Part 1 | The basics — what learning means for a neural net |
| Part 2 | Backpropagation intuition (different angle than 3B1B) |
| Part 3 | Why deep learning works unreasonably well — generalization, overfitting |

**Playlist:** https://www.youtube.com/playlist?list=PLccH6XYi5vIlWaqKD6QaMHjpmJDct517M

**Also watch:** "The moment we stopped understanding AI (AlexNet)" — historical context on when neural nets became too complex for humans to interpret. This connects to your XAI work with Qwen2.5-3B.

**Link:** https://www.youtube.com/watch?v=D8GOeCFFby4

---

## Key Concepts to Nail

After completing this category, you should be able to explain:

| Concept | One-liner |
|---|---|
| Neuron | Weighted sum of inputs, passed through an activation function |
| Activation function | Non-linear function (ReLU, sigmoid) that lets networks learn non-linear patterns |
| Loss function | Score measuring prediction error (cross-entropy for classification) |
| Gradient | Direction of steepest increase in loss — we go the opposite way |
| Learning rate | Step size in gradient descent — too big = diverge, too small = slow |
| Backpropagation | Chain rule applied layer-by-layer to compute weight gradients |
| Overfitting | Model memorizes training data but fails on new data |
| Epoch | One pass through the entire training dataset |

---

## Cybersecurity Connection

Understanding foundations directly applies to:

1. **Adversarial ML** — gradient-based attacks (FGSM, PGD) exploit the same math the model uses to learn
2. **Anomaly detection** — your Suricata + XAI pipeline uses neural network outputs; understanding loss functions helps you interpret detection confidence
3. **Model interpretability** — backpropagation tells you which inputs contributed most to a prediction (gradient-based attribution)
4. **Qwen2.5-3B tuning** — if you ever fine-tune your XAI model, you need to understand learning rate, epochs, overfitting

---

## Estimated Time

| Resource               | Time                            |
| ---------------------- | ------------------------------- |
| 3Blue1Brown (Ch 1-4)   | ~1 hour                         |
| Karpathy micrograd     | ~1.5 hours (watch + code along) |
| Welch Labs (Parts 1-3) | ~1.5 hours                      |
| Key concepts review    | 30 min                          |
| **Total**              | **~4.5 hours**                  |

One weekend of focused study.

---

## Next Step

After completing this category: [[concepts/llm-transformers-learning-path]] — Transformers & Attention (Category 2)

---

*Part of the LLM Learning Pathway — 5 categories from foundations to LLM security. Designed for cybersecurity practitioners.*
