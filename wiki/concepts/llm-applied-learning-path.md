---
id: llm-applied-learning-path-001
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
  - applied
  - fine-tuning
  - rag
  - agents
  - deployment
  - learning
related:
  - concepts/llm-papers-learning-path
  - concepts/llm-security-learning-path
  - concepts/llm-transformers-learning-path
  - entities/hermes-agent-setup
---

# Applied LLMs — Using, Fine-Tuning, Building

**Category 4 of 5** in the LLM Learning Pathway (Cybersecurity-Aligned)
**Prerequisites:** [[concepts/llm-papers-learning-path]] — at least Papers 1-4
**Goal:** Go from understanding LLMs to actually building with them. Hands-on, code-first.

---

## The Core Question

You understand transformers, attention, and scaling. Now: how do you USE LLMs in real systems?

Four levels of engagement:
1. **Use APIs** — call GPT/Claude/Qwen, prompt engineering
2. **Fine-tune** — adapt a pre-trained model to your domain
3. **Build pipelines** — RAG, agents, tool use
4. **Deploy** — run models on your own hardware (you already do this with Qwen2.5-3B)

---

## Section 1: Using LLMs via APIs

### Resources

| Resource | What | Link |
|---|---|---|
| OpenAI API docs | GPT-4, function calling, structured outputs | platform.openai.com/docs |
| Anthropic API docs | Claude, tool use, system prompts | docs.anthropic.com |
| Nous Portal | Free-tier models (MiMo v2 Pro, etc.) | portal.nousresearch.com |

### Key Concepts

| Concept | What | Why It Matters |
|---|---|---|
| System prompt | High-level instructions that shape model behavior | Your first line of defense against prompt injection |
| Temperature | Randomness of output (0 = deterministic, 1 = creative) | Security tasks need low temperature for consistency |
| Max tokens | Output length limit | Prevents runaway generation (cost control) |
| Function calling | Model outputs structured JSON for tool use | How hermes agent calls terminal, web_search, etc. |
| Structured outputs | Force JSON schema compliance | Reliable parsing — no hallucinated fields |
| Context window | Max input + output tokens | GPT-4: 128K, Claude: 200K, Qwen2.5: 128K |

### Hands-On You Already Have

Your hermes agent uses all of these:
- System prompts via HERMES.md
- Function calling (terminal, browser, web_search, etc.)
- Multi-provider routing (Nous Portal, OpenRouter)
- Temperature control (reasoning_effort)

**Document what you've learned.** You have more applied LLM experience than most learners.

---

## Section 2: Fine-Tuning

### Resources

| Resource | What | Link |
|---|---|---|
| Hugging Face NLP Course (Ch 3-4) | Fine-tuning with Transformers library | huggingface.co/learn/nlp-course |
| Unsloth | 2x faster fine-tuning, 60% less memory | github.com/unslothai/unsloth |
| Axolotl | Multi-GPU fine-tuning framework | github.com/axolotl-ai-cloud/axolotl |
| LoRA paper (Hu et al., 2021) | Low-Rank Adaptation — fine-tune efficiently | arxiv.org/abs/2106.09685 |
| Sebastian Raschka — "Build a LLM from Scratch" | Book: from tokenizer to fine-tuning | amazon.com (search title) |

### Fine-Tuning Methods (Ordered by Cost)

| Method | What | Cost | When to Use |
|---|---|---|---|
| **Prompt engineering** | No training, just better prompts | Free | First thing to try always |
| **Few-shot prompting** | Examples in the prompt | Free (token cost) | When prompt engineering isn't enough |
| **RAG** | Retrieve relevant context, inject into prompt | Low | When you need domain knowledge |
| **LoRA/QLoRA** | Low-rank adapter on top of frozen base model | Medium | When you need model behavior change |
| **Full fine-tuning** | Update all parameters | High | Rarely needed, mostly for pre-training |
| **RLHF/DPO** | Align model to human preferences | High | Safety, helpfulness, instruction following |

### When to Fine-Tune vs When NOT to

```
Fine-tune when:
  ✓ You need consistent output format
  ✓ Domain-specific terminology/behavior
  ✓ Base model doesn't understand your jargon
  ✓ You have 100+ high-quality examples

Don't fine-tune when:
  ✗ Prompt engineering can solve it (try first!)
  ✗ You have fewer than 50 examples
  ✗ You just need the model to know facts (use RAG instead)
  ✗ You're fine-tuning to "fix" safety guardrails
```

### Connection to WIMS-BFP

