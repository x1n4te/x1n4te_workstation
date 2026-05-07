---
id: spa-ai-recommendation-flow-session-001
type: source
created: 2026-04-14
updated: 2026-04-14
last_verified: 2026-04-14
review_after: 2026-05-14
stale_after: 2026-07-14
confidence: high
source_refs:
  - raw/articles/smart-parenting-app-codebase-2026-04-13
status: active
tags:
  - smart-parenting-app
  - mobile-dev
  - supabase
  - ai-research
  - openrouter
related:
  - concepts/smart-parenting-app-tech-stack
  - sources/operational/2026-04-14-smart-parenting-feature-session
  - concepts/hci-design-principles-mobile
---

# Smart Parenting App — AI Recommendation Flow Session (2026-04-14)

## Session Goal
Implement the AI recommendation feature for NestNote — stateless zero-shot prompting with context injection.

## Activities

### 1. Flow Design
- Created Excalidraw diagram: `wiki/artifacts/nestnote-ai-recommendation-flow.excalidraw`
- Uploaded: https://excalidraw.com/#json=tj57mNz3KQLVpzDGkc72F,7XvCES9eeVCTLdPtNpI-UA
- Flow: Select child → Query 28-day activities → Query last 3 recommendations → Build zero-shot prompt → Call OpenRouter (stateless) → Store result with based_on JSONB → Display

### 2. Schema Review
Reviewed database schema.sql against AI flow. Found 6 issues:
- Issue 1 FIXED: Activity type CHECK constraint (user applied migration)
- Issue 2 FIXED: getActivitySummary 7d→28d window
- Issue 3 FIXED: analyzeChild() missing previous recommendations in request
- Issue 4 FIXED: Edge Function analyze-child created
- Issue 5 FIXED: Missing composite index on recommendations(child_id, created_at DESC)
- Issue 6 FIXED: TypeScript ActivityType missing nap + physical_activity

**Decision:** 4-week window (28 days) instead of 2 weeks — better pattern recognition for child development, negligible cost increase (~2x input tokens).

### 3. Code Changes

#### api.ts
- `ActivityType` union: added `nap`, `physical_activity` (6 types total)
- `getActivitySummary()`: window changed from 7 days to 28 days
- `analyzeChild()`: rewritten to fetch activities + previous 3 recommendations + child profile in parallel via `Promise.all`, sends all to Edge Function

#### schema.sql
- Added: `CREATE INDEX idx_recommendations_child_created ON recommendations(child_id, created_at DESC);`

#### supabase/functions/analyze-child/index.ts (NEW — 329 lines)
- **Model:** `openrouter/elephant-alpha` (free, 100B params)
- **Activity Aggregation:** groups raw logs by type, computes stats (screen time avg + leisure/educational split, sleep avg/min/max + consistency score, nap frequency, meals per day + unique foods, education subjects, physical activity types)
- **Prompt Builder:** system role "child development advisor" + child profile + 4-week summary + previous 3 recs + structured JSON output instruction
- **Storage:** inserts into recommendations table via Supabase REST API with service role key (bypasses RLS), stores `based_on` JSONB audit trail (period, activity_summary, previous_rec_ids, child_settings, model)
- **CORS:** enabled for cross-origin requests

#### supabase/config.toml (NEW)
- Edge Function config: verify_jwt = false

#### components/ScreenHeader.tsx (NEW)
- Shared header component used by Log, History, AI Insights screens
- Features: icon + title, optional subtitle, child picker pill with avatar, modal child selector, optional back button
- HCI principles: consistency (#4), recognition over recall (#6), user control (#3)

#### app/(tabs)/ai.tsx
- Replaced local heuristic analysis with `analyzeChild()` API call
- Added `isToday()` cache check — skips API call if recommendations already generated today
- Removed 65 lines of local analysis rules
- Uses shared `ScreenHeader` component

#### app/(tabs)/history.tsx
- Replaced custom header + child picker modal with `ScreenHeader` component
- Removed showChildPicker state, childInitial, openChildPicker, handleSelectChild
- Removed 50+ lines of header/picker styles

#### app/(tabs)/log.tsx
- Replaced custom header (back button + centered title + child picker) with `ScreenHeader` component
- Removed showChildPicker state, custom child picker modal with "Add another child" button
- Removed 20+ lines of header/picker styles
- Updated to match History and AI Insights header format (icon + title + child picker pill)

### 4. Testing
- Edge Function tested via curl with test data
- First model (`google/gemma-4-31b-it:free`) rate-limited on OpenRouter
- Switched to `google/gemma-3-27b-it:free` — also rate-limited
- Final model: `openrouter/elephant-alpha` — working
- Test result: 3 recommendations generated (screen_time HIGH, sleep HIGH, nutrition MEDIUM)
- based_on audit trail verified: contains period, activity_summary, child_settings, model

### 5. Supabase Setup Required
- SQL: `CREATE INDEX IF NOT EXISTS idx_recommendations_child_created ON recommendations(child_id, created_at DESC);`
- Secret: `OPENROUTER_API_KEY` set via `supabase secrets set`
- Deploy: `supabase functions deploy analyze-child`

## Files Modified
| File | Change |
|---|---|
| lib/api.ts | ActivityType fix, 28d window, analyzeChild rewrite |
| database/schema.sql | Composite index |
| supabase/functions/analyze-child/index.ts | NEW — Edge Function |
| supabase/config.toml | NEW — Edge Function config |
| components/ScreenHeader.tsx | NEW — shared header |
| app/(tabs)/ai.tsx | Edge Function integration, ScreenHeader |
| app/(tabs)/history.tsx | ScreenHeader, removed picker |
| app/(tabs)/log.tsx | ScreenHeader, removed picker |
| wiki/artifacts/nestnote-ai-recommendation-flow.excalidraw | NEW — flow diagram |
