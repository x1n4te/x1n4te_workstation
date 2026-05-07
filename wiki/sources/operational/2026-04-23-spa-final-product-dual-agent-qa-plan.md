---
id: spa-final-product-dual-agent-qa-plan-2026-04-23
type: source
created: 2026-04-23
updated: 2026-04-23
status: active
tags:
  - smart-parenting-app
  - operational
  - testing
  - mobile-dev
  - agents
source_refs:
  - concepts/smart-parenting-app-tech-stack
  - concepts/smart-parenting-app-system-architecture
  - concepts/expo-local-notifications
---

# Smart Parenting App — Final Product Dual-Agent QA Plan

**Date:** 2026-04-23  
**Focus:** Define the release-candidate QA track that goes beyond the baseline audit and validates runtime quality, data integrity, and codebase lean-ness.  
**Models:** `minimax-m2.7` + `kimi-k2.6`

---

## Summary

This plan extends the existing Smart Parenting QA effort from a static baseline + bugfix cycle into a **final product certification workflow**.

The key reframing is that the goal is not to prove the app has literally zero errors. The goal is to reach a defensible ship state with:
- **0 known Critical issues**
- **0 known High issues**
- **0 dead primary actions**
- **0 prohibited-pattern regressions**
- **0 unresolved runtime console errors in golden flows**
- **0 must-fix bloat findings**

The plan is recorded in detail in [[analyses/smart-parenting-app-final-product-qa-plan]]. It builds on the current app architecture documented in [[concepts/smart-parenting-app-tech-stack]] and [[concepts/smart-parenting-app-system-architecture]].

## Dual-Agent Split

### MiniMax-M2.7
Assigned as the **compliance auditor**:
- checklist-driven validation
- data integrity and security verification
- dependency/dead-code/bloat review
- release gating and pass/fail scoring

### Kimi-K2.6
Assigned as the **product dogfooder**:
- end-to-end real-user flow testing
- UX/HCI friction discovery
- runtime validation
- edge-case reproduction and behavior checks

## Final Product QA Phases

### Phase 3 — Runtime Product Validation
Validate cold start, auth, child switching, tabs, modal behavior, pull-to-refresh, resume flow, and runtime stability.

### Phase 4 — Core Flow Completion Matrix
Certify every critical parent flow: logging all activity types, schedules, notification tap navigation, History accuracy, AI Insights, and Settings.

### Phase 5 — Failure & Edge-Case Validation
Test offline behavior, Supabase failures, expired auth, empty states, permission denial, invalid times, double-submit, and stale-state scenarios.

### Phase 6 — Data Integrity & Security Validation
Verify RLS assumptions, soft-delete filtering, mutation→refetch discipline, service-role boundaries, audit trails, and notification identifier consistency.

### Phase 7 — Performance & Bloat Audit
Audit unused dependencies, dead files/components/hooks/styles, console/debug leftovers, duplicate UI implementations, and perceived UI responsiveness.

### Phase 8 — Release Candidate Validation
Validate release-like readiness: TypeScript status, Expo health, migration/application sanity, fresh install/reinstall behavior, and permission flows.

### Phase 9 — Final Sign-Off Gate
Require independent scoring and merged verdict before ship.

## Operating Rules

1. The two models should receive **different mandates** rather than duplicate prompts.
2. No model should verify its own fix.
3. Findings should be considered confirmed only when both agents reproduce them, or when one provides hard evidence.
4. If either agent edits files, use isolated worktrees or restrict them to report files only.
5. Each phase should produce separate agent outputs plus a merged verdict.

## Deliverables

```text
docs/qa/final-product/
  phase-3/
  phase-4/
  phase-5/
  phase-6/
  phase-7/
  phase-8/
  RELEASE_SIGNOFF.md
```

## Hard Ship Gate

Ship only if:
- Critical = 0
- High = 0
- prohibited-pattern violations = 0
- dead primary actions = 0
- unresolved runtime console errors in certified flows = 0
- must-fix bloat findings = 0

---

## Related

- [[analyses/smart-parenting-app-final-product-qa-plan]] — detailed execution design
- [[concepts/smart-parenting-app-tech-stack]] — app stack + QA context
- [[concepts/smart-parenting-app-system-architecture]] — architecture boundaries to validate
- [[concepts/expo-local-notifications]] — notification behavior that must be certified in Phases 3–8
