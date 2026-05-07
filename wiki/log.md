# Wiki Log

Append-only activity log. Newest entries first.

**Entries archived:**
- 2026-04-14 and earlier → wiki/log-archives/log-2026-04-16.md
- 2026-04-16 to 2026-04-26 → wiki/log-archives/log-2026-04-26.md

---
**2026-05-07 | ingest | Smart Parenting App RLS stale cache bypass via SECURITY DEFINER RPC**

- Raw source captured: `raw/articles/smart-parenting-app-rls-stale-cache-bypass-2026-05-07.md`
- Created: `sources/operational/2026-05-07-spa-rls-stale-cache-bypass.md`
- Updated: `concepts/smart-parenting-app-tech-stack.md`, `concepts/smart-parenting-app-system-architecture.md`, `index.md`
- Verified in live repo: `lib/api.ts` uses `supabase.rpc('soft_delete_child', { child_id: childId })`; `database/migrations/20260507_soft_delete_child_rpc.sql` and `database/schema.sql` both define the `SECURITY DEFINER` function.
- Verified drift note: live `supabase/functions/analyze-child/index.ts` still defaults to `inclusionai/ling-2.6-1t:free`; user handoff claim of `baidu/cobuddy:free` is recorded as unverified runtime/docs drift.

---
**2026-05-05 | session | Hindsight memory provider set up — Groq GPT OSS 120B, bank hermes-main seeded**

- Hindsight 0.5.3 running in Docker on localhost:8888. LLM: Groq GPT OSS 120B free tier (llama-3.3-70b-versatile). Local embeddings (BAAI/bge-small-en-v1.5) and local reranker (cross-encoder/ms-marco-MiniLM-L-6-v2) built into image. No external embedding provider needed.
- Bank `hermes-main` created with mission, disposition (skepticism=4, literalism=3, empathy=2). 3 directives: security-first, documentation-truth, constitution-ram. CLI and REST API both configured.
- 20 structured facts seeded from WIMS-BFP wiki: PR #94 blockers (data_hash scope + analytics sync), Issue #95 M6-D spec, M5 task assignments to Red (ShibaTheShiba), Pocock audit outcomes (Candidate A reverted, Candidate B merged at 5dcb59f), codebase structure, Docker ritual, Keycloak patterns, auth architecture, public_dmz, IERC status, FRS module index. Groq token burn ~22k per 5-fact batch.
- **Groq API key persistence required:** user must add `export GROQ_API_KEY=...` to `~/.bashrc` or `~/.zshrc` before container restart — without it, container crashes with "LLM API key required."
- WIMS-BFP status: No large-scale refactoring. Red has M5-C/D/E/F. Earl (orljorstin) has PR #94 blockers. Candidate B merged. Candidate A reverted (regional.py stays 3326 LOC monolithic). M6-D correction workflow SPEC filed as GitHub Issue #95.

---

**2026-05-04 | ingest | WIMS-BFP FRS consolidated specification ingested**
|- Raw source: `raw/articles/wims-bfp-frs-consolidated-2026-05-04.md` — full 15-module specification superseding individual module files
|- Updates: `concepts/wims-bfp-frs-modules.md` updated with new modules 14 & 15, revised 5d, and cross-references
|- Index: added new source entry, total pages: 205
|


**2026-05-04 | audit | WIMS-BFP Earl-Branch SPEC audit written**
- Audit against FRS 2026-05-04 (15-module): M1, M3, M4, M5, M12, RLS, Tests
- Verdict: 7/8 compliant, 1 partial (M4.a.iii SHA-256 hash — 4 fields only, not full incident data)
- Must-fix: expand data_hash canonical payload to cover full incident + details tables
- Should-fix: add logger.warning on analytics sync failure (silent pass risk)
- Wiki page: `sources/operational/2026-05-04-wims-bfp-earl-branch-spec-audit.md`; index updated

