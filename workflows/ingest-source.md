# Workflow: Ingest Source

**Trigger:** A new file has been added to `raw/`.  
**Goal:** Read the raw source, synthesize wiki pages from it, update index and log.  
**Prerequisite:** The raw file is confirmed immutable (was ingested via `raw-ingest`).  

---

## When to Use This Workflow

- User drops a new PDF, paper, article, or notes into `raw/`
- User asks "ingest this source"
- `raw-ingest` alias completed successfully

---

## Steps

### Step 1 — Verify the raw file exists

```bash
ls -la ~/Documents/x1n4te-workstation/raw/<category>/
# Confirm the file is present and owned by your user (not root)
```

Do NOT proceed if the file is owned by root.

---

### Step 2 — Read the source

Read the raw file in its entirety. For PDFs, extract text first:

```bash
pdftotext ~/Documents/x1n4te-workstation/raw/<category>/<filename>.pdf -
# or
python -c "import pypdf; ..."
```

For markdown, text, or code files: read directly.

---

### Step 3 — Determine page type and category

Ask: What is the **primary contribution** of this source?

| If the source is... | Create this page type |
|---|---|
| Paper, article, report | `wiki/sources/<category>/<slug>.md` |
| Tool or product | `wiki/entities/<slug>.md` |
| Concept, theory, pattern | `wiki/concepts/<slug>.md` |
| Cross-cutting synthesis | `wiki/analyses/<slug>.md` |
| Thematic hub | `wiki/mocs/<category>.md` |

---

### Step 4 — Create the wiki source page

Create a new file at the appropriate path. Use YAML frontmatter:

```yaml
---
id: <slug>-001
type: source
title: "<Full Title>"
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_verified: YYYY-MM-DD
review_after: YYYY-MM-DD   # today + 90 days (or category TTL)
stale_after: YYYY-MM-DD    # today + 180 days
confidence: high           # assess: high / medium / low
source_refs:
  - raw/<category>/<filename>
status: active
tags: []
related: []
---
```

**In the body, include:**

1. **Summary** (2-3 paragraphs) — What is this source about? What are the key claims?
2. **Key Facts** — Bullet list of specific claims, numbers, dates, entities
3. **Notable Claims** — Any claims that contradict existing wiki pages (flag these)
4. **Open Questions** — Things the source doesn't answer
5. **Related** — Internal wiki links to connected concepts, entities, analyses

---

### Step 5 — Update existing pages

If the source touches existing wiki topics:

1. Open each relevant existing page
2. Add the new source to `source_refs[]`
3. If it **contradicts** existing claims → follow the Contradiction Policy
4. If it **strengthens** existing claims → note in body, bump `confidence` if warranted

---

### Step 6 — Update wiki/index.md

Add the new page to the catalog. Append to the relevant section:

```markdown
- **YYYY-MM-DD** | `<page-title>` | `<type>` | `<category>`
```

---

### Step 7 — Append to wiki/log.md

```markdown
YYYY-MM-DD | ingest | <filename-or-title> → <N> wiki page(s) created
```

---

### Step 8 — Git commit

```bash
git add raw/<category>/<filename>
git add wiki/sources/<category>/<slug>.md
git add wiki/index.md wiki/log.md
git commit -m "ingest: <filename> → <slug>.md"
```

---

## Validation

- [ ] Source page created with correct frontmatter
- [ ] `source_refs` points to the raw file
- [ ] `wiki/index.md` updated
- [ ] `wiki/log.md` appended
- [ ] Git commit created
- [ ] No `#needs-review` flags set (unless new raw is sparse)

---

## Edge Cases

**If the source is massive (> 50K tokens):**
Break it into chunks. Create one source page per chunk, all pointing to the same raw file. Use `source_refs: [raw/...]` on each.

**If the source contradicts multiple existing pages:**
Archive each contradicted page (per Contradiction Policy). Create new pages. Don't modify the old pages — archive them.

**If the source has no clear category:**
Create it in the most relevant existing category. If no category fits, create a new one — then update `HERMES.md` directory structure to reflect it.

---

## See Also

- `workflows/update-concept.md` — for updating existing pages post-ingest
- `workflows/wiki-sweep.md` — for periodic re-verification
- `HERMES.md` — raw/ contract, YAML schema, contradiction policy
