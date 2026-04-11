# Wiki Log

Append-only activity log. Newest entries first.

**Entries archived:** 12 older entries moved to wiki/log-archives/log-2026-04-08.md

---

## 2026-04-11 (continued)

**2026-04-11 | upgrade | S++ optimization — taxonomy, queries layer, page splits**
- Expanded: tag taxonomy 17→39 tags (7 categories: Project, Security, Infra, AI/ML, Dev, Research, Page Types)
- Created: wiki/queries/ and wiki/comparisons/ directories (query + comparison layer)
- Split: 10 oversized pages into overview + details sub-pages
  - smart-parenting-app-tech-stack: 383→85L + 341L details
  - wims-bfp-codebase-ingestion: 272→108L + 210L details
  - docker-security-wims-bfp: 252→194L + 105L details
  - slm-log-reading-pipeline: 245→96L + 193L details
  - wims-bfp-thesis-codebase-gaps: 297→145L + 194L details
  - keycloak-fastapi-security: 242→91L + 204L details
  - fastapi-security: 191→124L + 122L details
  - postgresql-security: 203→139L + 112L details
  - postgis-security: 127→106L + 65L details
  - vercel-web-interface: 216→71L + 185L details
- Fixed: all wikilink paths (added directory prefixes for detail page cross-links)
- Final: 111 pages, 0 broken links, 0 orphans, 0 missing frontmatter

**2026-04-11 | fix | SCHEMA.md created + broken links + orphans + tag cleanup**
- Created: wiki/SCHEMA.md — codified conventions, frontmatter spec, tag taxonomy (17 tags), page thresholds, update policy, archiving rules
- Fixed: 12 broken wikilinks — stripped brackets from generic terms in CTF writeups (ftp, SSH, Linux, HTB, etc.)
- Fixed: 2 orphan pages — added inbound [[wikilinks]] from llm-applied-learning-path → advisor-strategy, smart-parenting-ui-redesign → android-build-debugging
- Fixed: 528 junk tags removed — wiki page paths (404), URLs/paths (124) stripped from tags: fields across 90+ files
- Remaining: 522 topic-descriptor tags not in taxonomy (acceptable — real topic labels, just outside the 17-tag minimal set)

**2026-04-11 | audit | LLM Wiki audit gate — Karpathy-pattern full sweep**
- Fixed: 10 zero-wikilink pages — added inline [[wikilinks]] to body text
- Fixed: 24 pages missing source_refs — batch-patched all concept/entity/MOC pages
- Fixed: index page count (84→100), normalized table format (||→| )
- Fixed: log truncated from 37→15 entries, 145 lines archived to log-archives/
- Fixed: operational pages missing review_after/stale_after TTL fields
- Post-fix: 0 zero-wikilink content pages, 0 missing frontmatter fields

## 2026-04-11 (continued)

**2026-04-11 | thesis | WIMS-BFP Section 3.9 ethics — full expansion + IERC integration**
- Expanded 03-09-ethical-legal.md from ~47 lines to ~210 lines
- Added: Regulatory Compliance Framework (RA 10173 lawful bases, data subject rights, RA 10175 provisions, NPC Circulars reframed as "designed to support," DPIA → risk assessment)
- Added: Algorithmic/AI Impact section (3.9.2.4) per IERC Appendix H — XAI processing, bias risk, human oversight, transparency
- Added: Ethical Safeguards (consent protocol, vulnerable populations, data sovereignty)
- Added: Technical Data Protection (encryption, access control, audit) — rewritten as paragraphs
- Added: Data Retention and Disposal — paragraph format
- Renumbered: Data Migration Plans from 3.9.1 to 3.9.5 (resolved conflict with Regulatory Compliance Framework)
- IERC integration: IRB → IERC throughout, added form numbers (FO-IREC-001, 002, 003, 010), PHREB compliance
- AI writing remediation: both documents rewritten against Signs of AI Writing patterns (copulative avoidance, AI vocabulary, rule of three, significance puff, superficial -ing, promotional tone)
- Created: IRB-Submission-WIMS-BFP.md (standalone ethics protocol)
- Created: IREC-Form-01-WIMS-BFP.md (filled IREC application form)
- Created: wiki wims-bfp-ierc-appendices.md (IERC form field details)
- Created: wiki wims-bfp-ethics-section-revision-2026-04-11.md (revision log)