**2026-05-04 | research | WIMS-BFP FRS modules deep research (M5d, M6–M12, M14–M15)**
- M7 (Suricata IDS): no custom rules in repo, Suricata config file missing, no Lua impossible travel script, no GeoIP2 DB
- M8 (XAI/Qwen2.5-3B): pipeline exists but impossible travel not implemented, no GeoIP2, no documented system prompts
- M9 (Health Dashboard): get_system_health() exists but no wiki page, tsvector/GIN on logs unconfirmed
- M10 (RA 10173): PII encryption + RLS + audit trail covers most controls; ISO 27001 DPIA gap identified
- M11 (Pentest): procedure docs exist; actual pentest report template missing
- M14 (Public DMZ): code exists, no wiki
- M15 (Ref Data Service): code exists, no wiki
- Sources: arXiv Qwen2.5 Tech Report, Suricata docs, privacy.gov.ph, OWASP ASVS
- Page: `raw/articles/wims-bfp-frs-modules-deep-research-2026-05-04.md`; index updated

**2026-05-04 | wiki | WIMS-BFP wiki MOC gap analysis written**
- 13 missing pages identified across 10 categories (analytics, immutable records, admin onboarding, JWT refresh, public DMZ, ref data, scheduled reports, notifications, testing, infra)
- 5 ghost links found (MOC references non-existent pages)
- 3 unlinked existing pages identified
- P0: analytics-read-model, immutable-records, afor-commit-pipeline
- P1: admin-onboarding, keycloak-admin-python, jwt-refresh, national-analyst
- P2: public-dmz, ref-data-service, scheduled-reports
- Gap analysis page: `analyses/wims-bfp-wiki-moc-gap-analysis-2026-05-04.md`; MOC updated

