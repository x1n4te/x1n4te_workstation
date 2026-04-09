# HERMES.md — Vault Constitution

**Vault:** x1n4te-workstation  
**Location:** `~/Documents/x1n4te-workstation/`  
**Last updated:** 2026-04-07  
**Version:** 1.0

---

## Purpose

This vault is a compounding personal knowledge base built on the LLM Wiki pattern (Karpathy, 2026). It is a structured, interlinked collection of markdown files that grows richer with every interaction. The AI agent (Hermes) reads raw sources, synthesizes wiki pages, maintains cross-links, and flags stale content. The human (xynate) sources, questions, and decides.

**The vault is not a folder of notes. It is a living knowledge artifact that compound compounds on itself.**

---

## Directory Structure

```
x1n4te-workstation/
├── HERMES.md                   ← THIS FILE — vault constitution
├── .gitignore
├── raw/                        ← IMMUTABLE source documents (see §raw-contract)
│   ├── ai-research/
│   ├── cybersecurity/
│   ├── software-dev/
│   └── biomechanics/
├── wiki/                       ← LLM-maintained synthesis layer
│   ├── index.md                ← top-level catalog (auto-updated)
│   ├── log.md                  ← append-only activity log
│   ├── overview-state-of-field.md
│   ├── mocs/                   ← Maps of Content (thematic reading paths)
│   ├── sources/                ← source summaries, organized by category
│   │   ├── ai-research/
│   │   ├── cybersecurity/
│   │   ├── software-dev/
│   │   └── biomechanics/
│   ├── concepts/               ← ideas, theories, patterns
│   ├── entities/               ← people, orgs, products, roles
│   ├── analyses/               ← syntheses, comparisons, cross-category
│   └── sessions/               ← session log files
├── workflows/                  ← task playbooks (authoritative)
│   ├── ingest-source.md
│   ├── update-concept.md
│   ├── full-compile.md
│   ├── wiki-sweep.md
│   └── session-close.md
├── sessions/                   ← per-session state documents
│   └── YYYY-MM-DD.md           ← one per session
├── scripts/                    ← operational scripts
│   ├── token-budget.py
│   ├── wipe-and-recompile.py
│   └── wiki-sweep.py
└── conflict-queue/              ← collision artifacts (agent does NOT auto-resolve)
```

---

## raw/ Contract (IMmutable Source Layer)

**The most important rule in this vault:**

`raw/` is **immutable**. No agent, no process, no user may write to, modify, or delete any file inside `raw/` after ingestion.

### Why this matters

- `raw/` is the **source of truth**. Every wiki page is derived from it.
- `wipe-and-recompile.py` must **never** touch `raw/`.
- If you suspect vault corruption, wipe `wiki/` and re-compile from `raw/`. `raw/` is never wiped.
- Your thesis `.qmd` files live in `raw/software-dev/wims-bfp/thesis/` — they are the canonical source, never overwritten.

### OS-level enforcement

```bash
# raw/ is owned by root, mode 555, immutable bit set
ls -la ~/Documents/x1n4te-workstation/raw/
# → dr-xr-xr-x root root 4096 Apr  7 10:26 raw/

sudo chattr +i ~/Documents/x1n4te-workstation/raw
# Verify:
sudo lsattr ~/Documents/x1n4te-workstation/raw
# → ----i───────── raw/
```

### Adding files to raw/

Use the `raw-ingest` alias (defined in `~/.zshrc`):

```bash
# Add a PDF to ai-research
raw-ingest ~/Downloads/attention-is-all-you-need.pdf \
  -c ai-research \
  -m "ingest: Vaswani et al. Attention paper"

# Add thesis chapter
raw-ingest ~/thesis/chapter3-methodology.qmd \
  -c software-dev/wims-bfp \
  -m "ingest: WIMS-BFP Chapter 3 draft"
```

The alias: unlocks `raw/` (requires sudo), copies file(s), re-locks `raw/`, git-commits. You are prompted for confirmation before unlocking.

---

## Filename Conventions

| Type          | Format                           | Example                                 |
| ------------- | -------------------------------- | --------------------------------------- |
| Wiki page     | `kebab-case.md`                  | `suricata-pipeline.md`                  |
| Source page   | mirrors raw/ path                | `ai-research/ai-2027.md`                |
| Session file  | `YYYY-MM-DD.md`                  | `2026-04-07.md`                         |
| Raw note      | `YYYY-MM-DD-topic.md`            | `2026-04-07-attention-mechanism.md`     |
| Archived page | `*.archived/YYYY-MM-DD-title.md` | `suricata-rules.archived/2026-03-15.md` |

---

## YAML Frontmatter Schema

Every wiki page **must** have this frontmatter:

