---
id: spa-rls-stale-cache-bypass-2026-05-07
type: source
created: 2026-05-07
updated: 2026-05-07
last_verified: 2026-05-07
review_after: 2026-06-06
stale_after: 2026-08-05
confidence: high
source_refs:
  - raw/articles/smart-parenting-app-rls-stale-cache-bypass-2026-05-07.md
  - /home/xynate/local-projects/smart-parenting-app/lib/api.ts
  - /home/xynate/local-projects/smart-parenting-app/database/migrations/20260507_soft_delete_child_rpc.sql
  - /home/xynate/local-projects/smart-parenting-app/database/schema.sql
  - /home/xynate/local-projects/smart-parenting-app/supabase/functions/analyze-child/index.ts
status: active
tags:
  - smart-parenting-app
  - supabase
  - rls
  - database
  - api
  - debugging
  - operational
related:
  - concepts/smart-parenting-app-system-architecture
  - concepts/smart-parenting-app-tech-stack
  - sources/operational/2026-04-25-spa-consolidated-database-schema
---

# Smart Parenting App — RLS stale cache bypass via SECURITY DEFINER RPC

## Summary
Child soft-delete broke in the APK with `new row violates row-level security policy for table "children"` even after the `children_update` policy was fixed in Supabase SQL Editor. The working diagnosis is stale PostgREST policy metadata on the REST path, so the app switched deletion from direct table update to a privileged `soft_delete_child()` RPC with an internal ownership guard.

## Verified implementation
- `lib/api.ts` now calls `supabase.rpc('soft_delete_child', { child_id: childId })` in `deleteChild()`.
- `database/migrations/20260507_soft_delete_child_rpc.sql` defines `soft_delete_child(child_id UUID)` as `SECURITY DEFINER`.
- `database/schema.sql` contains the same function in the consolidated source-of-truth schema.
- `database/schema.sql` also documents why `children_update` must not include `deleted_at IS NULL` in the update policy check.

## Root cause
The user handoff reports that PostgREST kept serving a stale cached version of the `children_update` RLS policy even after PostgreSQL itself had the corrected definition. That explains the split behavior:
- direct SQL in the editor succeeded,
- impersonated PL/pgSQL succeeded,
- APK `.update()` requests still failed.

Architecturally, this means the logical policy was correct in PostgreSQL but the REST interface was not trustworthy immediately after the policy edit.

## SECURITY DEFINER bypass pattern
The new RPC keeps the authorization check inside the function:
1. Confirm a row exists where `id = child_id`, `parent_id = auth.uid()`, and `deleted_at IS NULL`.
2. Raise `Child not found or not authorized` if that check fails.
3. Perform `UPDATE children SET deleted_at = NOW() WHERE id = child_id`.

This is a controlled least-privilege bypass: it avoids the stale PostgREST update path without broadening delete authority beyond the authenticated parent.

## Verification performed
- `pg_policies` confirmed `children_update` was corrected to `USING (parent_id = auth.uid())` and `WITH CHECK (parent_id = auth.uid())`.
- Manual SQL Editor update succeeded on the same row.
- PL/pgSQL impersonation with `request.jwt.claim.sub` set to the parent UUID also succeeded.
- Triggers `children_bmi_trigger` and `children_updated_at` were audited and did not interfere with `deleted_at`.
- Live repo inspection confirms the RPC function exists in both the migration and consolidated schema, and confirms the frontend is calling the RPC.

## Deployment trail
- Migration to execute: `database/migrations/20260507_soft_delete_child_rpc.sql`
- Release build command: `./gradlew assembleRelease`
- Reported artifact: `~/local-projects/smart-parenting-app/android/app/build/outputs/apk/release/app-release.apk`
- Reported install target: `192.168.1.15:41095`

## AI model note
The same handoff states the Edge Function model was changed to `baidu/cobuddy:free`. Live code inspection of `supabase/functions/analyze-child/index.ts`, however, still shows `const MODEL = Deno.env.get("OPENROUTER_MODEL") || "inclusionai/ling-2.6-1t:free";`.

Conclusion: the RLS/RPC change is verified in code, but the model-switch claim is currently a documentation/runtime drift item rather than a verified code fact.

## Related pages
This update sharpens [[concepts/smart-parenting-app-system-architecture]] around where authorization truly lives and updates [[concepts/smart-parenting-app-tech-stack]] with the current Edge Function model drift state. It also extends [[sources/operational/2026-04-25-spa-consolidated-database-schema]] because `database/schema.sql` is now the authoritative place where the RPC bypass is documented.
