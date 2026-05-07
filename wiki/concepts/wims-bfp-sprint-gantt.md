---
id: wims-bfp-sprint-gantt-001
type: concept
created: 2026-04-21
updated: 2026-04-21
last_verified: 2026-04-21
review_after: 2026-05-21
stale_after: 2026-07-21
confidence: high
source_refs:
  - raw/sources/wims-bfp-codebase/frs-modules.md (codebase wiki)
status: active
tags:
  - wims-bfp
  - design
  - operational
related:
  - concepts/wims-bfp-sprint-timeline
  - concepts/wims-bfp-frs-modules
  - mocs/wims-bfp
---

# WIMS-BFP Sprint Gantt Chart

Mermaid-format Gantt chart. Paste into any Mermaid renderer (GitHub, Obsidian, mermaid.live).

```mermaid
gantt
title WIMS-BFP Sprint Plan — Apr 22 - May 5, 2026 (24 tasks, 11 modules)
dateFormat YYYY-MM-DD
axisFormat %b %d

section S1 — M2: Offline Queue + Encryption + Sync (30%)
[FE] encrypt queued payloads Web Crypto AES-256-GCM   :s1a, 2026-04-22, 1d
[FE] queue mgmt view/edit/delete queued incidents     :s1b, after s1a, 1d
[BE] atomic sync FastAPI transaction per incident      :s1c, after s1b, 1d
[SW] integrity verify AES-GCM tag before upload        :s1d, 2026-04-23, 1d
[SW] exponential backoff retry max 5 in sync handler   :s1e, after s1d, 1d
[FE] toast handler sync-complete postMessage            :s1f, after s1e, 1d
[SQL] add Flagged status to verification_status enum   :s1g, 2026-04-24, 1d
[TEST] queue create+encrypt+sync+integrity tests       :crit, s1h, after s1g, 1d

section S2 — M3: Conflict Detection (NOT STARTED)
[BE] conflict detection endpoint + RapidFuzz         :s2a, 2026-04-25, 1d
[BE] exact+fuzzy+30min match + background task       :s2b, after s2a, 1d
[FE] wire runConflictDetection() to real backend     :s2c, after s2b, 1d
[FE] validator review UI approve/reject/merge        :s2d, after s2c, 1d
[TEST] integration tests conflict detection          :crit, s2e, after s2d, 1d

section S3 — M4: Immutable Storage (NOT STARTED)
[SQL] append-only GRANT/REVOKE on committed records  :s3a, 2026-04-27, 1d
[SQL] version_id + original_record_id columns        :s3b, after s3a, 1d
[BE] version creation on modification                :s3c, after s3b, 1d
[BE] commit verification status gate                 :s3d, after s3c, 1d
[TEST] append-only + version chain tests             :crit, s3e, after s3d, 1d

section S4 — M5: Analytics Completion (HALF)
[SQL] materialized views incident counts+trends      :s4a, 2026-04-29, 1d
[BE] filter engine date+type+location+severity+damage :s4b, after s4a, 1d
[BE] Celery beat refresh hourly                      :s4c, after s4b, 1d
[FE] analyst dashboard filters+charts+CSV export     :s4d, after s4c, 1d
[TEST] materialized view + filter correctness        :crit, s4e, after s4d, 1d

section S5 — M6: Cryptographic Security (HALF)
[BE] key rotation mechanism OpenBao/manual           :s5a, 2026-05-01, 1d
[BE] expand PII encryption narratives+casualty+damage :s5b, after s5a, 1d
[OPS] TLS enforcement Nginx SSL + Docker internal    :s5c, after s5b, 1d

section S5 — M7: IDS Suricata (HALF)
[OPS] Suricata AF_PACKET Docker network monitoring   :s5d, 2026-05-01, 1d
[OPS] app-layer parsers HTTP+DB+uploads+auth         :s5e, after s5d, 1d

section S5 — M8: XAI Threat Detection (NOT STARTED)
[BE] prompt template Sovereign Forensic Template     :s5f, 2026-05-02, 1d
[BE] Qwen2.5-3B Ollama inference pipeline            :s5g, after s5f, 1d
[BE] on-demand admin trigger sync response            :s5h, after s5g, 1d
[TEST] encryption roundtrip + Suricata + XAI tests   :crit, s5i, after s5h, 1d

section S6 — M1: Session Management (90%→100%)
[CONFIG] ssoSessionMaxLifespan 28800 (8h per FRS)    :s6a, 2026-05-04, 1d
[BE] backchannel logout on password+role change      :s6b, after s6a, 1d
[API] GET/DELETE /api/admin/sessions list+terminate  :s6c, after s6b, 1d
[FE] replace — with active sessions view+terminate   :s6d, after s6c, 1d

section S6 — M9: System Monitoring (NOT STARTED)
[BE] health API Docker+psutil+DB latency+sync        :s6e, 2026-05-04, 1d
[FE] /admin/system health cards real-time             :s6f, after s6e, 1d

section S6 — M10: Compliance RA 10173 (NOT STARTED)
[DOC] data minimization + purpose limitation audit    :s6g, 2026-05-05, 1d
[DOC] compliance report structured findings           :s6h, after s6g, 1d

section S6 — M11: Penetration Testing (NOT STARTED)
[OPS] Nmap + OWASP ZAP + sqlmap staging scans        :s6i, 2026-05-05, 1d
[DOC] PenTest report findings+remediation             :s6j, after s6i, 1d

section S6 — M13: Notifications (NOT STARTED)
[API] SSE endpoint /api/notifications/stream         :s6k, 2026-05-05, 1d
[FE] react-hot-toast non-intrusive top-right         :s6l, after s6k, 1d

section S6 — E2E Integration
[TEST] full flow create→conflict→verify→commit→analytics→notify :crit, s6m, 2026-05-05, 1d

section OUT OF SCOPE
M2: AFOR Import — Laqqui handling                    :done, laqqui, 2026-04-22, 14d
M12: User Management — cherry-picked, DONE            :done, m12, 2026-04-21, 1d
```

## Legend

| Prefix | Meaning |
|--------|---------|
| `[BE]` | Backend (Python/FastAPI) |
| `[FE]` | Frontend (Next.js/React) |
| `[API]` | API endpoint (route + handler) |
| `[SQL]` | Database (migration, schema, RLS) |
| `[OPS]` | Operations (Docker, Suricata, security) |
| `[TEST]` | Integration/E2E tests |
| `[DOC]` | Documentation/compliance |
| `[CONFIG]` | Configuration change |
| `crit` | Critical path — blocks other work |

## Related

- [[concepts/wims-bfp-sprint-timeline]] — detailed task breakdown with hour estimates
- [[concepts/wims-bfp-frs-modules]] — FRS module status and requirements
