# AI Cybersecurity After Mythos: The Jagged Frontier

**Source:** https://aisle.com/blog/ai-cybersecurity-after-mythos-the-jagged-frontier
**Author:** Stanislav Fort (Founder & Chief Scientist, AISLE)
**Published:** April 2026

---

## TL;DR

AISLE tested Anthropic Mythos's showcase vulnerabilities on small, cheap, open-weights models. They recovered much of the same analysis. AI cybersecurity capability is very *jagged*: it doesn't scale smoothly with model size, and the moat is the system into which deep security expertise is built, not the model itself.

## Key Findings

### 1. Small models match Mythos on detection

- **FreeBSD NFS exploit (CVE-2026-4747):** 8/8 models detected it, including GPT-OSS-20b (3.6B active params, $0.11/M tokens)
- **OpenBSD SACK bug (27 years old):** GPT-OSS-120b (5.1B active) recovered the full exploit chain in a single API call
- No agentic workflow needed — single zero-shot API calls

### 2. Inverse scaling on some tasks

- OWASP false-positive test: small open models OUTPERFORMED frontier models
- Only Opus 4.6 and borderline Sonnet 4.6 correctly traced Java data flow
- Most frontier models (Claude 3.5/3.7 Sonnet, GPT-4o) got it WRONG

### 3. Rankings reshuffle across tasks

- GPT-OSS-120b: recovers full SACK chain but FAILS Java data flow tracing
- Qwen3 32B: perfect 9.8 CVSS on FreeBSD but declares SACK code "robust"
- There is NO stable "best model for cybersecurity"

### 4. Sensitivity vs Specificity

- All models: 100% sensitivity (find the bug in unpatched code)
- Specificity varies wildly: GPT-OSS-120b only one perfectly reliable on both unpatched AND patched code
- Most models false-positive on the PATCHED code (fabricate signed-integer bypass arguments)

### 5. The system matters more than the model

- AISLE's scaffold: launch container → prompt model → hypothesize/test → ASan crash oracle → rank files → validate
- This scaffold works with multiple model families
- "A thousand adequate detectives searching everywhere will find more bugs than one brilliant detective who has to guess where to look"

## AI Cybersecurity Pipeline (5 stages)

1. **Broad-spectrum scanning** — navigate large codebases, find attack surface
2. **Vulnerability detection** — spot what's wrong in relevant code
3. **Triage and verification** — true positive vs false positive, severity
4. **Patch generation** — fix the vulnerability
5. **Exploit construction** — weaponize (hardest, least needed for defense)

## AISLE Track Record

- 15 CVEs in OpenSSL (12 out of 12 in one release, CVSS 9.8 Critical)
- 5 CVEs in curl
- 180+ externally validated CVEs across 30+ projects
- Runs on OpenSSL, curl, and OpenClaw pull requests
- Security analyzer catches vulns before shipping

## Mythos vs Reality

- Anthropic Mythos: limited-access, expensive frontier model
- AISLE tested: 3.6B-param open model at $0.11/M tokens
- Result: comparable detection capability on showcased vulnerabilities
- The "moat" is the system scaffolding + security expertise, not the model

## What This Means for Defenders

- Discovery-grade AI cybersecurity is BROADLY ACCESSIBLE now
- Don't wait for Mythos access — build with current models
- Focus on: scaffolds, pipelines, maintainer trust, workflow integration
- Cheap models deployed broadly > one expensive model deployed narrowly
- The bottleneck is security expertise and engineering, not model intelligence

## Models Tested

| Model                 | Params (active) | FreeBSD Detection | OpenBSD SACK      | OWASP FP     |
| --------------------- | --------------- | ----------------- | ----------------- | ------------ |
| GPT-OSS-120b          | 5.1B            | ✅ A+              | ✅ Full chain      | ✅ Correct    |
| GPT-OSS-20b           | 3.6B            | ✅                 | ❌ B-              | ✅ Correct    |
| Kimi K2               | open            | ✅                 | ✅ Concrete bypass | ✅ Correct    |
| DeepSeek R1           | open            | ✅ (most precise)  | ❌ F               | ✅ Correct    |
| Qwen3 32B             | 32B             | ✅ (perfect CVSS)  | ❌ "Robust"        | ❌            |
| Claude Opus 4.6       | frontier        | ✅                 | ❌                 | ✅ Correct    |
| Claude Sonnet 4.6     | frontier        | ✅                 | ❌                 | ✅ Borderline |
| Claude 3.5/3.7 Sonnet | frontier        | ✅                 | ❌                 | ❌ Wrong      |
