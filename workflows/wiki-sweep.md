# Workflow: Wiki Sweep

**Trigger:** On-demand (user asks "run a sweep") or scheduled (weekly cron).  
**Goal:** Find expired entries, attempt re-verification against raw sources, tag or archive accordingly.  
**Prerequisite:** Read `HERMES.md` — know the TTL defaults per category.  

---

## What This Workflow Does

Scans every wiki page, checks `stale_after` and `review_after` against today, and applies the appropriate action:

| Condition | Action |
|---|---|
| `today > stale_after` | Hard flag: `#stale-intel`, `status: stale` |
| `today > review_after` AND newer raw exists for this topic | Re-verify: re-read raw, update claims, bump `last_verified` |
| `today > review_after` AND no newer raw | Soft flag: `#needs-review` |
| `last_verified` > 180 days ago AND no new raw | Escalate: `#stale-intel` |

---

## Steps

### Step 1 — Run the sweep script

```bash
python ~/Documents/x1n4te-workstation/scripts/wiki-sweep.py
```

This produces a report:
```
=== Wiki Sweep Report: YYYY-MM-DD ===
Pages scanned: 47
Flagged #stale-intel: 3
Flagged #needs-review: 5
Re-verified: 2
Archived: 1
Errors: 0
```

---

### Step 2 — Review flagged pages

For each `#stale-intel` flag:
1. Open the page
2. Check `source_refs[]` — do the raw files still exist?
3. If raw files exist and claims are still valid → remove `#stale-intel`, bump `last_verified`, reset TTL
4. If raw files exist but claims are outdated → update claims (Type A update)
5. If raw files are gone or claims are wrong → archive (Type B update)

For each `#needs-review` flag:
1. Open the page
2. Determine: is there new raw source that could re-verify this?
3. If yes → re-read raw, update claims, remove `#needs-review`
4. If no → leave flag, note in `Missing From Startup Context` that new source is needed

---

### Step 3 — Handle archived pages

If a page was archived because it was contradicted:
1. Confirm the new replacement page exists
2. Confirm the archived page has correct `superseded_by:` / `supersedes:` links
3. Confirm the new page has `related:` link back to archived page

---

### Step 4 — Update wiki/log.md

```markdown
YYYY-MM-DD | sweep | scanned: <N> | stale: <X> | verified: <Y> | archived: <Z>
```

---

### Step 5 — Git commit

```bash
git add wiki/
git add wiki/log.md
git commit -m "sweep: scanned <N> pages — <X> stale, <Y> verified, <Z> archived"
```

---

### Step 6 — Report to user

Present the sweep summary:

```
=== Wiki Sweep Complete: YYYY-MM-DD ===

Scanned: <N> pages
#stale-intel flagged: <X> pages
#needs-review flagged: <Y> pages
Re-verified and updated: <Z> pages
Archived: <W> pages

[If X > 0]: Pages needing your attention:
  - wiki/path/page1.md
  - wiki/path/page2.md

[If Y > 0]: Pages that need new sources:
  - wiki/path/page3.md
  - wiki/path/page4.md
```

---

## Running as a Cron Job

Set up a weekly sweep via `mcp_cronjob`:

```bash
# Create the cron job
mcp_cronjob create \
  --name "Weekly wiki sweep" \
  --prompt "Run the wiki-sweep workflow for x1n4te-workstation. Report results to user." \
  --schedule "0 9 * * MON" \
  --skill "wiki-sweep" \
  --deliver "origin"
```

This sends the sweep report to your Telegram every Monday at 9 AM.

---

## Edge Cases

**Sweep finds a page with no `stale_after`:**
- Set `stale_after` to `last_verified + 180 days` (or category default)
- Do not flag — this is a legacy page that predates the TTL schema
- Update `updated:` when the page is next touched

**Sweep finds orphaned pages (no other page links to them):**
- Check if the page should exist (is it a valid topic?)
- If yes: add it to the relevant MOC's reading path
- If no (it's noise): archive it

**Sweep finds a page with no `source_refs[]`:**
- Flag `#needs-review`
- This page was likely created without a corresponding raw source — it needs grounding

---

## Validation

- [ ] Sweep script ran without errors
- [ ] `wiki/log.md` updated with sweep entry
- [ ] Git commit created
- [ ] User report delivered
- [ ] `#stale-intel` pages reviewed within 1 week

---

## See Also

- `scripts/wiki-sweep.py` — the script that automates the scan
- `workflows/update-concept.md` — for re-verification updates
- `HERMES.md` — TTL defaults per category, stale flag rules