## 2026-04-11

**2026-04-11 | ethics | WIMS-BFP ethics paper — IERC forms, Section 3.9 revision, de-AI writing**
- Expanded thesis Section 3.9 (Ethical and Legal Considerations): added RA 10173 lawful bases, data subject rights, RA 10175 mitigations, NPC Circular readiness (not compliance — thesis prototype), DPIA framework, consent protocol, vulnerable populations, data sovereignty, algorithmic impact (3.9.2.4 for XAI module), encryption standards, access control, audit/non-repudiation, data retention, data migration plans (3.9.5)
- IRB → IERC terminology update: referenced FO-IREC-001, 002, 003, 010 form numbers, PHREB compliance
- Created: wiki/sources/software-dev/wims-bfp-ierc-appendices.md (appendix key details, screening checklist, document checklist)
- Created: ethics/IRB-Submission-WIMS-BFP.md (standalone IRB protocol)
- Created: ethics/IREC-Form-01-WIMS-BFP.md (in-depth FO-IREC-001 fill-out with all 6 sections)
- De-AI-ified all ethics prose using Signs of AI Writing patterns (removed copulative avoidance, AI vocabulary, rule of three, significance inflation, superficial -ing phrases)
- Skill created: ierc-ethics-review-submission (IERC form workflow + de-AI writing)

**2026-04-11 | dev | Smart Parenting App — full UI redesign from v0/NestNote design**
- Branch: `feature/ui-redesign-nestnote` (14 commits)
- Ported 5 screens from v0.app Next.js design to React Native/Expo
- Created: wiki/sources/operational/2026-04-10-smart-parenting-ui-redesign.md (full session doc)
- Created: wiki/concepts/hci-design-principles-mobile.md (10 HCI principles with examples)
- Bug fixes: RLS parent_id missing, auth guard race condition, child selection reset, signUp auto-login, Alert.alert web incompatibility, animation killed by redirect
- UI: 6 activity types (added nap + physical), child picker modal, multi-child dashboard, stepper + text duration input, meal food groups, welcome/goodbye animations
- Design tokens: primary #3B82F6, navy #0F172A, activity-specific colors

---

## 2026-04-10

**2026-04-10 | ingest | CTF writeups + command sheets + home lab SOC ingested**
- Created: wiki/sources/cybersecurity/ctf-writeups-tryhackme.md (9 THM writeups)
- Created: wiki/sources/cybersecurity/ctf-writeups-hackthebox.md (16 HTB writeups)
- Created: wiki/sources/cybersecurity/mitre-attack-command-sheet.md (4 MITRE ATT&CK kill chain refs)
- Created: wiki/sources/cybersecurity/home-lab-soc-setup.md (QEMU/KVM + Wazuh SIEM setup)
- Skills demonstrated: SSH tunneling, SQLi, IDOR, Splunk SIEM, phishing, AI security, PostgreSQL, Redis, RDP, LLMNR poisoning

**2026-04-10 | ingest | Hermes Agent v0.8.0 full reference ingested**
- Created: wiki/entities/hermes-agent-v2-reference.md (8.9KB)
- Covers: CLI commands, slash commands, config sections, 18 providers, 15 toolsets, spawning modes (one-shot/PTY/multi-agent), voice STT/TTS, agent loop architecture, contributor reference
- Source: hermes-agent skill v2.0.0

---

## 2026-04-10 (continued)

**2026-04-10 | research | Keycloak MFA findings — CONFIGURE_TOTP broken in Keycloak 24**
- Created: wiki/concepts/keycloak-mfa-findings.md (6KB)
- Finding: CONFIGURE_TOTP required action provider NOT registered in Keycloak 24.0.0
- Finding: Forced TOTP enrollment via required actions does NOT work
- Works: Self-service TOTP enrollment via account page
- Works: Manual admin TOTP enrollment per user
- Works: OTP subflow CONDITIONAL triggers after enrollment
- Workaround: Browser flow cloning + OTP REQUIRED (but blocks unenrolled users)
- Recommendation for thesis: Demonstrate MFA via manual enrollment, document as "available and configured"

---

## 2026-04-09

