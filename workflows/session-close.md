# Workflow: Session Close

**Trigger:** End of every work session — user says "that's all" or indicates they are done.  
**Goal:** Document the session, update the handoff state, and ensure the next session can start without re-explanation.  
**Prerequisite:** `sessions/session-template.md` exists. Read `HERMES.md` §Session Close Protocol first.  

---

## Hard Rule

**Do NOT spin down until ALL steps below are complete.**

If you attempt to close a session with an empty `Decisions Made` section, you MUST warn the user:
```
⚠️ No decisions recorded. Did you forget to document outcomes?
```

Only proceed after filling in all required sections.

---

## Steps

### Step 1 — Create or update the session file

Sessions are stored at `sessions/YYYY-MM-DD.md`.

If a session file for today already exists (multiple conversations in one day):
- Append to the existing file as a new section
- Keep the same frontmatter, add a second `## Session` block

If no session file exists for today:
- Copy `sessions/session-template.md` to `sessions/YYYY-MM-DD.md`
- Fill in `date:`, `started:`, `ended:`, `tools_used:`, `files_changed:`, `related:`

---

### Step 2 — Fill in Required Sections

Every section below MUST be completed before spin-down.

#### Summary (REQUIRED — 3 sentences max)

What happened. What was decided. What is the current state.

Example:
> "Completed Phase 1 vault skeleton — HERMES.md written, 5 workflow files created, and session template set up. Decided on chattr +i enforcement for raw/ and raw-ingest alias for safe file addition. Vault is now operational; next session begins Phase 2 with AI-2027 ingest."

#### Decisions Made (REQUIRED — at least one row)

| Decision | Rationale | Affected Pages |
|---|---|---|
| Chose chattr +i over FUSE mount for raw/ enforcement | Simpler, no Drive dependency | raw/ setup |
| raw-ingest alias drops immutable bit, copies, re-locks | Required because root owns raw/ | ~/.zshrc |

If no decisions were made this session, write:
> "No substantive decisions made this session."

#### State After Session (REQUIRED)

What is currently running, configured, or in progress.

```markdown
## State After Session

- Vault skeleton: COMPLETE
- HERMES.md: written (396 lines, ~3,400 tokens)
- Workflows: 5/5 written
- Scripts: pending (Phase 1.6)
- Phase 1: 80% complete
- Phase 2: Ready to start
```

#### Known Issues / Warnings (REQUIRED — can be empty)

| Issue | Severity | Notes |
|---|---|---|
| raw-ingest alias requires sudo each time | Low | Expected behavior, not a bug |
| Vault has no content yet (empty) | Medium | Phase 2 fills it |

#### Next Steps (REQUIRED — at least one item)

For the next session to pick up:

- [ ] Phase 1.6: Write `scripts/token-budget.py`, `scripts/wiki-sweep.py`, `scripts/wipe-and-recompile.py`
- [ ] Phase 2: Ingest AI-2027.pdf — first real source
- [ ] Create symlink: `raw/software-dev/wims-bfp/thesis/` → `~/workspace-dev/wims-bfp-docs/`

#### Missing From Startup Context (REQUIRED)

Things you had to look up or ask about during this session that should have been pre-loaded next time:

- [ ] The exact path to the vault (`~/Documents/x1n4te-workstation/`)
- [ ] The git remote URL for the vault repo

---

### Step 3 — Fill in Stats

| Metric | Value |
|---|---|
| Session duration | ~45 minutes |
| Wiki pages created | 6 (1 template + 5 workflows) |
| Wiki pages updated | 0 |
| Sources ingested | 0 |
| Tokens spent (est.) | ~X,XXX |
| Git commits | 4 (skeleton, HERMES.md, session template, workflows) |

---

### Step 4 — Update sessions/last-session.md

This is a symlink/copy that always points to the most recent session:

```bash
cp ~/Documents/x1n4te-workstation/sessions/YYYY-MM-DD.md \
   ~/Documents/x1n4te-workstation/sessions/last-session.md
```

---

### Step 5 — Update wiki/log.md

```markdown
YYYY-MM-DD | session | Phase 1 complete | 6 files created | <N> commits
```

---

### Step 6 — Git commit the session

```bash
git add sessions/YYYY-MM-DD.md sessions/last-session.md
git add wiki/log.md
git commit -m "session: YYYY-MM-DD — Phase 1 vault skeleton complete"
```

---

### Step 7 — Report to user

Before spinning down, give the user a summary:

```
=== Session Close: 2026-04-07 ===

SUMMARY:
Phase 1 vault skeleton complete. HERMES.md, 5 workflows, session template written.

NEXT STEPS:
1. Phase 1.6 — scripts (token-budget, wiki-sweep, wipe-and-recompile)
2. Phase 2 — Ingest AI-2027.pdf as first real source
3. Create thesis symlink in raw/

STATE: Vault is operational. Ready for Phase 2.

Git: 4 commits on master
```

---

## Validation Checklist

- [ ] Session file created with all sections filled
- [ ] `Decisions Made` has at least one entry (or "no decisions" note)
- [ ] `Next Steps` has at least one actionable item
- [ ] `sessions/last-session.md` updated
- [ ] `wiki/log.md` appended
- [ ] Git commit created
- [ ] User received session close report

---

## See Also

- `sessions/session-template.md` — the template this workflow fills
- `workflows/ingest-source.md` — typically the first workflow run in a new session
- `HERMES.md` — Session Close Protocol (hard rule)
