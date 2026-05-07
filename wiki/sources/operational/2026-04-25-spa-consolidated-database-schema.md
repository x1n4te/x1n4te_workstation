---
id: 2026-04-25-spa-consolidated-database-schema
type: operational-source
created: 2026-04-25
updated: 2026-04-25
tags:
  - smart-parenting-app
  - operational
  - database
  - supabase
status: active
project: smart-parenting-app
---

# Smart Parenting App — Consolidated Database Schema

## Context

The app previously kept the base database definition in `database/schema.sql` plus multiple incremental SQL migration files under `database/` and `database/migrations/`. The deployment/handoff goal was to leave `database/` with one runnable `.sql` schema file.

## Changes

- Rebuilt `database/schema.sql` as the single consolidated SQL bootstrap file.
- Folded in the former migration files:
  - `002_add_avatar_url.sql`
  - `002_avatars_bucket.sql`
  - `migration_add_activity_types.sql`
  - `migration_child_settings.sql`
  - `migration_child_routine.sql`
  - `migration_gender.sql`
  - `migration_child_notifications.sql`
  - `migration_scheduled_activities.sql`
  - `migration_scheduled_activities_v2.sql`
  - `migration_scheduled_activities_v3.sql`
  - `migrations/001_add_insight_type_and_trend.sql`
- Preserved Supabase RLS for `children`, `activities`, `recommendations`, `alerts`, and `scheduled_activities`.
- Preserved child soft-delete scoping via `deleted_at IS NULL` in child-scoped policies.
- Preserved avatar storage bucket setup and replaced the prior broad storage policies with owner-aware `avatars_*` policies using `public.is_owned_avatar_object(name)`.
- Renamed optional development seed data to `database/seed_test_account.sql.template` so `database/schema.sql` is the only `.sql` file in `database/`.
- Sanitized the seed template to use `YOUR_USER_UUID` and parent-created development credentials instead of concrete local test credentials.
- Placed comments for migrated columns after compatibility `ADD COLUMN IF NOT EXISTS` guards so rerunning on older partial databases does not fail before columns exist.
- Updated README/database setup references and the test-user helper references to the template seed file.

## Verification

- `search_files('*.sql', database)` returned only `database/schema.sql`.
- Static schema coverage check confirmed all migrated tables/columns/constraints/policies/storage objects are present.
- Policy count check: 4 policies each for `children`, `activities`, `recommendations`, `alerts`, `scheduled_activities`, and `storage.objects`.
- `git diff --check -- database/schema.sql database/seed_test_account.sql.template README.md scripts/create_test_user.js` passed.
- `node --check scripts/create_test_user.js` passed.
- `npx tsc --noEmit --pretty false` passed.

## Notes

- `database/schema.sql` is intended for a fresh Supabase project but includes compatibility guards (`IF NOT EXISTS`, constraint recreation, idempotent policy drops) for older partial database states.
- No Supabase RLS weakening was intentional; service-role Edge Function bypass behavior remains unchanged and outside this schema consolidation.
