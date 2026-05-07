## AI Implementation — Smart Parenting App

### Architecture Overview

The AI feature is a **zero-shot prompting system** that runs entirely server-side via a Supabase Edge Function. No **fine-tuning**. No **training data**. No **model hosting**.

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
  7. Sends to OpenRouter API (openrouter/elephant-alpha model)
  8. Parses JSON response
  9. Normalizes via deterministic rules (recommendation-normalizer.ts)
  10. Inserts recommendations into DB with full audit trail
        ↓
Client receives recommendations, caches in state, renders cards
```

---

### The Model

**`inclusionai/ling-2.6-1t:free`** via OpenRouter (free tier).

- 1 trillion parameter MoE model (sparse activation — only activates relevant experts per token)
- This is NOT GPT-4, NOT Claude, NOT locally hosted
- Selected for: free access, reasonable quality for structured JSON output
- Temperature: 0.4 (low randomness, consistent outputs)
- Max tokens: 2048
- 1 retry attempt with +0.15 temperature adjustment on failure

**Why zero-shot?** Because the model is used as a **reasoning engine over structured data** — not as a knowledge base. The prompt contains all the context (child data, trends, WHO guidelines). The model synthesizes it. No fine-tuning needed because the prompt is the curriculum.

---

### Prompt Architecture

The prompt is the product. It's 686 lines of highly structured injection. Key sections:

| Section | What it contains |
|---------|-----------------|
| **Data Quality** | Confidence level, log-day count, flags (e.g., "Sparse data") |
| **Child Profile** | Name, age in years+months, gender, BMI assessment (z-score, percentile, WHO category) |
| **Developmental Context** | Age-bracketed WHO pediatric guidelines (INFANT/TODDLER/PRESCHOOLER/SCHOOL-AGE) |
| **Routine Schedule** | Bedtime, wake-up, meals, nap, activity, learn times — from child's profile |
| **Configured Limits** | Parent-set max screen time, min sleep |
| **Trend Analysis** | Period-over-period comparison with ↑→↓ symbols |
| **Activity Summary** | 28-day aggregates per activity type with specific numbers |
| **Scheduled Activities** | Real planned activities from DB — completed/pending/skipped/missed counts |
| **Previous Recommendations** | Last 3 recs with age timestamps — forces follow-up comparison |

**Hardcoded instructions** include:
- "MUST explicitly cite data in every recommendation"
- Category enum restricted to: `screen_time | sleep | meal | education | physical_activity | general`
- `physical_activity` only for movement — NOT generic "activity"
- Structure formula: `[Data citation]. [Limit comparison]. [2-3 sentence advice.]`
- Follow-up requirement if prior recommendations exist

---

### Recommendation Normalizer

The model outputs JSON — but LLMs are unreliable at emitting exact enums. The normalizer (`recommendation-normalizer.ts`) is a deterministic post-processing layer:

**Category inference** — Uses weighted regex patterns across sentence segments:
```
screen_time: /\bscreen\s*time\b/i weight=7, /\b(tablet|phone|tv|device)\b/i weight=3
sleep: /\bsleep(?:ing)?\b/i weight=7, /\bbed\s*time\b/i weight=4
meal: /\bmeal(?:s)?\b/i weight=7, /\bfruit|vegetable|protein\b/i weight=3
education: /\beducation(?:al)?\b/i weight=7, /\bread|homework|school\b/i weight=4
physical_activity: /\bphysical\s+activit(?:y|ies)\b/i weight=8, /\boutdoor\s+play\b/i weight=5
```
Picks the **first** matching segment by character position, highest weight wins ties.

**Priority normalization** — Maps any string to `high | medium | low`. Unknown defaults to `medium`.

**Insight type inference** — Falls back based on priority: `high`→`risk`, `medium`→`opportunity`, `low`→`positive`.

**Trend normalization** — `null | "null" | "none"` → `null`. Validates against `worsening | stable | improving`.

Max 3 recommendations returned (`.slice(0, 3)`).

---

### Audit Trail (`based_on`)

Every saved recommendation carries a `based_on` JSONB field:

```json
{
  "period": "2026-03-28 to 2026-04-25",
  "compact_summary": { "screen_time": {...}, "sleep": {...}, ... },
  "previous_rec_ids": ["uuid1", "uuid2"],
  "child_settings": { "max_screen_time_minutes": 120, "min_sleep_minutes": 600 },
  "bmi_category": "normal",
  "age_months": 42,
  "scheduled_summary": { "total": 5, "completed": 2, "pending": 3, ... },
  "model": "inclusionai/ling-2.6-1t:free",
  "confidence": "high",
  "category_normalization": "deterministic-v1"
}
```

This means **every recommendation is reproducible** — replay the exact same inputs, get the same output. Panelists can verify the logic without re-running the model.

---

### Confidence Scoring

| Log Days | Confidence | Meaning                     |
| -------- | ---------- | --------------------------- |
| ≥ 14     | High       | Solid data base             |
| 7–13     | Medium     | Limited history             |
| < 7      | Low        | Speculative — flagged in UI |

Flags emitted: `Sparse data`, `No sleep or screen time data — key metrics missing`, `First analysis — no baseline`.

---

### Caching

The **client** (`ai.tsx`) checks `isToday()` before calling the Edge Function — if recommendations already exist for today, it skips the API call entirely. The Edge Function itself does NOT cache — it regenerates on every call. Cache is a client-side UX decision to avoid redundant API calls.

---

### Security Considerations

- Edge Function uses **service role key** (bypasses RLS) to write recommendations back — this is intentional and auditable
- The API key for OpenRouter is stored as a Supabase secret, not in the client
- Client NEVER has direct access to the model — all AI traffic goes through the Edge Function
- No child PII sent to third-party beyond OpenRouter (child name, age, activity stats only)
- `based_on` audit trail allows full reproducibility — can be audited without re-running AI

---

## Likely Panelist Questions

### 1. "How does the AI generate recommendations? Is it trained on child development data?"

**Answer:** No training. Zero-shot prompting. The model (`inclusionai/ling-2.6-1t:free`, 1T parameter MoE) acts as a reasoning engine — the prompt IS the knowledge. The prompt injects:
- The child's actual activity data (28 days of logs)
- WHO age-specific pediatric guidelines (developmental context section)
- Parent-configured limits (screen time max, sleep min)
- Previous recommendations with follow-up comparison instructions

The model synthesizes these structured inputs into natural language advice. No fine-tuning, no curated training set.

---

### 2. "What model are you using? Why that one?"

**Answer:** `inclusionai/ling-2.6-1t:free` via OpenRouter. A 1-trillion parameter sparse Mixture-of-Experts model. Selected because:
1. Free tier — critical for a ₱12K commission with no server budget
2. Capable of structured JSON output
3. OpenRouter provides abstraction — can swap to GPT-4 or Claude by changing one line in the Edge Function without touching app code

**Limitation:** Quality is dependent on the free model. Production systems should use GPT-4o or Claude 3.5 Sonnet for better recommendation quality.

---

### 3. "How do you ensure the recommendations are safe? What if the AI suggests something dangerous?"

**Answer:** Three safety layers:

1. **Prompt hardcoding** — The system prompt explicitly instructs the model to cite data and stay within WHO guidelines. It cannot invent medical advice outside the child's actual logged data.

2. **Output normalization** — The normalizer (`recommendation-normalizer.ts`) enforces a strict schema. Even if the model hallucinates a `category`, the regex-based inference maps it to one of 6 allowed categories. Invalid recommendations are filtered out (max 3 pass through).

3. **RLS + service role** — The Edge Function writes recommendations to the `recommendations` table. The client reads them through RLS (filtered to `child_id` the parent owns). The parent always sees AI output before it reaches their child.

**Limitation:** This is NOT a medical device. The UI does not claim clinical accuracy. Recommendations are parent-advisory only.

---

### 4. "The model could hallucinate. How do you verify recommendations are correct?"

**Answer:** Through the `based_on` audit trail. Every recommendation has a `based_on` JSONB field containing:
- The exact 28-day data window used
- The compact summary (all aggregated metrics)
- The previous recommendation IDs
- The model used
- The confidence level

A panelist or auditor can:
1. Take the same input data
2. Replay the prompt
3. Verify the output matches

Additionally, the `recommendation-normalizer.ts` has a test file (`recommendation-normalizer.test.ts`) validating that malformed/edge inputs produce correct outputs.

---

### 5. "How do you handle the case where there's no data? What does the AI say?"

**Answer:** The confidence scoring handles this explicitly:
- `data_days < 7` → `confidence: low` + flag: `"Sparse data — recommendations may be speculative"`
- Empty activity summary → prompt shows `"No activity data available."`
- No previous recs → `"First analysis — no baseline for comparison"`

The model is instructed to acknowledge uncertainty in low-confidence cases. The UI shows a confidence banner when data is sparse.

---

### 6. "Is the AI running on the device or in the cloud?"

**Answer:** Cloud. Supabase Edge Functions (Deno runtime) on Supabase's infrastructure. The client makes a single HTTPS call to `https://[PROJECT].supabase.co/functions/v1/analyze-child`. The model runs on OpenRouter's servers. No local AI.

