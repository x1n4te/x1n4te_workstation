---
title: AI Insights Architecture
created: 2026-04-25
updated: 2026-04-25
type: concept
tags: [ai-insights, feature, architecture, security, supabase]
sources: [raw/technical-reference.md]
---

# AI Insights Architecture

The AI feature is a **zero-shot prompting system** that runs entirely server-side via a Supabase Edge Function. No fine-tuning. No training data. No model hosting.

```
Parent taps "Insights" tab
        ↓
Client calls analyzeChild() in lib/api.ts
        ↓
POST to Edge Function: /functions/v1/analyze-child
        ↓
Edge Function:
  1. Fetches 28 days of activities from Supabase (REST, service role key)
  2. Aggregates into compact summary (avg, total, days logged, categories)
  3. Computes trend signals (current vs previous period, ↑→↓)
  4. Computes confidence (high ≥14 days, medium ≥7, low <7)
  5. Fetches real scheduled activities from DB
  6. Builds a structured prompt with ALL data injected
  7. Sends to OpenRouter API (inclusionai/ling-2.6-1t:free)
  8. Parses JSON response
  9. Normalizes via deterministic rules (recommendation-normalizer.ts)
  10. Inserts recommendations into DB with full audit trail
        ↓
Client receives recommendations, caches in state, renders cards
```

See [[ai-insights-display]] for the client-side card UI (3-per-category limit, recency badges, dates).

---

## The Model

**`inclusionai/ling-2.6-1t:free`** via OpenRouter (free tier).

- 1 trillion parameter MoE model (sparse activation)
- Temperature: 0.4 (low randomness)
- Max tokens: 2048
- 1 retry attempt with +0.15 temperature adjustment on failure

**Why zero-shot?** The model is used as a **reasoning engine over structured data** — not as a knowledge base. The prompt contains all context (child data, trends, WHO guidelines). The model synthesizes it.

---

## Prompt Architecture

The prompt is 686 lines of highly structured injection. Key sections:

| Section | What it contains |
|---------|-----------------|
| **Data Quality** | Confidence level, log-day count, flags |
| **Child Profile** | Name, age in years+months, gender, BMI assessment |
| **Developmental Context** | Age-bracketed WHO pediatric guidelines |
| **Routine Schedule** | Bedtime, wake-up, meals, nap, activity, learn times |
| **Configured Limits** | Parent-set max screen time, min sleep |
| **Trend Analysis** | Period-over-period comparison with ↑→↓ symbols |
| **Activity Summary** | 28-day aggregates per activity type |
| **Scheduled Activities** | Real planned activities — completed/pending/skipped/missed counts |
| **Previous Recommendations** | Last 3 recs with age timestamps — forces follow-up comparison |

**Hardcoded instructions:**
- "MUST explicitly cite data in every recommendation"
- Category enum: `screen_time | sleep | meal | education | physical_activity | general`
- `physical_activity` only for movement — NOT generic "activity"
- Structure formula: `[Data citation]. [Limit comparison]. [2-3 sentence advice.]`

---

## Recommendation Normalizer

The model outputs JSON — but LLMs are unreliable at exact enums. The normalizer (`recommendation-normalizer.ts`) is a deterministic post-processing layer:

**Category inference** — weighted regex patterns across sentence segments:
```
screen_time: /\bscreen\s*time\b/i weight=7
sleep: /\bsleep(?:ing)?\b/i weight=7
meal: /\bmeal(?:s)?\b/i weight=7
education: /\beducation(?:al)?\b/i weight=7
physical_activity: /\bphysical\s+activit(?:y|ies)\b/i weight=8
```
Picks the **first** matching segment by character position, highest weight wins ties.

**Priority normalization** → maps any string to `high | medium | low`. Unknown defaults to `medium`.

**Insight type inference** → falls back based on priority: `high`→`risk`, `medium`→`opportunity`, `low`→`positive`.

**Trend normalization** → `null | "null" | "none"` → `null`. Validates against `worsening | stable | improving`.

Max 3 recommendations returned (`.slice(0, 3)`).

---

## Audit Trail (`based_on`)

Every saved recommendation carries a `based_on` JSONB field:

```json
{
  "period": "2026-03-28 to 2026-04-25",
  "compact_summary": { "screen_time": {...}, "sleep": {...} },
  "previous_rec_ids": ["uuid1", "uuid2"],
  "child_settings": { "max_screen_time_minutes": 120, "min_sleep_minutes": 600 },
  "bmi_category": "normal",
  "age_months": 42,
  "scheduled_summary": { "total": 5, "completed": 2, "pending": 3 },
  "model": "inclusionai/ling-2.6-1t:free",
  "confidence": "high",
  "category_normalization": "deterministic-v1"
}
```

This means **every recommendation is reproducible** — replay the exact same inputs, get the same output.

---

## Confidence Scoring

| Log Days | Confidence | Meaning |
|----------|------------|---------|
| ≥ 14 | High | Solid data base |
| 7–13 | Medium | Limited history |
| < 7 | Low | Speculative — flagged in UI |

Flags: `Sparse data`, `No sleep or screen time data — key metrics missing`, `First analysis — no baseline`.

---

## Caching

The **client** (`ai.tsx`) checks `isToday()` before calling the Edge Function — if recommendations already exist for today, it skips the API call. The Edge Function itself does NOT cache. Cache is a client-side UX decision.

---

## Security Considerations

- Edge Function uses **service role key** (bypasses RLS) to write recommendations — intentional and auditable
- OpenRouter API key stored as a Supabase secret, not in the client
- Client NEVER has direct model access
- No child PII sent beyond OpenRouter (name, age, activity stats only)
- `based_on` audit trail allows full reproducibility

Recommendations are displayed via [[ai-insights-display]]. The Edge Function stores the audit trail in `recommendations`.

**Limitation:** This is NOT a medical device. The UI does not claim clinical accuracy. Recommendations are parent-advisory only.
