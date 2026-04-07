# Workflow: Update Concept

**Trigger:** An existing wiki page needs updating — new information, revised claims, added cross-links.  
**Goal:** Update the page while preserving the edit history and maintaining frontmatter integrity.  
**Prerequisite:** The page exists in `wiki/`. Read `HERMES.md` before starting.  

---

## When to Use This Workflow

- New raw source contradicts an existing wiki claim
- User asks "update the X page with what we learned about Y"
- A `wiki-sweep` flagged the page as needing review
- A session produced new information relevant to an existing page

---

## Types of Updates

### Type A: Additive (new information added, old claims unchanged)

Safe. Append new content, update `updated:` timestamp.

### Type B: Corrective (old claim was wrong, needs revision)

Follow Contradiction Policy if the correction is significant:
1. Archive the current page to `.archived/`
2. Create a revised page with updated claims
3. Link bidirectionally (archived → new, new → archived)

### Type C: Structural (frontmatter only — tags, related, TTL fields)

Safe. Update frontmatter, bump `updated:`.

---

## Steps

### Step 1 — Read the existing page

Open the page, read its full content and frontmatter. Note:
- Current `id:`
- Current `updated:`
- Current `source_refs[]`
- Current `confidence:`

---

### Step 2 — Assess the update type

| Update type | Action |
|---|---|
| A: Additive | Proceed to Step 3 |
| B: Corrective | Archive first → Step 3 |
| C: Structural | Proceed to Step 3 |

**For Type B — Archive the current version:**

```bash
mkdir -p ~/Documents/x1n4te-workstation/wiki/<path>/.archived/
mv ~/Documents/x1n4te-workstation/wiki/<path>/<page>.md \
   ~/Documents/x1n4te-workstation/wiki/<path>/.archived/<page>-$(date +%Y-%m-%d).md
```

Add to the archived file's top:

```yaml
---
status: archived
archived_date: YYYY-MM-DD
superseded_by: ../<page>.md
---
## Archived: YYYY-MM-DD
**Status:** superseded  
**Reason:** <brief explanation of why this was superseded>
**Superseded by:** [](../<page>.md)
```

---

### Step 3 — Make the edit

Edit the page body as needed. When done:

- **Type A/C:** Keep existing `id:` and `created:`. Update `updated:` to today.
- **Type B:** Keep existing `id:`. Update `updated:` to today. Add `supersedes: .archived/<old-file>` to frontmatter.

---

### Step 4 — Update frontmatter

| Field | When to update |
|---|---|
| `updated` | Always — any content change |
| `last_verified` | Only if you re-checked against raw sources |
| `confidence` | Bump if corroboration increased; lower if contradicted |
| `related` | Add new cross-links |
| `tags` | Add new tags |
| `review_after` / `stale_after` | Recalculate if `last_verified` was bumped |

---

### Step 5 — Append to wiki/log.md

```markdown
YYYY-MM-DD | update | <page-title> | <type-of-update>
```

---

### Step 6 — Git commit

```bash
git add wiki/<path>/<page>.md
git add wiki/<path>/.archived/<old-page>-YYYY-MM-DD.md   # if Type B
git add wiki/log.md
git commit -m "update: <page-title> | type: <A|B|C>"
```

---

## Validation

- [ ] `updated:` bumped to today
- [ ] `source_refs[]` still accurate
- [ ] If Type B: archived file exists with correct header
- [ ] `wiki/log.md` appended
- [ ] Git commit created
- [ ] Related pages still link correctly (check `related:` field)

---

## See Also

- `workflows/ingest-source.md` — for adding entirely new sources
- `workflows/wiki-sweep.md` — for sweep-triggered re-verification
- `HERMES.md` — contradiction policy, YAML schema
