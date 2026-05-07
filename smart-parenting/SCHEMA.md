# Wiki Schema

## Domain
Smart Parenting mobile application — Expo SDK 55 + Supabase backend. Covers architecture, screen walkthroughs, feature implementations, design system, and development logs.

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `database-schema.md`)
- Every wiki page starts with YAML frontmatter
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per concept page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- Provenance markers: append `^[raw/changelog-2026-04-25.md]` at the end of paragraphs whose claims come from a specific source

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary | raw
tags: [from taxonomy below]
sources: [raw/feature-name.md]
confidence: high | medium | low   # optional
---
```

### raw/ Frontmatter
```yaml
---
ingested: YYYY-MM-DD
sha256: <optional>
---
```

## Tag Taxonomy
- **Architecture:** `architecture`, `database`, `repo-structure`, `navigation`
- **Screens:** `screen`, `dashboard`, `activities`, `history`, `settings`, `auth`
- **Features:** `feature`, `ai-insights`, `notifications`, `schedule`
- **Engineering:** `state-management`, `component`, `security`, `rls`, `supabase`, `expo`
- **Domain:** `ui-ux`, `design-system`, `bmi`, `who-guidelines`
- **Meta:** `changelog`, `panelist`, `technical-reference`

Rule: every tag on a page must appear in this taxonomy. Add new tags here first.

## Page Thresholds
- **Create a page** when a concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details, or things outside the domain
- **Split a page** when it exceeds ~200 lines
- **Archive** superseded content to `_archive/`

## Update Policy
When new information conflicts with existing content:
1. Check dates — newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark contradiction in frontmatter: `contradictions: [page-name]`
4. Flag for review in the lint report
