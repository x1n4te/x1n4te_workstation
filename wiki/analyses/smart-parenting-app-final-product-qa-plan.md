---
id: smart-parenting-app-final-product-qa-plan-001
type: analysis
created: 2026-04-23
updated: 2026-04-23
last_verified: 2026-04-23
review_after: 2026-06-22
stale_after: 2026-08-21
confidence: high
source_refs:
  - sources/operational/2026-04-23-spa-final-product-dual-agent-qa-plan
  - concepts/smart-parenting-app-tech-stack
  - concepts/smart-parenting-app-system-architecture
  - concepts/expo-local-notifications
status: active
tags:
  - smart-parenting-app
  - testing
  - analysis
  - mobile-dev
  - agents
related:
  - concepts/smart-parenting-app-tech-stack
  - concepts/smart-parenting-app-system-architecture
  - concepts/expo-local-notifications
  - sources/operational/2026-04-23-spa-final-product-dual-agent-qa-plan
---

# Smart Parenting App — Final Product QA Plan (Dual-Agent)

## Purpose

This page defines the **final-product QA track** for Smart Parenting after the baseline audit and bug-fix phases. It is meant to answer a stricter release question:

> Is the app ready to behave like a production release candidate on real parent workflows, with no known severe defects and no avoidable codebase bloat?

This plan builds on [[concepts/smart-parenting-app-tech-stack]], validates architecture assumptions from [[concepts/smart-parenting-app-system-architecture]], and explicitly includes notification behavior from [[concepts/expo-local-notifications]].

## Important Constraint: "No Errors" Means "No Known Ship-Blocking Errors"

The app cannot be proven mathematically free of all errors. The actionable product standard is:
- **0 known Critical issues**
- **0 known High issues**
- **0 dead primary flows**
- **0 prohibited HCI/security regressions**
- **0 unresolved runtime console errors in certified flows**
- **0 must-fix dependency or dead-code bloat findings**

Anything weaker is not release certification.

## Preconditions

Before this plan starts:
1. **Phase 1** static QA baseline must exist.
2. **Phase 2** high-priority findings from the baseline must already be in active fix/retest flow.
3. The app architecture and current feature set must be documented in the wiki.

## Agent Topology

### Controller
A controller agent owns:
- phase dispatch
- report collation
- conflict resolution
- rerun decisions
- final sign-off synthesis

### Agent A — MiniMax-M2.7
**Role:** compliance auditor

Best used for:
- strict checklist execution
- static/runtime correctness verification
- data integrity and security review
- dependency/dead-code/bloat analysis
- release gating logic

### Agent B — Kimi-K2.6
**Role:** product dogfooder

Best used for:
- end-to-end user journey validation
- HCI friction detection
- runtime behavior checking
- exploratory bug discovery
- perceived product readiness evaluation

## Operating Rules

1. **Different prompts, different jobs.** Do not send identical instructions to both models.
2. **No self-verification.** A model must not be the final reviewer of its own fix.
3. **No concurrent edits to the same source files.** If write access is needed, use isolated worktrees.
4. **Separate reports per phase.** Each model writes its own report before controller synthesis.
5. **Fail closed on evidence.** A finding is confirmed only when:
   - both agents reproduce it, or
   - one agent provides hard evidence (screenshot, console trace, exact repro, file path/diff).

## Role Split by Phase

| Phase | MiniMax-M2.7 | Kimi-K2.6 | Primary Output |
|---|---|---|---|
| 3 | Runtime checklist + state coverage | Real-user runtime walkthrough | Runtime verdict |
| 4 | Core flow certification matrix | End-to-end flow execution | Flow pass/fail matrix |
| 5 | Failure injection checklist | Graceful-failure UX validation | Edge-case report |
| 6 | RLS/data/refetch/security audit | Runtime data-integrity verification | Integrity verdict |
| 7 | Dependency/dead-code/bloat audit | Perceived performance/jank audit | Bloat/perf report |
| 8 | Release-build readiness + env/migration checks | Fresh install / reinstall / smoke validation | RC readiness report |
| 9 | Independent ship score | Independent ship score | Final sign-off |

## Phase 3 — Runtime Product Validation

### Objective
Validate that the running app behaves coherently in normal usage, not just in static inspection.

### MiniMax lane
- verify all 5 tabs are accessible
- check modal open/close paths
- confirm loading/error/empty states where expected
- confirm pull-to-refresh on list/data surfaces
- detect dead buttons and missing handlers
- check for console/runtime noise in golden flows
- confirm no `Alert.alert()` regressions

### Kimi lane
- cold start the app like a parent would
- sign in, select child, navigate across tabs
- open/close key modals and forms
- move app background → foreground
- relaunch and confirm persistence behavior
- note confusion, friction, and broken affordances

### Exit criteria
- no crashes or redboxes
- no blank dead-end screens
- no dead primary actions

## Phase 4 — Core Flow Completion Matrix

### Objective
Certify every critical user journey end-to-end.

### Flows to certify
1. sign in / sign out
2. add/select child
3. log screen time
4. log sleep
5. log nap
6. log meal
7. log physical activity
8. log education
9. create schedule
10. update schedule
11. delete schedule
12. log from schedule
13. notification tap → correct navigation
14. History filtering aligned to selected context
15. AI Insights generation + cache behavior
16. settings updates

### Exit criteria
- all critical flows pass
- no flow requires workaround
- every mutation refetches visibly and correctly