**2026-05-04 | review | WIMS-BFP Earl-Branch ingested to wiki**
- Fetched `origin/Earl-Branch` → local branch; 3 commits ahead of master
- Commits: `c5ce2b9` (analytics sync #84 + immutable records #66), `7d0ea8a` (JWT refresh #93), `570eaed` (admin onboarding #91)
- 10 files changed (+644/-43); new: `17_immutable_records.sql`, `test_immutable_records.py`
- Wiki page: `sources/operational/2026-05-04-wims-bfp-earl-branch-review.md`; index updated

**2026-05-04 | create | WIMS-BFP Ch3 + Ch4 thesis-ready artifacts**
- Produced 3 structured chapter artifacts from ingested sources for Tuesday submission
- Ch3 Research Question Alignment Matrix: fully written with WIMS-BFP-specific objectives, STRIDE mapping, Ch1→Ch3→Ch4 traceability flow, narrative text, implementation notes
- Ch4 System Quality Evaluation Results: 5-category structure (Functional Suitability/Performance/Reliability/Usability/Explainability), all tables with X.XX placeholders, interpretation templates
- Ch4 Security Testing Results: 11 technical test cases (AUTH-001–AVAIL-002), 6-category expert survey, 7-video index, consolidated interpretation table
- Only actual survey data (weighted means) and evidence filenames need filling
- Files: `wims-bfp-ch3-research-question-alignment-matrix-artifact-2026-05-04.md`, `wims-bfp-ch4-system-quality-evaluation-results-artifact-2026-05-04.md`, `wims-bfp-ch4-security-testing-results-artifact-2026-05-04.md`
- Updated handoff with Tuesday deliverables section and updated index.md

**2026-05-04 | ingest | WIMS-BFP secure coding and deployment checklist**
- Secure coding practices: input validation, parameterized queries/ORM, CSRF tokens, centralized auth, secrets in env vars, error handling, dependency scanning, code review
- Secure deployment (cloud/VM/web): server hardening, Nginx security headers (CSP/HSTS/X-Frame-Options), HTTPS enforcement, database security, IAM least privilege, MFA, private subnets, backup/recovery
- Deployment testing before release checklist
- Common deployment mistakes to avoid (9 items)
- Sample Ch3 statement template
- WIMS-BFP-specific alignment table mapping sections to docker-compose.yml, nginx.conf, init-scripts, CI pipeline
- Source: `raw/articles/wims-bfp-secure-coding-deployment-checklist-2026-05-04.md`

**2026-05-04 | ingest | WIMS-BFP enhanced cybersecurity development checklist**
- Advanced technical controls: MFA/OTP, password policy, bot protection, Zero Trust (continuous verification, least privilege, device trust), session security (HttpOnly/Secure/SameSite/JWT rotation), input security (server-side validation, ORM, XSS/CSRF protection), data protection (HSTS, field encryption, secrets management), logging/forensics, availability/resilience, API security, admin hardening, security testing readiness
- 12-section cybersecurity design mindset reminders (default deny, verify all, minimize data, log important actions, encrypt sensitive data, build for recovery)
- WIMS-BFP implementation alignment table: Keycloak RBAC, RLS, JWT refresh, AES-256-GCM PII, audit logs, JMeter load test, security test cases AUTH-001 through AVAIL-001
- Source: `raw/articles/wims-bfp-enhanced-cybersecurity-development-checklist-2026-05-04.md`

**2026-05-04 | ingest | WIMS-BFP system development compliance checklist**
- 11-section development checklist: Legal/Ethical (RA 10173), Requirements/Scope, UI/UX, Functional validation, Data/DB, Security/Cybersecurity controls, Performance/Reliability, AI/Analytics, Testing readiness, Documentation/research alignment, Final defense readiness
- WIMS-BFP-specific alignment mapping to wiki pages for each section
- Companion checklist cross-references to enhanced cybersecurity checklist and secure coding/deployment checklist
- Source: `raw/articles/wims-bfp-system-development-compliance-checklist-2026-05-04.md`

**2026-05-04 | ingest | WIMS-BFP security testing evaluation questionnaire + guidelines**
- Security Testing Evaluation Questionnaire: 30 items across 6 categories (Auth, Input Validation, Logging, Data Protection, Availability, Overall Security), demographics, consent, KPI targets ≥4.00 per category
- Technical testing guidelines: 7 recommended test areas mapped to STRIDE, test case documentation format, 5 sample results (AUTH-001 through AVAIL-001), video documentation requirements (7 required videos), ethical compliance
- Questionnaire alignment: standards cross-reference (NIST CSF, OWASP ASVS, ISO 27001, ISO 25010), qualification criteria for respondents, computation guide (WM formula), validation requirements
- Source: `raw/articles/wims-bfp-security-testing-evaluation-questionnaire-2026-05-04.md`

**2026-05-04 | ingest | WIMS-BFP post-test evaluation questionnaire**
- ISO/IEC 25010 evaluation questionnaire: 30 items across 5 categories (Functional Suitability, Performance Efficiency, Reliability, Usability, Explainability) + optional Security Readiness section
- Demographics, consent form, 5-point Likert scale, open-ended feedback
- Researcher analysis guide: weighted mean interpretation table, Cronbach's Alpha targets, sampling justification, ethical compliance, visual presentation recommendations (bar charts, radar, pie)
- WIMS-BFP category-to-STRIDE mapping for Ch4 results
- Source: `raw/articles/wims-bfp-post-test-evaluation-questionnaire-2026-05-04.md`

**2026-05-04 | ingest | WIMS-BFP authority approval letter template**
- Captured formal permission request letter for controlled security testing (agency/BFP context)
- Includes 7-safeguard ethical commitment list, scope block, schedule fields, authority consent block (approve/approve-with-conditions/deny)
- WIMS-BFP-specific pre-filled fields: research title, institution, RA 10173 reference
- Usage context: pre-testing authorization, IERC evidence, panel appendix
- Source: `raw/articles/wims-bfp-authority-approval-letter-template-2026-05-04.md`

**2026-05-04 | ingest | WIMS-BFP ethical security testing guide**
- Captured ethical security testing procedure: pre-testing prep (5 steps), 5-step execution, dos/don'ts, documentation requirements, student workflow
- Includes Ch3 ethical statement template and panel defense answer template
- WIMS-BFP-specific test scope table mapped to authentication, SQL injection, logging, HTTPS, DoS, AI explainability
- Standards alignment: NIST SP 800-115, OWASP ASVS, ISO 25010, ISO 27001
- Source: `raw/articles/wims-bfp-ethical-security-testing-guide-2026-05-04.md`

**2026-05-04 | ingest | WIMS-BFP expert validation guide**
- Captured expert validation procedure: 7 steps, validator selection criteria (3-min), rating form template, CVI computation, Ch3 sample statement
- Includes full validation request letter template (WIMS-BFP-specific with study objectives)
- Maps questionnaire items to the 6-objective STRIDE matrix (Spoofing/Tampering/Repudiation/Info Disclosure/DoS/Cross-cutting)
- Standards cross-reference: OWASP ASVS, NIST SP 800-115, NIST CSF, ISO 25010, ISO 27001
- Source: `raw/articles/wims-bfp-expert-validation-guide-2026-05-04.md`

**2026-05-04 | ingest | WIMS-BFP research question alignment matrix**
- Captured alignment guide: 6-objective matrix mapping objectives → modules → ISO/IEC 25010 evaluation → STRIDE threats → OWASP ASVS/NIST 800-115 tests → Ch4 evidence
- Includes STRIDE summary table and Ch1→Ch3→Ch4 flow diagram
- Source: `raw/articles/wims-bfp-research-question-alignment-matrix-2026-05-04.md`

**2026-05-04 | ingest | WIMS-BFP full paper structure (outline)**
- Captured user-provided thesis structure: all 6 chapters, preliminaries, bibliography, appendices
- Structural mapping table added linking chapter inputs/outputs
- Source: `raw/articles/wims-bfp-paper-structure-2026-05-04.md`
- Linked from `mocs/wims-bfp.md` and `index.md`

**2026-05-03 | split | WIMS-BFP integration closeout split for wiki page-size discipline**
- Split oversized closeout into compact source page plus detail/archive pages.
- Main: `sources/operational/2026-05-03-wims-bfp-pr78-pr83-integration-closeout.md`.
- Details: `sources/operational/2026-05-03-wims-bfp-pr78-pr83-integration-details.md`.
- Archive: `sources/operational/2026-05-03-wims-bfp-session-handoff-archive.md`.

**2026-05-03 | update | WIMS-BFP session handoff compacted into LLM Wiki**
- Created durable source page: `sources/operational/2026-05-03-wims-bfp-pr78-pr83-integration-closeout.md`.
- Migrated complete PR #78–#83 integration, conflict-resolution, CI/CD, and proactive JWT refresh details out of `.hermes/WIMS-BFP-SESSION-HANDOFF/wims-bfp-session-handoff.md`.
- Compacted session handoff to start-of-session boot state only: repo/wiki paths, verified remote master SHA, live-check commands, current operational state, and context cap protocol.
- Updated `index.md` and `mocs/wims-bfp.md` navigation.

**2026-05-03 | update | SCHEMA tag taxonomy expanded for GitHub operations**
- Added valid tag `github` under Development Practices for GitHub repositories, issues, pull requests, and Actions.

**2026-05-02 | ingestion | WIMS-BFP — orljorstin Implementation Summary**
- Ingested report from orljorstin's agent (Earl Justin P. Camama).
- 6 issues resolved by orljorstin: #42 (user deactivation + Keycloak/Redis), #43 (active session viewer + force logout), #44 (health dashboard), #45 (audit log viewer), #57 (bulk approve), #59 (report status tracker).
- 2 remaining open: "On-Going Fires" dashboard filter bug; concurrent session block reverted.
- Raw source: `raw/articles/wims-bfp-orljorstin-sprint-2026-05-02.md`.
- Updated handoff: `~/.hermes/wims-bfp-session-handoff.md`.

**2026-05-02 | ingestion | WIMS-BFP Team Sprint — Apr 28 – May 2, 2026**
- Fetched all GitHub commits, PRs, branches via gh CLI.
- Identified 4 contributors: x1n4te (41 total), laqqui (3), G10dero (3), ShibaTheShiba (1).
- 2 open PRs: PR #78 (feature/analyst-CRUD, +5258/-2036, 60 files) and PR #79 (feat/module-2-incident-workflow, +4558/-1329, 29 files, checkpoint with 10 deferred items).
- PR #77 (fix/init-auth-fix-no-loop) merged Apr 28.
- Key recent ADRs: strict FRS roles, Keycloak 26.6.0 MFA, conditional OTP, backchannel logout (branch sessionManagement/red).
- Team real names: G10dero + laqqui = Guinevere T. Tendero, orljorstin = Earl Justin P. Camama, ShibaTheShiba = Red Gabrielle A. Dela Cruz.
- Raw source: `raw/articles/wims-bfp-team-sprint-apr-28-may-02-2026.md`.
- Related: `[[sources/wims-bfp-codebase]]`, `[[entities/WIMS-BFP]]`.
- Added History activity actions sheet, edit modal, and delete confirmation modal for logged `activities` records.
- Wired History card trailing action affordance while preserving recorded time labels; update/delete mutations call Supabase helpers and then silently refetch source-of-truth activity data.
- Edit modal uses inline validation and plain RN `TextInput` + `View` wrappers for compact time/date fields; delete uses explicit modal confirmation with loading/error states.
- Verification: `npx tsc --noEmit` passed; `git diff --check` passed; prohibited-pattern searches found no new `Alert.alert`, service-role usage, `@expo/dom-webview`, new `any`, TODOs, or Paper TextInput imports in new History CRUD components.
- Source: `sources/operational/2026-05-01-spa-history-activity-crud-ui`.

**2026-05-01 | session | Smart Parenting App — History activity CRUD phases 1-2**
- Implemented Phase 1 API helpers: `ActivityValue`, narrow `UpdateActivityInput`, `updateActivity()`, and `deleteActivity()` in `lib/api.ts`; typed Supabase client with generated `Database` types.
- Implemented Phase 2 shared activity value utility layer in `lib/activity-values.ts`: option constants, duration/food-group helpers, shared `getActivityLabel()`, and `buildUpdatedActivityValue()` normalizer for the upcoming edit modal.
- Rewired `app/(tabs)/history.tsx` to use shared label/stat helpers and removed local JSONB `any` casts in label/stats paths.
- Verification: `npx tsc --noEmit` passed; `git diff --check` passed; no RLS/schema changes, no `Alert.alert()`, no service-role keys.
- Source: `sources/operational/2026-05-01-spa-history-activity-crud-phase2`.

**2026-04-30 | ingestion | Matt Pocock "How to Fix Any Codebase" — 1 new concept**
- Source: YouTube, ~11 min. Focus: live demo of `improve-codebase-architecture` skill + strategic/tactical framing. Confidence: high.
- **Core thesis:** AI accelerates software entropy; cure is running `improve-codebase-architecture` skill every few days with human strategic judgment.
- **Key new framing:** Agent = tactical programmer (ground-level, fast changes); Human = strategic programmer (aerial view, long-term health, judgment calls).
- **1 new concept page created:** `concepts/strategic-vs-tactical-programming` — the human-as-strategist/agent-as-tactician framework; harness-before-refactoring for legacy codebases.
- **Raw transcript:** `raw/transcripts/matt-pocock-improve-codebase-architecture-2026.md`
- **Glossary terms added:** module, interface, implementation, deep/shallow module, seam, adapter (from hexagonal architecture).
- **Live demo finding:** untested seam across frontend/backend boundary — two parallel implementations must agree but have zero test coverage at the seam.
- **No skill created** — `improve-codebase-architecture` skill already documented (Pocock skills repo, 41.5K stars).
- **Key quote:** "I think of agents as really, really good tactical programmers. They're able to get on the ground and make changes quickly. But they need someone on the level above them who is the strategic programmer."
- **Relevance to WIMS-BFP:** x1n4te as lead architect = strategic programmer role; agents do tactical implementation; strategic/tactical split validates the 4-agent (Orchestrator/Builder/Tester/Critic) architecture as a deliberate separation of strategic intent from tactical execution.
- **Wiki cross-refs updated:** improve-codebase-architecture-skill, deep-modules-ai-navigation.

**2026-04-30 | ingestion | Karpathy "Software 3.0" — AISLE Symposium — 4 new concepts**
- Source: YouTube, ~29 min. AISLE AI Symposium. Fetched via youtube-transcript-api. Confidence: high.
- **Core thesis:** LLMs are a new computing paradigm (Software 3.0) — prompting replaces code, context window is the lever, agents are the runtime.
- **Karpathy's December 2024 inflection:** "stark transition" — agents started outputting correct code without corrections; vibe coding became viable as primary workflow.
- **4 new concept pages created:**
  - `concepts/software-3-llm-computing-paradigm` — 3 eras of software, OpenClaw/menu-genen examples, new opportunities impossible before
  - `concepts/verifiability-agentic-ai` — RL + verification reward hypothesis; jaggedness explained by circuits + data distribution; car-wash walk-vs-drive failure
  - `concepts/vibe-coding-vs-agentic-engineering` — floor-raising (vibe coding) vs ceiling-preserving (agentic engineering); WIMS-BFP requires agentic engineering
  - `concepts/agent-native-infrastructure` — sensors/actuators, "copy-paste to agent" as programming paradigm; everything must be rewritten for agents
- **Raw transcript:** `raw/transcripts/karpathy-software-3-llms-new-computer-2026-04.md`
- **Cross-refs updated:** jagged-frontier-ai-capability, wims-bfp-agentic-workflow, entities/andrej-karpathy
- **Key quotes:**
  - "What is the piece of text to copy-paste to your agent? That's the programming paradigm."
  - "You can outsource your thinking but you can't outsource your understanding."
- **Relevance to WIMS-BFP:** WIMS-BFP's 4-agent workflow (Orchestrator/Builder/Tester/Critic) is an agentic engineering implementation; the verifiability framework explains why certain tasks (code) are automatable and others (taste, judgment) are not.
- **No skill created** — the protocols described (spec-first, agentic QA) are already covered by existing skills.

**2026-04-28 | session | WIMS-BFP — PR #77 review, UUID mismatch diagnosis, PR #78 creation + CI fix**

- **PR #77 review** (`fix/init-auth-fix-no-loop` → `master`, merged as #77): Reviewed 10-file diff. Confirmed root cause: Keycloak JWT `sub` = `715f23c9-1d85-487d-92c8-a75823d3ebdb` (Keycloak-randomized) vs DB seed `keycloak_id` = `11111111-...` (deterministic). Loop fires at `auth.py` fallback guard: `if existing_keycloak_id != JWT sub → 403 identity mismatch`. PR #77 fixes this via `bfp-realm.json` deterministic user IDs + bootstrap ordering + encoder region assignment. **Issues found**: `incident_verification_history` schema incompatibility between `05_`/`06_` migration files (target_type/target_id columns missing from `05_` definition), missing `ALTER TABLE fire_incidents ENABLE ROW LEVEL SECURITY` in new migration, `99_verify_bootstrap.sql` hardcoded `<> 5` but 6 rows exist (svc_suricata). Confirmed by decoding JWT from live session.

- **Keycloak UUID debug protocol**: Decoded JWT `sub` vs `wims.users.keycloak_id` comparison confirmed UUID drift. Fastest diagnostic: `python3 -c "import base64,json,..."` on JWT payload vs `docker compose exec postgres psql -U postgres -d wims -c "SELECT keycloak_id FROM wims.users WHERE username='encoder_test'"`.

- **PR #77 merged to master**: `gh pr merge 77 --admin --merge`. Accidentally merged directly to master (PR base was master, not feature/analyst-CRUD).

- **PR #78 created** (`feature/analyst-CRUD` → `master`): 57 files, +4965/-1817 lines. National Analyst CRUD: dashboard, PostGIS heatmaps, CSV/Excel/PDF exports, Celery beat scheduled reports, self-service profile. 18 commits rebased cleanly on master post-PR-77. Draft state. URL: https://github.com/x1n4te/WIMS-BFP-PROTOTYPE/pull/78

- **PR #78 CI failure + fix**: CI Merge Gate failed despite branch head green. Root cause: GitHub synthetic merge ref (`refs/pull/78/merge`) recontaminated `src/postgres-init/` with stale files from master (`05_validator_workflow.sql`, `06_fix_ivh_legacy.sql`, `99_verify_bootstrap.sql`) and a trailing `\connect wims` in `00_keycloak_bootstrap.sql` pointing to wrong DB (`wims_test` in CI). Fix: `90327fe` + `468833b` — removed bad `\connect`, deleted stale legacy init files. Isolated PostGIS verification passed. Final CI: ALL SUCCESS (Security Audit, Validate Migrations, Frontend, Backend, Docker Build, Merge Gate).

- **Lesson**: When PR-only CI fails but branch head is green → inspect `refs/pull/<PR>/merge` (GitHub's synthetic merge commit). Patched `github-pr-workflow` skill with this addendum.

- **Updated**: wiki log, `.hermes/plans/m1/HANDOFF-M1-INFRA-ISSUES-CLOSED.md` (PR #78 merge-ref CI drift addendum)

**2026-04-26 | ingestion | Matt Pocock "Advanced AI Coding Techniques" — 5 new concepts**
- Source: YouTube, 1h36m workshop. Fetched via youtube-transcript-api. Confidence: high.
- **Created (net-new):**
  - concepts/smart-zone-dumb-zone.md — Dex Hy concept; ~100k threshold; token counter as essential HUD
  - concepts/ralph-wiggum-software-practice.md — named after Simpsons; "small change" loop; contrast with multi-phase plans
  - concepts/sand-castle-parallelization.md — TypeScript lib for parallel Ralph loops; Planner/Implement/Review/Merger architecture
  - concepts/push-pull-coding-standards.md — push/pull decision matrix; coding standards push to reviewer, pull to implementer
  - concepts/improve-codebase-architecture-skill.md — Pocock skill; scan for shallow module candidates; zero-tests discovery
- **Updated:**
  - concepts/design-concept-alignment.md — added session phases model (system prompt → exploratory → implementation → testing → clear); sub-agent token efficiency (93.7k Opus exploration at zero main-session cost)
  - concepts/feedback-loops-ai-coding.md — added doc-rot section (stale PRDs mislead AI); compacting vs clear (prefer clear); QA with human taste (not just gate)
- **Cross-links:** All 5 new pages cross-linked to existing concepts and vice versa
- **Key insight for WIMS-BFP:** Human review gate = taste imposition moment, not just correctness gate

**2026-04-26 | lint | Wiki Quality Audit & Remediation — 196 pages**
- Full lint pass: 10 checks across 197 pages
- **TAG SPRAY FIXED:** Expanded SCHEMA.md taxonomy from 48 to ~285 tags. Added 223 tags organized into 15 categories. Stripped 2 invalid tags (archived, placeholder).
- **BROKEN WIKILINKS FIXED:** 10 broken links repaired across 7 files. MITRE terms converted to bold, wrong paths corrected, raw/ links redirected to wiki pages.
- **ORPHAN BACKLINKS ADDED:** 9 backlinks added from related pages to 7 orphan concept pages. New concept pages (cognitive-overload, design-concept-alignment, etc.) now cross-referenced.
- **FRONTMATTER FIXED:** 4 pages patched (missing id, type, created, updated, tags).
- **OVERSIZED PAGES DEFERRED:** 37 pages >200 lines. Top 5 are reference docs (signs-of-ai-writing 593, spa-client-handover 561, step-3.5-flash 544, orchestrator-ultraplan 513, postgis-secure-coding 466). Splitting deferred — would break coherence.
- **LOG ROTATED:** Previous entries archived to log-archives/log-2026-04-26.md

**2026-05-05 | smart-parenting-app | Notification orphan fixes + standalone APK**
- Fixed scheduled activity completion ordering: OS notifications cancel before logging/status update to reduce orphan reminder crash windows.
- Added distinct `-extra` skip reasons for routine 15-minute pre-reminders and future-only pending schedule restoration.
- Added `scheduled_activities.deleted_at` schema/type/query/RLS filtering and Edge Function `deleted_at=is.null` scheduled summary filter.
- Built standalone Android release APK with embedded JS bundle and `.env` Supabase public credentials; installed to adb device `192.168.1.15:39903`.
- Source: sources/operational/2026-05-05-spa-notification-orphan-fixes
