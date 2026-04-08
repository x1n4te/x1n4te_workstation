---
id: suricata-cves-2026-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-04-15
stale_after: 2026-04-29
confidence: high
source_refs:
  - nvd.nist.gov/vuln/detail/CVE-2026-31934
  - nvd.nist.gov/vuln/detail/CVE-2026-22264
  - nvd.nist.gov/vuln/detail/CVE-2026-22262
  - nvd.nist.gov/vuln/detail/CVE-2026-22259
  - nvd.nist.gov/vuln/detail/CVE-2026-31937
status: active
tags:
  - suricata
  - cve
  - ids-ips
  - vulnerability
  - cybersecurity
related:
  - entities/suricata
  - concepts/threat-detection-pipeline
---

# Suricata CVEs — 2026 (Source Summary)

**Source:** NVD, SentinelOne, GitHub OISF
**Technology:** Suricata IDS/IPS
**Relevance:** WIMS-BFP's core threat detection engine

---

## CVE-2026-31934 — SMTP MIME URL Search DoS (CVSS 7.5)

**Affected:** Suricata 8.0.0 through 8.0.3
**Type:** Denial of Service (CPU exhaustion)
**Attack vector:** Remote, unauthenticated

**Description:** Quadratic complexity (O(n²)) when searching for URLs within MIME-encoded SMTP messages. Attacker sends crafted SMTP messages that trigger worst-case algorithmic behavior, causing CPU exhaustion in the IDS/IPS.

**Impact on WIMS-BFP:** If Suricata monitors SMTP traffic, an attacker could degrade detection capability, allowing malicious SMTP traffic to bypass detection.

**Patch:** Upgrade to Suricata ≥8.0.4
**Reference:** https://www.sentinelone.com/vulnerability-database/cve-2026-31934/

---

## CVE-2026-22264 — Suricata Pre-Patch Vulnerability

**Affected:** Suricata ≤7.0.14 and 8.0.0–8.0.3
**CVSS:** AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H (CVSS 9.1)
**Type:** Integrity + Availability

**Description:** Specially crafted traffic exploits a flaw in Suricata's processing logic. Specific details in OISF advisory GHSA-mqr8-m3m4-2hw5.

**Impact on WIMS-BFP:** High — affects all Suricata versions prior to patch. WIMS-BFP should verify it's running ≥7.0.15 or ≥8.0.4.

**Patch:** https://github.com/OISF/suricata/commit/549d7bf60616de8e54686a188196453b5b22f715

---

## CVE-2026-22262 — Critical Suricata Vulnerability (CVSS 9.8)

**Affected:** Multiple Suricata versions
**CVSS:** 9.8 (Critical)
**Type:** Remote, unauthenticated

**Description:** Critical vulnerability in Suricata IDS/IPS. Specific details in OISF advisory.

**Impact on WIMS-BFP:** Critical — highest CVSS score. Requires immediate patching.

**Patch:** Verify Suricata installation version: `suricata --build-info | grep version`

---

## CVE-2026-22259 — Specially Crafted Traffic

**Affected:** Suricata <8.0.3 and <7.0.14
**Type:** Processing flaw

**Description:** Specially crafted network traffic triggers processing errors in Suricata.

**Patch:** Upgrade to ≥7.0.14 or ≥8.0.3

---

## CVE-2026-31937 — DCERPC Buffering Performance

**Affected:** Suricata <7.0.15
**Type:** Performance degradation (DoS)

**Description:** Inefficiency in DCERPC buffering causes performance degradation. Can be used as a DoS vector to slow down IDS processing.

**Patch:** Upgrade to ≥7.0.15

---

## Mitigation Checklist for WIMS-BFP

```
[ ] Verify Suricata version: suricata --build-info | grep version
[ ] Patch to ≥8.0.4 if on 8.x, or ≥7.0.15 if on 7.x
[ ] Monitor for new CVEs via: https://suricata.io/security/
[ ] Alert threshold: any CVE ≥7.5 CVSS
```

---

## Concepts Derived From This Source

- [[concepts/threat-detection-pipeline]] — How Suricata fits into WIMS-BFP's threat detection chain