Your Qwen2.5-3B XAI pipeline uses **in-context learning** (not fine-tuning). The "Sovereign Forensic Template" provides examples in the prompt. This is the right approach for your use case — fine-tuning a 3B model on Suricata alerts would risk overfitting and lose general language understanding.

If you ever need to improve XAI narrative quality, consider:
1. Better prompt engineering (try first)
2. More/better examples in the template (few-shot)
3. LoRA fine-tuning (only if 1-2 fail)

---

## Section 3: RAG (Retrieval-Augmented Generation)

### Resources

| Resource | What | Link |
|---|---|---|
| RAG paper (Lewis et al., 2020) | The original RAG paper | arxiv.org/abs/2005.11401 |
| LangChain RAG tutorial | End-to-end RAG pipeline | python.langchain.com/docs/tutorials/rag |
| LlamaIndex | Data framework for RAG | docs.llamaindex.ai |
| ChromaDB | Lightweight vector database | docs.trychroma.com |

### RAG Pipeline

```
User query
    ↓
Embed query (text → vector)
    ↓
Vector search (find similar documents)
    ↓
Retrieve top-K documents
    ↓
Inject into prompt: "Context: {docs}\n\nQuestion: {query}"
    ↓
LLM generates answer grounded in retrieved context
    ↓
Response with citations
```

### Key Concepts

| Concept | What | Why It Matters |
|---|---|---|
| Embedding | Text → dense vector (e.g., 768 dimensions) | Enables semantic similarity search |
| Chunking | Split documents into smaller pieces | Prevents context window overflow, improves retrieval precision |
| Vector database | Stores embeddings for fast similarity search | ChromaDB, Pinecone, Weaviate, Qdrant |
| Retrieval | Finding relevant chunks for a query | The "R" in RAG — quality here determines answer quality |
| Reranking | Re-score retrieved chunks with a cross-encoder | Improves precision after initial retrieval |
| Hallucination | Model generates plausible but false information | RAG reduces this by grounding in real documents |

### RAG vs Fine-Tuning

| Aspect | RAG | Fine-Tuning |
|---|---|---|
| Knowledge | External, updatable | Baked into weights |
| Cost | Low (no training) | Medium-High (GPU hours) |
| Freshness | Always current (re-index) | Stale after training |
| Accuracy | Depends on retrieval quality | Depends on training data |
| Best for | Facts, documents, knowledge bases | Behavior, style, format |

### Connection to Your LLM Wiki

Your LLM Wiki IS a RAG system. The wiki pages are the knowledge base. When hermes reads `wiki/index.md`, `wiki/log.md`, and session files at session start — that's retrieval-augmented generation. You're already doing RAG, just manually.

---

## Section 4: Agents & Tool Use

### Resources

| Resource | What | Link |
|---|---|---|
| ReAct paper (Yao et al., 2022) | Reasoning + Acting framework | arxiv.org/abs/2210.03629 |
| LangChain Agents | Agent frameworks | python.langchain.com/docs/modules/agents |
| OpenAI function calling | Structured tool invocation | platform.openai.com/docs/guides/function-calling |

### Agent Architecture

```
User request
    ↓
LLM decides: answer directly OR use a tool
    ↓ (if tool)
LLM generates tool call (structured JSON)
    ↓
Tool executes (API call, code, search, etc.)
    ↓
Tool result fed back to LLM
    ↓
LLM generates final response
```

### Agent Patterns

| Pattern | How It Works | Example |
|---|---|---|
| ReAct | Reason → Act → Observe loop | "I need to check X → call tool → see result → answer" |
| Plan-and-execute | Plan steps first, execute sequentially | "Step 1: search, Step 2: analyze, Step 3: report" |
| Multi-agent | Multiple LLMs with different roles | Orchestrator → Builder → Tester → Critic |
| Reflexion | Self-critique and retry | "My first answer was wrong because X, let me try Y" |

### Connection to Hermes Agent

Hermes IS an agent system. Your setup:
- **ReAct pattern** — hermes reasons about what tool to use, executes, observes results
- **Tool use** — terminal, browser, web_search, file operations, cron
- **Skills** — procedural memory (SKILL.md files) loaded on demand
- **Delegation** — subagent spawning via delegate_task

You're already building with agents. Document what works and what doesn't.

### Connection to WIMS-BFP

Your XAI pipeline is a simple agent:
1. **Trigger** — Suricata generates EVE JSON alert
2. **Tool** — FastAPI extracts metadata
3. **Prompt** — "Sovereign Forensic Template" with alert data
4. **LLM** — Qwen2.5-3B generates narrative
5. **Output** — Human-readable forensic report