**2026-04-09 | ingest | Signs of AI Writing — full Wikipedia page ingested (52KB)**
- Updated: wiki/concepts/signs-of-ai-writing.md — full content from Wikipedia (52KB, 18 sections, 561 lines)
- Covers: Caveats, Content (6 subsections), Language & Grammar (5 subsections), Style (10 subsections), Communication (3 subsections), Markup (7 subsections), Citations (7 subsections), Miscellaneous, Signs of Human Writing, Ineffective Indicators, Historical Indicators
- Source: en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing

**2026-04-09 | ingest | LLM Learning Pathway — Category 5 (LLM Security) expanded**
- Updated: wiki/concepts/llm-security-learning-path.md — full content (15KB)
- Covers: NIST adversarial ML taxonomy (NIST.AI.100-2e2025), OWASP LLM Top 10, attack techniques (prompt injection, jailbreaking, data poisoning, model extraction, membership inference), red teaming process, defense strategies, 6 tools (Garak, DeepTeam, PyRIT, ART, promptmap, LLM Guard), 5 hands-on exercises, WIMS-BFP thesis security evaluation recommendations
- All 5 categories now complete: 36.5 hours total

**2026-04-09 | ingest | LLM Learning Pathway — Category 4 (Applied LLMs) expanded**
- Updated: wiki/concepts/llm-applied-learning-path.md — full content (12KB)
- Covers: API usage, fine-tuning (LoRA, RLHF, DPO), RAG pipeline, agents & tool use, deployment & quantization, 4 hands-on projects
- Projects: RAG for wiki, fine-tune Qwen2.5-3B for security narratives, security agent, XAI pipeline security evaluation

**2026-04-09 | ingest | LLM Learning Pathway — Category 3 (Papers) expanded**
- Updated: wiki/concepts/llm-papers-learning-path.md — full content (11KB)
- Covers: 8 essential papers with summaries, 18 extended reading list, reading strategy, 4-week plan, cybersecurity connections per paper
- Papers: Attention Is All You Need, BERT, GPT-2, GPT-3, Scaling Laws, InstructGPT/RLHF, LLaMA, DeepSeek-R1/GRPO

**2026-04-09 | ingest | LLM Learning Pathway — Category 2 (Transformers & Attention) expanded**
- Updated: wiki/concepts/llm-transformers-learning-path.md — full content (11KB)
- Covers: transformer architecture diagram, attention mechanism step-by-step, Q/K/V walkthrough, RNN comparison, 5 cybersecurity connections
- Resources: 3Blue1Brown Ch 5-7, Karpathy build GPT + tokenizer, Welch Labs DeepSeek MLA

**2026-04-10 | wiki | Android build debugging session ingested (13 errors documented)**
- Created: wiki/sources/operational/2026-04-10-android-build-debugging.md (5KB)
- Covers: 13 build errors + fixes, SDK 54 compatible package versions, environment setup
- Key lessons: Expo Go version matters, package versions must match SDK, Java 17 required

**2026-04-09 | ingest | Revised thesis PDF ingested (title updated, 2 Table 21 items remaining)**
- Updated: wiki/sources/software-dev/wims-bfp-abstract.md — new title, authors, adviser, institution
- Updated: wiki/sources/software-dev/wims-bfp-thesis-revisions-2026-04-08.md — status 49/51, 2 remaining
- Title changed: "A Secure Web Incident Monitoring System with AI-Assisted Threat Detection" → "A Secured Web Offline-First Incident Monitoring System with Explainable AI for Threat Interpretability"
- Remaining: Instructor (line 5674) and TanStack Query (line 5657) still in Table 21
- Removed confirmed: PyNaCl, X25519, OpenBao, Llama.cpp all at 0 occurrences
- Added confirmed: AES-256-GCM (29), TLS 1.3 (8), Ollama (4), idb (23)

**2026-04-09 | fix | Auth loop — 10 root causes in docker-compose + auth + nginx + frontend**
- Fixed: keycloak ports 8080:8080 (browser OIDC redirect blocked)
- Fixed: keycloak healthcheck accepts 302 (was expecting 200 OK)
- Fixed: frontend ports 3000:3000 (callback URL unreachable)
- Fixed: ollama healthcheck removed (no curl/wget in image)
- Fixed: backend ollama dependency relaxed to service_started
- Fixed: BACKEND_URL routed through nginx (cookie domain fix)
- Fixed: sw.js URL exclusions for /api/ and /auth/ (CORS + OIDC state fix)
- Root cause: 7 issues total — exited containers, missing ports, broken healthchecks, cookie routing, service worker interception
- Wiki: created wiki/sources/operational/2026-04-09-auth-loop-fix.md
- Commit: cd519f6

