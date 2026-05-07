---
id: 2026-04-25-spa-ai-recommendation-category-normalization
type: source
created: 2026-04-25
updated: 2026-04-25
status: active
tags:
  - smart-parenting-app
  - ai-insights
  - supabase-edge-functions
  - recommendations
---

# Smart Parenting App — AI Recommendation Category Normalization

## Summary

Hardened the `analyze-child` Supabase Edge Function after recommendations were classified into the ambiguous legacy `activity` category even when the primary evidence was not physical activity.

## Root cause

The prompt allowed `nutrition | activity | general`, while the app/database activity taxonomy uses concrete categories such as `meal`, `education`, and `physical_activity`. The model could therefore overuse `activity` because the prompt also contains generic sections like `ACTIVITY SUMMARY` and `SCHEDULED ACTIVITIES`. The Edge Function inserted the model category directly with no deterministic validation.

## Changes

- Added deterministic recommendation normalization in `supabase/functions/analyze-child/recommendation-normalizer.ts`.
- Updated prompt category contract to exactly: `screen_time | sleep | meal | education | physical_activity | general`.
- Mapped legacy aliases:
  - `nutrition` → `meal`
  - `activity` → inferred from content, not accepted directly
  - generic scheduled/routine activity advice → `general`
- Restricted `physical_activity` to explicit movement evidence such as physical activity, outdoor/active play, playground, sports, swimming, dancing, walking practice, motor skills, or movement.
- Normalizes priority, insight type, and trend before insertion.
- Adds `category_normalization: "deterministic-v1"` to `based_on` for auditability.
- Checks Supabase REST insert responses before returning recommendations.

## Verification

- Added Deno regression tests covering:
  - ambiguous `activity` + screen-time citation → `screen_time`
  - replacement physical-activity suggestion after screen-time evidence still → `screen_time`
  - same-sentence physical-activity suggestion after earlier screen-time evidence still → `screen_time`
  - replacement education/reading suggestion after low-weight TV evidence still → `screen_time`
  - app-reminder wording in generic scheduled routines stays `general`
  - generic scheduled activities → `general`
  - `nutrition` → `meal`
  - explicit physical movement → `physical_activity`
  - mislabelled physical category with sleep evidence → `sleep`
- `deno test supabase/functions/analyze-child/recommendation-normalizer.test.ts` passed.
- `deno check --no-lock supabase/functions/analyze-child/recommendation-normalizer.ts` passed.
- `npx tsc --noEmit --pretty false` passed.

## Note

A full `deno check` of `index.ts` was attempted, but the Supabase Edge Runtime type package triggered large npm dependency resolution through Deno and timed out in this local environment. The pure normalizer module and Expo TypeScript project checks passed.