Not a full ReAct loop, but the same pattern: structured input → LLM processing → structured output.

---

## Section 5: Deployment & Local Inference

### Resources

| Resource | What | Link |
|---|---|---|
| Llama.cpp | CPU/GPU inference for GGUF models | github.com/ggerganov/llama.cpp |
| vLLM | High-throughput GPU serving | github.com/vllm-project/vllm |
| Ollama | Easy local model serving | ollama.com |
| GGUF format | Quantized model format for local inference | huggingface.co/models?sort=trending&search=gguf |

### Quantization Methods

| Method | Bits | Quality | Speed | Use Case |
|---|---|---|---|---|
| FP16 | 16 | Best | Slowest | Training, research |
| GPTQ | 4/8 | Good | Fast | GPU inference |
| AWQ | 4 | Good | Fast | GPU inference |
| GGUF Q4_K_M | 4 | Good | Fast | CPU/local inference |
| GGUF Q8_0 | 8 | Better | Medium | CPU/local, higher quality |

### Your Hardware (GTX 1050 Max-Q, 3GB VRAM)

| Model | Quantization | Fits in VRAM? | Performance |
|---|---|---|---|
| Qwen2.5-3B | Q4_K_M | Yes | Good for XAI tasks |
| Phi-3-mini (3.8B) | Q4_K_M | Yes | Good general purpose |
| Llama-3.2-3B | Q4_K_M | Yes | Good instruction following |
| Mistral-7B | Q4_K_M | Tight | May need CPU offload |
| Qwen2.5-7B | Q4_K_M | No | Needs CPU or more VRAM |

### Connection to WIMS-BFP

You're already running Qwen2.5-3B via Llama.cpp on consumer hardware. This is "AI-on-Premise" — no data leaves the network. Critical for government applications where data sovereignty matters.

---

## Cybersecurity Connection

| Concept | Security Application |
|---|---|
| API usage | Prompt injection via API parameters, token smuggling |
| Fine-tuning | Data poisoning during training, backdoor injection |
| RAG | Vector database poisoning (OWASP LLM08), retrieval manipulation |
| Agents | Excessive agency (OWASP LLM06), tool misuse via prompt injection |
| Deployment | Model extraction, membership inference, side-channel attacks |

Your [[sources/software-dev/wims-bfp-ch3c-security-tools|WIMS-BFP XAI pipeline]] uses in-context learning (RAG-like) with Qwen2.5-3B. Understanding these applied concepts helps you evaluate and secure your own system.

---

## Hands-On Projects

### Project 1: Build a RAG System for Your Wiki
- Index all wiki pages into ChromaDB
- Query: "What's the WIMS-BFP architecture?" → retrieves relevant pages → generates answer
- **Why:** You already have the knowledge base. RAG makes it queryable.

### Project 2: Fine-Tune Qwen2.5-3B for Security Narratives
- Collect 200+ Suricata alerts → human-written narratives
- LoRA fine-tune Qwen2.5-3B on this dataset
- Compare XAI narrative quality before/after
- **Why:** Direct thesis application. Could improve MOS scores.

### Project 3: Build a Security Agent
- Agent that reads Suricata logs, queries CVE databases, generates threat reports
- Tools: web_search, file_read, terminal
- Pattern: ReAct loop
- **Why:** Applies agent architecture to your cybersecurity domain.

### Project 4: Evaluate LLM Security of Your XAI Pipeline
- Test prompt injection via Suricata log payloads
- Test narrative poisoning (can an attacker make Qwen2.5-3B generate misleading reports?)
- Document findings in thesis Chapter 3 security evaluation
- **Why:** Strengthens your thesis AND applies Category 5 knowledge.

---

## Estimated Time

| Section | Time |
|---|---|
| API usage review | 1 hour (you already know this) |
| Fine-tuning concepts + LoRA paper | 3 hours |
| RAG pipeline (theory + build) | 4 hours |
| Agents & tool use | 2 hours |
| Deployment & quantization | 1 hour (you already know this) |
| Hands-on project (pick one) | 5-10 hours |
| **Total** | **~16-21 hours** |

2-3 weeks at 1-2 hours/day.

---

## Next Step

After completing this category: [[concepts/llm-security-learning-path]] — LLM Security (Category 5). Your cybersecurity background makes this your highest-value category.

---

*Part of the LLM Learning Pathway — 5 categories from foundations to LLM security.*
