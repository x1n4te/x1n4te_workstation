# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete

## [2026-04-25] create | Wiki initialized
- Domain: Smart Parenting mobile application (Expo SDK 55 + Supabase)
- Migrated from flat markdown files into structured LLM-wiki
- Created: SCHEMA.md, index.md, log.md
- Created raw/ layer: 8 source files
- Created concepts/ layer: 14 concept pages
- Backed up pre-wiki files to `_pre-wiki-backup/`

## [2026-04-25] update | Added date picker to log mode
- Log mode now has a date selector (same nav row pattern as schedule mode)
- `logDate` state added; passed as `recorded_at` to `logActivity(childId, type, value, logDate)`
- `logActivity()` in api.ts updated to accept optional `date?: Date` parameter
- `screen-activities.md` updated: flow diagram now shows log mode flow, key design decision added

## [2026-04-25] lint | wikilink gate — 8 pages fixed, all 14 now pass
- Pages with <2 wikilinks: screen-history (0), ai-insights-architecture (1), ai-insights-display (1), auth-loading-overlay (1), screen-auth (1), screen-dashboard (1), screen-activities (1), design-system (1)
- Fixed: added contextual wikilinks to each page — no new content added, only cross-reference enrichments
- Verified: index.md and filesystem aligned (14/14)

## [2026-05-01] fix | 12:00 PM bug on all activities — root cause and fix
- **File:** lib/api.ts — removed `toLocalNoonISOString()` and its usage in `logActivity()`
- **Root cause:** `toLocalNoonISOString()` (introduced in commit 4084bd4) forced hour=12, minute=0, second=0 when logging with a selected date. Every `recorded_at` written to Supabase was noon UTC, displayed as 12:00 PM in all timezones.
- **Fix:** `date.toISOString()` now preserves actual wall-clock time while anchoring to the correct calendar date.
- **Impact on existing records:** Already-stored 12:00 PM activities will persist until re-logged; fix prevents new corruptions.
- **Pushed to:** origin/launch-ready (commit 3a82442)
- **Source ref:** [[hci-design-principles-mobile]] (timestamp accuracy)

## [2026-04-25] ingest | April 25 release changelogs and feature docs
- Sources: CHANGELOG.md, ai-insights-improvements.md, notification-system.md, schedule-redirect.md
- Filed into raw/ and synthesized into concepts/
- Cross-linked all concept pages with [[wikilinks]]
