# Hindsight Memory Migration Session Log — 2026-04-18

## Status: ABANDONED — Returning to Honcho

Honcho still has $40 USD credits remaining. User elected to stay on Honcho and
defer Hindsight migration for when credits approach exhaustion.

---

## What Was Attempted

1. **Honcho credit exhaustion imminent** — triggered comparison of memory providers
2. **Hindsight selected** — LongMemEval 91.4-94.6%, free self-hosted, 4 retrieval strategies
3. **Docker deployment** — full image (ghcr.io/vectorize-io/hindsight:latest)
4. **Hurdles cleared:**
   - Docker volume permissions (root-owned ~/.hindsight-data → chmod 777)
   - Embedding env vars removed (full image has local embeddings)
   - Groq gpt-oss-20b selected (200k tokens/day free tier)
5. **Hurdle that stopped progress:**
   - Groq gpt-oss-20b has **8,000 TPM limit**
   - Hindsight fact-extraction prompt (system instructions + mission + schema) is ~8-11k tokens
   - Even a single short sentence exceeded the limit → HTTP 413 → 0 facts extracted
6. **Attempted fix:** Switched docker run to llama-3.3-70b-versatile (32k TPM) but
   $GROQ_API_KEY was not exported in shell environment → container failed to start

---

## Root Cause

```
HTTP 413: Request too large for model `openai/gpt-oss-20b`
tokens per minute (TPM): Limit 8000, Requested 11001
```

Hindsight's fact extraction is synchronous and sends the full bank mission + system
prompt + extraction schema alongside user content. The overhead is ~8k tokens before
user content is even added. gpt-oss-20b at 8k TPM cannot handle it.

---

## Resolution

- Hindsight container stopped and removed
- Stayed on Honcho ($40 credits remaining)
- Skill `hindsight-memory-setup` updated with correct config (llama-3.3-70b-versatile + RETAIN_MAX_COMPLETION_TOKENS=32000)
- All Honcho memory preserved (peer cards, observations, conclusions intact)

---

## Key Learnings

| Finding | Detail |
|---|---|
| gpt-oss-20b TPM | 8,000 (too low for Hindsight extraction) |
| llama-3.3-70b-versatile TPM | 32,000 (sufficient) |
| Hindsight extraction overhead | ~8k tokens/system prompt before user content |
| CLI --document-tags | Deprecated — tags not persisted to item level |
| CLI batch retain | Synchronous — times out on large batches |
| REST API | More reliable for batch operations with tags |
| `retain_extraction_mode: standard` | Still fails at 8k TPM limit |

---

## When to Resume Migration

When Honcho credits near $0:
1. Export Groq API key to shell: `export GROQ_API_KEY=gsk_...`
2. Run Hindsight with `llama-3.3-70b-versatile` (not gpt-oss-20b)
3. Set `HINDSIGHT_API_RETAIN_MAX_COMPLETION_TOKENS=32000`
4. Test single fact retain before batch import
5. Use REST API with unique `document_id` per fact for tag support

---

## Files Modified

- `~/.hermes/skills/devops/hindsight-memory-setup/SKILL.md` — docker run template updated
  with `llama-3.3-70b-versatile` and `RETAIN_MAX_COMPLETION_TOKENS=32000`
