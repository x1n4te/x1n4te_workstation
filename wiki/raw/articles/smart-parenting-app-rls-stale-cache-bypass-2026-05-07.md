# Smart Parenting App — RLS Stale Cache Bypass via SECURITY DEFINER RPC

Source: user-provided operational handoff
Date captured: 2026-05-07
Project: Smart Parenting App

## Problem Statement
APK threw `new row violates row-level security policy for table "children"` during child soft-delete, even after the `children_update` RLS policy was corrected in Supabase SQL Editor to remove the `AND deleted_at IS NULL` clause from `WITH CHECK`.

## Root Cause
Supabase PostgREST maintains a metadata/schema cache. Updating a policy via SQL Editor updates PostgreSQL, but PostgREST instances behind the load balancer can serve stale cached policy definitions to the REST API. `NOTIFY pgrst` did not reliably flush all instances. The APK's `.update()` calls were hitting a cached version of the `children_update` policy that still contained the old `deleted_at IS NULL` restriction in `WITH CHECK`, causing the row to violate its own new `deleted_at = NOW()` value.

## Verification Steps
- `pg_policies` confirmed `children_update` has correct `USING (parent_id = auth.uid())` and `WITH CHECK (parent_id = auth.uid())`.
- Manual SQL Editor `UPDATE` on the same row succeeded.
- PL/pgSQL impersonation block (setting `request.jwt.claim.sub` to parent UUID) succeeded, proving the DB-level policy is correct.
- Triggers `children_bmi_trigger` and `children_updated_at` were audited — safe, no `deleted_at` interference.

## Solution: RPC Bypass
Created `soft_delete_child(child_id UUID)` as `SECURITY DEFINER`:
- Bypasses PostgREST table-update path by calling `.rpc()` instead of `.from().update()`.
- Still enforces ownership with an internal `SELECT 1 FROM children WHERE id = child_id AND parent_id = auth.uid() AND deleted_at IS NULL` check before updating.
- Raises `Child not found or not authorized` if ownership fails.

## Files Changed
- `lib/api.ts` — `deleteChild()` switched from `supabase.from('children').update(...)` to `supabase.rpc('soft_delete_child', { child_id: childId })`.
- `database/migrations/20260507_soft_delete_child_rpc.sql` — migration DDL for the RPC function.
- `database/schema.sql` — updated source-of-truth DDL.

## Deployment Steps
1. Execute migration in Supabase SQL Editor.
2. Rebuild APK: `./gradlew assembleRelease`.
3. Install to device via `adb install -r`.

## Build Artifact
- APK path: `~/local-projects/smart-parenting-app/android/app/build/outputs/apk/release/app-release.apk`
- Installed to: `192.168.1.15:41095`

## Additional User-Reported Note
The operational handoff also states that the Supabase Edge Function model was changed to `baidu/cobuddy:free`.
