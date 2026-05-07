---
id: push-pull-coding-standards-001
type: concept
created: 2026-04-26
updated: 2026-04-26
last_verified: 2026-04-26
review_after: 2026-06-26
stale_after: 2026-10-26
confidence: high
source_refs:
  - raw/transcripts/matt-pocock-ai-coding-advanced-techniques-2026.md
status: active
tags:
  - ai-coding
  - software-dev
  - agents
  - pocock
  - coding-standards
  - implementation
  - review
related:
  - concepts/ralph-wiggum-software-practice
  - concepts/feedback-loops-ai-coding
  - concepts/deep-modules-ai-navigation
  - concepts/sand-castle-parallelization
  - concepts/design-concept-alignment
---

# Push vs Pull — Enforcing Coding Standards with AI

## Definition

**Push** and **pull** are two fundamentally different mechanisms for communicating information to an AI agent during coding:

| Mechanism | Direction | When Used | How It Works |
|-----------|-----------|----------|--------------|
| **Push** | Human → Agent | Always sent with every prompt | Token cost; adds to every request |
| **Pull** | Agent → Human (on demand) | Available but not forced | No token cost until agent queries |

**Push example:** Writing coding standards in `CLAUDE.md` — every prompt appends these tokens.
**Pull example:** A skill file with a description header — the agent pulls it only when relevant.

## The Push/Pull Decision Matrix

Matt Pocock (2026) articulates a specific heuristic for where each mechanism belongs:

| Phase | Mechanism | Rationale |
|-------|-----------|-----------|
| **Implementation** | Pull | Agent pulls standards only when it has a question; conservative token use preserves smart zone |
| **Automated Review** | Push | Reviewer needs both the code AND the standards to compare against; push ensures both arrive together |

> "What do I mean by push and pull? Push is where you push instructions to the LLM. So you say okay if you put something in CLAUDE.md, talk like a pirate — that instruction is always going to be sent to the agent. Pull is where you give the agent an opportunity to pull more information. And that's for instance like skills."

## Why This Matters

### Token Economics

Every token pushed to the LLM:
1. Increases context window usage
2. Strains attention relationships
3. Moves the session toward the dumb zone

Coding standards pushed unconditionally to every implementation request waste the smart zone on boilerplate. The agent may never need those tokens — but they cost attention regardless.

### Review Needs Push

Automated code review requires the reviewer to compare code against standards. If standards are not pushed to the reviewer:
- Reviewer does not have the comparison baseline
- Style violations are missed
- The review loop is broken

Implementation does not need this — the agent can reference standards as questions arise.

## The Practical Pattern

### Implementation Phase (Pull)

```
skill: coding-standards.md
  description: "Optional reading for agent. Pull this if you have questions about our patterns."

→ Agent references it when uncertain
→ Does not add tokens to every request
```

### Review Phase (Push)

```
.review/push/
  coding-standards.md  ← pushed explicitly to reviewer
  eslint-rules.md       ← pushed explicitly to reviewer
  architecture.md       ← pushed explicitly to reviewer

reviewer prompt: "Here is the code AND our coding standards. Compare them."
```

## This Is Not Just About Coding Standards

The push/pull distinction applies to all auxiliary information in an AI coding session:

| Info Type | Push or Pull? | Reason |
|-----------|-------------|--------|
| Coding standards | Push (review), Pull (implement) | Implementation asks; reviewer must compare |
| Architecture docs | Pull (with index) | Agent navigates as needed |
| Error logs | Push (per incident) | Must be in context for diagnosis |
| Canonical source (SDK template) | Push (per fix) | Non-negotiable reference |
| Design concept | Push (grill-me) | Alignment is mandatory, not optional |

## Relationship to Other Concepts

|| Concept | Connection |
|---------|-----------|
| [[concepts/feedback-loops-ai-coding]] | Automated review (push phase) is part of the feedback loop stack |
| [[concepts/sand-castle-parallelization]] | Sand Castle explicitly uses push in reviewer, pull in implementer |
| [[concepts/design-concept-alignment]] | Grill-me is a push activity (active alignment, not on-demand) |
| [[concepts/ralph-wiggum-software-practice]] | Ralph loop's review step uses push; implementation step uses pull |

## Key Takeaway

Coding standards are not inherently good as push — they are good as pull during implementation and push during review. This is a concrete token economics decision, not a preference. Pushing everything always is how you fill the context window with low-value tokens and enter the dumb zone faster.

> "Push is where you push instructions to the LLM. Pull is where you give the agent an opportunity to pull more information."

## References

- Matt Pocock, "Advanced AI Coding Techniques" (YouTube, 2026) — explicit push/pull decision framework