**2026-04-09 | code | Database refactor + integration tests delegated to Claude Code**
- Delegated: Claude Code print mode ($1.74, 23 turns)
- Fixed: database.py — eager init of _engine/_SessionLocal, load_dotenv() before URL resolution
- Added: get_db() (bare) + get_db_with_rls() (RLS-aware) split to avoid dependency cycle
- Tests: 15/15 passed (test_regional_crud.py — create, read, update, delete with status gating)
- Docs: updated docs/API_AND_FUNCTIONS.md (3 CRUD endpoints added), docs/ARCHITECTURE.md (DB session management section), docs/CHANGELOG.md (new Unreleased entry)
- Cleanup: Claude removed 11 stale files (1,655 lines), CHANGELOG.md moved to docs/
- Wiki: created wiki/sources/operational/2026-04-09-database-refactor-integration-tests.md


## 2026-04-11

**2026-04-11 | security | Keycloak auth hardening — MFA enforcement, account lockout, session timeout**
- Scope: 3 security gaps identified in WIMS-BFP prototype
  - MFA: OTP policy NOT SET, no OTP step in browser flow, CONFIGURE_TOTP broken in KC 24
  - Account lockout: bruteForceProtected=False (completely disabled)
  - Session timeout: ssoSessionIdleTimeout=1800 already correct, frontend has NO idle detection
- Decision: Clone browser flow to `browser-with-mfa` — OTP subflow REQUIRED WITHOUT `conditional-user-configured` (forces TOTP enrollment prompt for unenrolled users)
- Decision: Account lockout via Keycloak brute force protection (5 failures → temporary lockout, escalating to permanent)
- Decision: Disable directAccessGrantsEnabled on wims-web client (PKCE-only, prevents MFA bypass)
- Task breakdown: 8 steps (OTP policy → flow clone → brute force → client lockdown → password policy → session verify → apply → test)
- Branch: `feature/suricata-celery-ingestion` (will create feature/auth-hardening if needed)

**2026-04-11 | fix | Keycloak auth hardening — desk check results + DB fix**
- Applied: brute force protection (5 failures), password policy (12+ chars), wims-web direct grants disabled — all verified
- Applied: browser-with-mfa flow as default browser flow
- Fixed: "Cannot login, credential setup required" error on ALL users
  - Root cause: broken CONFIGURE_TOTP entry in required_action_provider table
    with empty alias and default_action=true in bfp realm
  - Fix: UPDATE required_action_provider SET default_action=false WHERE alias='' AND provider_id='CONFIGURE_TOTP'
- MFA: CONDITIONAL OTP (not REQUIRED) — Keycloak 24.0.0 CONFIGURE_TOTP bug prevents forced enrollment
  - Users with TOTP: prompted for OTP on every login (verified)
  - Users without TOTP: CONDITIONAL subflow skipped, login succeeds (verified)
- Desk check: encoder_test and analyst_test login OK, validator_test needs VERIFY_PROFILE action

**2026-04-11 | security | Keycloak 26.6.0 upgrade — MFA now fully enforced**
- Upgraded: Keycloak 24.0.0 → 26.6.0 (latest, April 2026)
- Breaking changes fixed:
  - KC_PROXY: edge → KC_PROXY_HEADERS: forwarded
  - KC_HOSTNAME_STRICT removed (deprecated in KC 26 hostname v2)
  - 'displayName' field removed from AuthenticationExecutionExportRepresentation (KC 26 schema change)
  - Test user passwords updated to meet new policy (WimsBFP2026!)
- Critical fix: CONFIGURE_TOTP now properly registered with alias='CONFIGURE_TOTP' (was null in KC 24)
  - Set as defaultAction: True — forces TOTP enrollment on first login for all users
- MFA flow: browser-with-mfa (created via API, clone endpoint broken in KC 26)
  - Cookie [ALTERNATIVE], Username/Password [REQUIRED], OTP Form [REQUIRED]
  - With CONFIGURE_TOTP as defaultAction: unenrolled users get TOTP setup page
- Commits: 2953d2a (docker-compose + realm JSON)