---

### 7. "Why not use local AI / on-device inference?"

**Answer:** Three reasons:
1. **Hardware:** The target test device (Xiaomi Note 12 4G, GTX 1050 laptop) cannot run a 1B+ parameter model efficiently
2. **Cost:** ₱12K commission budget — no server costs available. OpenRouter free tier + Supabase free tier = ₱0 AI infrastructure cost
3. **Quality:** Free local models (TinyLlama, Qwen2.5-3B) are unreliable at structured JSON output required for the recommendation schema

If this were a funded startup product: GPT-4o or Claude 3.5 Sonnet via OpenRouter, or a fine-tuned open model on Modal/Vast.ai GPU.

---

### 8. "What's the computational cost? How many API calls?"

**Answer:** One Edge Function invocation per "Generate Insights" tap. With client-side today-caching: at most once per parent per child per day.

The Edge Function itself makes:
- 1 REST call to Supabase (fetch scheduled activities)
- 1 OpenRouter API call (chat completions)
- N INSERT calls to Supabase (one per recommendation, max 3)

This is stateless — no session, no context window, no KV cache. Every call is a fresh computation.

---

### 9. "How does the app handle network failures or AI timeouts?"

**Answer:** The Edge Function has:
- 30-second timeout on OpenRouter call (via `AbortController`)
- 1 retry with temperature bump (+0.15)
- On all attempts failing → HTTP 502 with the last raw AI response in the error body

