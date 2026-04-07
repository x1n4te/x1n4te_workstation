# Workflow: Full Compile

**Trigger:** `wipe-and-recompile.py` has been run, or user requests a full re-build of the wiki from raw sources.  
**Goal:** Regenerate all wiki pages exclusively from the immutable raw/ layer.  
**Prerequisite:** `wipe-and-recompile.py` completed successfully and wiki/ skeleton is empty.  

---

## Warning

This workflow takes a long time if raw/ has many sources. It should only be run:
- After `wipe-and-recompile.py` — to rebuild from a clean slate
- Annually or semi-annually — to refresh synthesis from accumulated raw sources

For incremental updates, use `ingest-source.md` instead.

---

## Before You Start

1. Confirm `wiki/` is empty (skeleton only):
```bash
ls ~/Documents/x1n4te-workstation/wiki/
# Expected: index.md log.md mocs/ sources/ concepts/ entities/ analyses/ sessions/
```

2. Confirm `raw/` has content:
```bash
find ~/Documents/x1n4te-workstation/raw/ -type f | wc -l
```

3. Set a session timer — expect this to take multiple hours if raw/ has 100+ files.

---

## Steps

### Phase A: Pre-compile survey

#### Step A1 — Enumerate all raw sources

```bash
find ~/Documents/x1n4te-workstation/raw/ -type f \
  -not -path "*/.git/*" \
  -not -path "*/.archived/*" \
  | sort
```

List all files. Group by category.

#### Step A2 — Read each raw source

For each file in `raw/`:
- Extract content (use `pdftotext` for PDFs)
- Make notes: key claims, entities, contradictions, open questions
- Determine: does a wiki page for this topic already exist?

#### Step A3 — Read existing archived wiki pages

Before wiping, the backup at `wiki.backup.<timestamp>/` may contain pages worth restoring. Check:
- Were any pages in `.archived/` directories?
- Any pages with `confidence: high` that should be rebuilt?

---

### Phase B: Compile

Process raw sources in this order (most foundational first):

```
1. Entities (people, orgs, products, roles) — other pages depend on these
2. Concepts (theories, patterns) — cross-link to entities
3. Sources (per-category) — cite entities and concepts
4. Analyses (cross-category syntheses) — depend on all of the above
5. MOCs (Maps of Content) — reading paths through the above
```

#### For each raw source, create or update:

1. **Entity page** if the source is about a person/org/product/role
2. **Concept page** if the source introduces a theory or pattern
3. **Source page** with `source_refs: [raw/path/to/file]`
4. **Analysis page** if the source bridges multiple categories

#### Cross-linking rules:

- Every source page MUST link to at least 1 entity or concept
- Every concept page MUST link to at least 2 other concepts or entities
- Every analysis page MUST link to at least 2 source pages from different categories
- Use `related:` in frontmatter AND body wikilinks (`[[page]]`)

---

### Phase C: Build MOCs

After all source/concept/entity pages exist:

1. Read `wiki/sources/` directory structure
2. Create one MOC per category:
   - `wiki/mocs/ai-research.md`
   - `wiki/mocs/cybersecurity.md`
   - `wiki/mocs/software-dev.md`
   - `wiki/mocs/biomechanics.md`
3. Each MOC should list:
   - Overview of the category
   - Key entities (with links)
   - Key concepts (with links)
   - Key source pages (with links)
   - Recommended reading order
   - Open questions / gaps

---

### Phase D: Build overview-state-of-field.md

If this is a re-compile (not first build), read the previous `overview-state-of-field.md` from the backup. Note what changed.

Create a new `wiki/overview-state-of-field.md` that:
- Describes the current state of each category
- Notes major changes since the last compile
- Identifies gaps (topics with no wiki page yet)
- Lists questions that need new raw sources to answer

---

### Phase E: Finalize

#### Step E1 — Update wiki/index.md

Regenerate the full catalog listing every page.

#### Step E2 — Update wiki/log.md

```markdown
YYYY-MM-DD | full-compile | Rebuilt wiki from raw/ | <N> pages created | <M> raw sources processed
```

#### Step E3 — Git commit

```bash
git add wiki/
git commit -m "full-compile: rebuilt wiki from raw/ — <N> pages, <M> sources"
```

---

## Validation Checklist

- [ ] Every raw source has at least one corresponding wiki page
- [ ] Every wiki page has `source_refs[]` pointing to at least one raw file
- [ ] Every MOC links to at least 3 pages in its category
- [ ] `wiki/index.md` lists all created pages
- [ ] `wiki/log.md` has the full-compile entry
- [ ] No orphaned wiki pages (page with no references to it)
- [ ] Git history shows the full-compile commit

---

## Estimated Time

| raw/ size | Estimated time |
|---|---|
| 1–10 files | 30–60 minutes |
| 11–50 files | 2–4 hours |
| 51–200 files | Half day |
| 200+ files | Full day or more |

Start this workflow when you have uninterrupted time.

---

## See Also

- `scripts/wipe-and-recompile.py` — for the wipe step before this workflow
- `workflows/ingest-source.md` — for incremental source addition
- `workflows/wiki-sweep.md` — for periodic maintenance
- `HERMES.md` — YAML schema, TTL defaults