```yaml
---
id: suricata-eve-json-analysis-001   # deterministic UID (slug + hash)
type: analysis                         # source | concept | entity | analysis | MOC
created: 2026-03-15
updated: 2026-04-02
last_verified: 2026-04-06
review_after: 2026-07-06              # last_verified + 90 days
stale_after: 2026-10-06              # last_verified + 180 days
confidence: high                      # high | medium | low
source_refs:                           # links to raw sources backing this page
  - raw/suricata/eve-json-spec.md
  - raw/suricata/et-open-rules-2026.md
status: active                         # active | archived | under_review | stale
tags:
  - suricata
  - detection-engine
related:
  - concepts/suricata-pipeline
  - entities/et-open
---
```

### Field semantics

| Field | Purpose | Who sets it |
|---|---|---|
| `id` | Unique page identifier | Agent on creation |
| `type` | Page taxonomy | Agent on creation |
| `created` | Birth date | Agent on creation |
| `updated` | Last substantive change | Agent bumps on content edit |
| `last_verified` | Last cross-check against raw/ | Agent on verify/sweep |
| `review_after` | Soft TTL (90 days default) | Agent calculates |
| `stale_after` | Hard TTL → `#stale-intel` auto-tag | Agent calculates |
| `confidence` | Reliability of claims | Agent assesses on creation |
| `source_refs` | Raw sources for this page | Agent populates on ingest |
| `status` | Lifecycle: active / archived / under_review / stale | Agent transitions |
| `tags` | Obsidian tag search | Agent or user |
| `related` | Cross-links to other wiki pages | Agent maintains |

### TTL defaults by category

| Category | `review_after` | `stale_after` |
|---|---|---|
| AI Research | 30 days | 90 days |
| Cybersecurity (threat intel) | 7 days | 21 days |
| Cybersecurity (architecture) | 90 days | 180 days |
| Software Dev | 60 days | 120 days |
| Biomechanics | 60 days | 180 days |

---

## Page Types

| Type | What it holds | Example |
|---|---|---|
| `source` | Summary of a raw source document | `wiki/sources/ai-research/ai-2027.md` |
| `concept` | Ideas, theories, patterns | `wiki/concepts/rlm-wiki-pattern.md` |
| `entity` | People, orgs, products, roles | `wiki/entities/national-validator.md` |
| `analysis` | Syntheses, comparisons, cross-category | `wiki/analyses/wims-bfp-threat-pipeline.md` |
| `MOC` | Thematic hub with reading path | `wiki/mocs/ai-research.md` |

---

## Token Budget Policy

**Init budget:** HERMES.md + index.md + log.md (last 20) + last session ≤ **50,000 tokens**.

```bash
# Measure at start of each session
python ~/Documents/x1n4te-workstation/scripts/token-budget.py
```

If init exceeds 40,000 tokens → warning. If init exceeds 50,000 tokens:
- Truncate `wiki/log.md` to last 5 entries
- Skip `sessions/` deep reads
- Report to user: "Vault init at 62K tokens — consider archiving old sessions"

---

## Session Open Protocol (Required — Every Session)

Before any work begins, the agent MUST read in this order:

```
1. HERMES.md                          ← vault primer (this file)
2. wiki/index.md                     ← what pages exist (compact listing)
3. wiki/log.md (last 20 entries)     ← what changed recently
4. sessions/last-session.md          ← Decisions Made + Next Steps handoff
5. Missing From Startup Context       ← last session's feedback loop items
```

After reading: report token budget status to user.

---

## Session Close Protocol (Required — Before Spin-down)

The agent MUST complete ALL steps before spinning down:

```
1. Update sessions/<YYYY-MM-DD>.md
   ✓ Fill in Summary (3 sentences)
   ✓ Fill in Decisions Made (with rationale)
   ✓ Fill in Next Steps (explicit, actionable)
   ✓ Fill in Known Issues (deferred problems, explicitly flagged)
   ✓ Fill in Missing From Startup Context (what I wished I had known)

2. EMPTY CHECK
   ✗ If Decisions Made is EMPTY → abort spin-down, warn user
     "⚠️ No decisions recorded. Did you forget to document outcomes?"

3. Git commit the session file
   git add sessions/<YYYY-MM-DD>.md
   git commit -m "session: <date>"

4. Report session summary to user before exiting
```

---

## Wiki Sweep Protocol

Run on-demand or weekly (via `mcp_cronjob`):

```bash
python ~/Documents/x1n4te-workstation/scripts/wiki-sweep.py
```

**What it does:**

| Condition | Action |
|---|---|
| `today > stale_after` | Hard flag: append `#stale-intel`, set `status: stale` |
| `today > review_after` AND newer raw exists | Re-verify: re-read raw, update claims, bump `last_verified` |
| `today > review_after` AND no newer raw | Soft flag: append `#needs-review` |
| `last_verified` > 6 months old with no new raw | Escalate: append `#stale-intel` |