The client (`ai.tsx`):
- Loading state during API call
- Error banner with retry button on failure
- No silent failures — parent always knows if analysis failed

---

### 10. "What data does the AI see? Is it GDPR/PDPA compliant?"

**Answer:** Data sent to OpenRouter:
- Child name (first name only in prompt — `"Name: Juan"`)
- Age (in months/years)
- Activity statistics (aggregates, NOT raw logs)
- BMI assessment
- Routine schedule times

**NOT sent:** Parent email, parent name, family location, device identifiers, raw activity timestamps

The Philippines **PDPA** applies — parent consent is required for processing child data. The app requires parent account creation and explicitly presents the AI feature as processing their child's data. The `based_on` audit trail allows data lineage verification.

**Limitation:** No formal PDPA/DPA consent checkbox currently implemented in the onboarding wizard. This is a gap for the ethics review.

---

### 11. "Why is this better than a rule-based system?"

**Answer:** A rule-based system would require hardcoding thresholds for every combination of:
- Age × activity type × gender × BMI category
- Trend direction × previous recommendation × scheduled vs actual

That's a combinatorial explosion. The AI approach:
- One prompt template, parameterized by actual data
- Automatically handles new activity types (just add to the aggregation)
- Can synthesize cross-domain insights ("screen time is up AND sleep is down — consider bedtime routine")

The trade-off: rule-based is auditable by inspection; AI is auditable only by reproduction (via `based_on`).
