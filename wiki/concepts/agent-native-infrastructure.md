---
id: agent-native-infrastructure-001
type: concept
created: 2026-04-30
updated: 2026-04-30
last_verified: 2026-04-30
review_after: 2026-07-30
stale_after: 2026-10-30
confidence: medium
source_refs:
  - raw/transcripts/karpathy-software-3-llms-new-computer-2026-04
status: active
tags:
  - agentic-ai
  - infrastructure
  - llm
  - software-dev
related:
  - concepts/software-3-llm-computing-paradigm
  - concepts/vibe-coding-vs-agentic-engineering
  - entities/andrej-karpathy
---

# Agent-Native Infrastructure

## Definition

**Agent-native infrastructure** refers to computing systems, interfaces, and tooling designed primarily for consumption by AI agents rather than humans. The shift from human-legible interfaces (documentation, CLIs, dashboards) to agent-legible data structures and action pathways.

## The Problem with Current Infrastructure

**Everything is still written for humans.** Libraries, frameworks, cloud services, APIs — all assume human comprehension as the baseline.

Karpathy's pet peeve:
> "Why are people still telling me what to do? I don't want to do anything. What is the thing I should copy-paste to my agent?"

Every time a human is told "go to this URL" or "configure your DNS settings," the agent must figure out how to translate that into action. Human-legible instructions are not agent-legible.

## The Sensor/Actuator Framework

Karpathy proposes decomposing agentic workloads into:
- **Sensors** — ways for agents to perceive the world (read files, query APIs, observe system state)
- **Actuators** — ways for agents to act on the world (execute code, call APIs, modify files)

Agent-native infrastructure is the design of these sensors and actuators so agents can operate autonomously.

## The Agents-All-The-Way-Down Vision

Karpathy describes a world where:
1. Human describes what they want to their personal agent
2. Agent talks to other agents to negotiate details (scheduling, contracts, coordination)
3. Infrastructure is configured and deployed autonomously
4. Agents simulate activity and test the deployment
5. The human barely intervenes except at the spec/design level

**The test:** Can you give an LLM a prompt to build Menu Genen and have it deployed on the internet with zero human intervention?

Karpathy says this test currently fails because of deployment friction — the gap between "I built it locally" and "it's live and working."

## What "Agent-Legible" Means

### Human-Legible (Current)
- Natural language documentation ("To install, run `npm install`")
- Step-by-step tutorials
- Error messages with explanations
- Dashboards with human-readable metrics

### Agent-Legible (Native)
- Direct copy-pasteable command sequences
- Structured data (JSON, not prose)
- Machine-readable error codes with recovery paths
- APIs that return all necessary context in a single call (no need to follow links)

## Examples of the Gap

**Menu Genen deployment on Vercel:**
- Required working with multiple third-party services
- Stringing together different service configurations
- Manually configuring DNS
- Navigating settings UIs designed for human comprehension

An agent-native equivalent would be:
- A single API or spec that says "deploy this app to production"
- The agent handles service selection, configuration, and DNS automatically

## The Infrastructure Rewrite

Karpathy's prediction: "Everything has to be rewritten. Everything is still fundamentally written for humans and has to be moved around."

This is analogous to the shift from desktop apps to web apps — not just a technology change, but a complete rethinking of what the interface assumes about its user.

## Implications

### For Platform Builders
- Design APIs as if the caller is an agent with full context
- Return complete information in responses (no "click here for more")
- Provide machine-readable error recovery paths
- Make authentication and authorization agent-compatible (not just human-friendly OAuth flows)

### For Developers Using Agents
- Think "what would I copy-paste to an agent?" not "what code would I write?"
- Design specs that agents can execute without human mediation
- Build verification loops that agents can run autonomously

### For AI-Native Application Design
- Consider whether your app could be replaced by a sufficiently powerful prompt to an LLM
- If yes, question whether the code path adds unique value
- Prefer prompting over programming when possible

## Connection to Software 3.0

Agent-native infrastructure is the **deployment and execution layer** of Software 3.0:

- [[concepts/software-3-llm-computing-paradigm]] establishes that prompting is the programming paradigm
- Agent-native infrastructure is the platform that makes prompting sufficient for end-to-end task completion

## Key Takeaway

> "I don't want to do anything. What is the thing I should copy-paste to my agent?"

The next generation of infrastructure will be designed for agents, not humans. The ones who build it will have a structural advantage.

## References

- [[raw/transcripts/karpathy-software-3-llms-new-computer-2026-04]] — full transcript
- [[entities/andrej-karpathy]] — speaker
- [[concepts/software-3-llm-computing-paradigm]] — the paradigm context