---

## Collision Handling

**If agent and user edit the same wiki page simultaneously:**

1. Agent reads file → computes MD5 hash
2. Agent writes → compares hash before write
3. If hash mismatch → agent does NOT overwrite
4. Agent writes to `conflict-queue/<page>-<timestamp>.md` instead
5. User resolves in Obsidian manually
6. Next sweep clears resolved conflicts

**Rule:** Agent never forcibly overwrites a user-modified file.

---

## Contradiction Policy

When new raw data contradicts an existing wiki claim:

```
1. Archive the old page
   old page → wiki/<path>/.archived/<page>-<date>.md

2. Create new page with updated claims
   new page → wiki/<path>/<page>.md

3. In archived page header:
   ## Archived: YYYY-MM-DD
   Status: superseded
   Superseded by: ../<new-page>.md
   Reason: <brief explanation>

4. In new page:
   ## Historical Context
   Supersedes: .archived/<old-page>.md

5. Git commit both transitions
```

**Never delete.** Archived pages are audit trail. They answer "what did we think before?"

---

## Git Policy

| Who | What | When |
|---|---|---|
| Agent | Auto-commit after ingest, lint, sweep | After each operation |
| User | Manual commit for Obsidian edits | When ready |
| User | Commits for raw/ additions | Via `raw-ingest` alias |

```bash
# Agent auto-commits use this format:
git commit -m "ingest: ai-2027.pdf → 6 wiki pages"
git commit -m "lint: updated 3 pages, flagged #stale-intel"
git commit -m "sweep: 2 stale, 1 verified, 3 archived"
git commit -m "session: 2026-04-07 decisions"
```

---

## Personal Context (Who This Vault Serves)

**Owner:** xynate (x1n4te)  
**Role:** BSIT Cybersecurity 3rd year, FEU-TECH — Thesis: WIMS-BFP  
**Thesis:** "WIMS-BFP: A Secure Web Incident Monitoring System with AI-Assisted Threat Detection for Cybersecurity-Specific Forensics-Driven Analysis in the Bureau of Fire Protection"  
**AI focus:** Local Qwen2.5-3B SLM for XAI on Suricata IDS logs

### Active projects

| Project | Category | Status |
|---|---|---|
| WIMS-BFP | Software Dev / Cybersecurity | Active — thesis year |
| Suricata-Celery pipeline | Cybersecurity (Blue Team) | Active |
| LLM Wiki vault (this) | AI Research / Ops | Active — building |
| Threat-Intel-SIEM-Lite | Cybersecurity | Active |

### FRS Roles (for WIMS-BFP authorization)

These are the only valid role literals in any authorization logic:

```
CIVILIAN_REPORTER
REGIONAL_ENCODER
NATIONAL_VALIDATOR
NATIONAL_ANALYST
SYSTEM_ADMIN
```

No aliases. No shorthand. No implicit role mapping.

### Key frameworks referenced

- **RLS (Row Level Security)** — PostgreSQL; enforced via `wims.current_user_id` context
- **MITRE ATT&CK** — threat actor TTPs, used in threat-hunting
- **NIST Cybersecurity Framework** — cited in thesis
- **FRS** — Functional Requirements Specifications for WIMS-BFP

---

## Workflow Reference

| Workflow | Trigger | Location |
|---|---|---|
| Ingest new source | File added to raw/ | `workflows/ingest-source.md` |
| Update existing page | On-demand | `workflows/update-concept.md` |
| Full vault re-compile | Post wipe-and-recompile | `workflows/full-compile.md` |
| Sweep expired entries | On-demand / weekly | `workflows/wiki-sweep.md` |
| Session close | Every session end | `workflows/session-close.md` |

---

## Scripts Reference

| Script | Purpose | Usage |
|---|---|---|
| `scripts/token-budget.py` | Measure vault init token cost | Run each session start |
| `scripts/wipe-and-recompile.py` | Nuclear reset of wiki/ | Only when degraded; NEVER touches raw/ |
| `scripts/wiki-sweep.py` | Find + flag expired entries | Weekly or on-demand |

---

## Hard Rules Summary

1. **raw/ is immutable.** `chattr +i` is set. `raw-ingest` alias is the only write path.
2. **Thesis files are ground truth.** Live in `raw/`, never in `wiki/`. Never overwritten.
3. **wipe-and-recompile.py NEVER touches raw/.** Explicit path whitelist enforces this.
4. **Decisions Made required before spin-down.** Empty = abort.
5. **Never delete wiki pages.** Always archive to `.archived/`.
6. **Git commit after every agent operation.** Ingest, lint, sweep, session.
7. **Token budget checked each session.** Init > 50K tokens = truncate and warn.

---

*This file is the vault constitution. It is loaded at the start of every session. When this file is updated, the new version takes effect immediately.*