## Phase 5 — Failure & Edge-Case Validation

### Objective
Validate graceful failure behavior under bad inputs and unstable conditions.

### Failure cases
- no network
- Supabase query failure
- expired auth/session
- empty data sets
- soft-deleted child edge cases
- notification permission denied
- invalid time range
- overnight duration cases
- double-submit
- fast modal reopen after failure
- stale child/store state transitions

### MiniMax lane
Drive the failure matrix and verify expected error-state coverage.

### Kimi lane
Evaluate the UX quality of failure handling:
- inline errors
- retry paths
- spinner behavior
- form recovery after failed submit
- no silent failure

### Exit criteria
- every failure shows feedback
- no stuck full-screen spinner
- no silent broken state

## Phase 6 — Data Integrity & Security Validation

### Objective
Prove that app behavior still respects data boundaries and refetch discipline in realistic usage.

### MiniMax lane
Audit:
- RLS assumptions and boundaries
- soft-delete defense-in-depth
- mutation → refetch discipline
- no client service-role usage
- no leaked keys
- AI `based_on` audit trail
- notification ID consistency
- stale Zustand closure risks in listeners

### Kimi lane
Runtime verify:
- updated data actually reflects persisted state
- child switching scopes data correctly
- soft-deleted data does not leak back into UI
- notification tap selects correct child/screen
- schedule changes persist and re-render correctly

### Exit criteria
- 0 auth boundary issues
- 0 soft-delete leaks
- 0 stale post-write UI states
- 0 missing AI audit trails on new records

## Phase 7 — Performance & Bloat Audit

### Objective
Ensure the app is lean enough to ship and not carrying unnecessary maintenance weight.

### MiniMax lane
Audit for:
- unused dependencies
- dead files/components/hooks/styles/constants
- TODO/FIXME/stub leftovers
- debug logs and stray console calls
- duplicate UI implementations
- banned packages
- abandoned/generated leftovers

### Kimi lane
Audit perceived product performance:
- dashboard responsiveness
- tab switch latency
- modal open/close responsiveness
- pull-to-refresh smoothness
- History chart rendering behavior
- schedule/log flow responsiveness

### Exit criteria
- no unjustified dependencies worth removing
- no dead feature remnants left in place
- no must-fix UI jank in core flows
- cleanup recommendations stay surgical

## Phase 8 — Release Candidate Validation

### Objective
Validate the actual ship candidate, not only a development session.

### MiniMax lane
Check:
- TypeScript health
- Expo health / doctor status
- environment config sanity
- DB migration readiness/application state
- notification configuration sanity
- release-only risk checklist

### Kimi lane
Smoke test:
- fresh install
- reinstall / relaunch
- first-run permissions
- notification behavior after reinstall
- core flow smoke in release-like conditions

### Exit criteria
- release path is clean
- migration state is verified
- no release-only blocker remains

## Phase 9 — Final Sign-Off Gate

Both models independently score:
- runtime stability
- HCI correctness
- data integrity
- platform parity
- bloat status
- ship confidence

The controller merges those into `RELEASE_SIGNOFF.md`.

### Hard ship gate
Ship only if:
- Critical = 0
- High = 0
- prohibited-pattern violations = 0
- dead primary actions = 0
- unresolved runtime console errors in certified flows = 0
- must-fix bloat findings = 0

## Artifact Layout

```text
docs/qa/final-product/
  phase-3/
    minimax.md
    kimi.md
    verdict.md
  phase-4/
    minimax.md
    kimi.md
    verdict.md
  phase-5/
    minimax.md
    kimi.md
    verdict.md
  phase-6/
    minimax.md
    kimi.md
    verdict.md
  phase-7/
    minimax.md
    kimi.md
    verdict.md
  phase-8/
    minimax.md
    kimi.md
    verdict.md
  RELEASE_SIGNOFF.md
```

## Recommended Prompt Split

### MiniMax-M2.7 prompt theme
"Falsify release readiness. Be systematic, skeptical, and fail-closed. Prioritize HCI violations, data-integrity issues, dead UI, console/runtime errors, release blockers, and bloat."

### Kimi-K2.6 prompt theme
"Dogfood the product like a real parent. Prioritize confusion, friction, weak validation, dead taps, misleading copy, modal friction, and broken end-to-end flows."

## Execution Cadence

For each phase:
1. Run both agents in parallel.
2. Cross-review the top findings.
3. Merge findings into a controller verdict.
4. Batch fixes by severity.
5. Re-test only impacted paths plus adjacent regressions.

## Recommended Ownership Split

If one model must lead while the other complements:
- **Kimi-K2.6 leads Phases 3, 4, 5**
- **MiniMax-M2.7 leads Phases 6, 7, 8**
- **Both independently score Phase 9**

This split aligns product behavior testing with dogfooding strength and keeps compliance/bloat/release gating with the stricter checklist-oriented model.

## Summary

The final-product QA track turns Smart Parenting QA from a static bug list into a release-candidate certification process. It preserves the current HCI-first philosophy while adding stronger evidence requirements, dual-model cross-checking, and an explicit ship gate.

---

## Related

- [[sources/operational/2026-04-23-spa-final-product-dual-agent-qa-plan]]
- [[concepts/smart-parenting-app-tech-stack]]
- [[concepts/smart-parenting-app-system-architecture]]
- [[concepts/expo-local-notifications]]
