---
id: nextjs-cves-2026-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-04-15
stale_after: 2026-04-29
confidence: high
source_refs:
  - nvd.nist.gov/vuln/detail/CVE-2026-29057
  - sentinelone.com/vulnerability-database/cve-2026-27980
  - github.com/vercel/next.js/discussions/86977
status: active
tags:
  - nextjs
  - cve
  - frontend
  - vulnerability
  - cybersecurity
  - pwa
related:
  - entities/nextjs
  - concepts/frontend-security
---

# Next.js CVEs — 2026 (Source Summary)

**Source:** NVD, Vercel, HeroDevs, GitHub
**Technology:** Next.js (React framework)
**Relevance:** WIMS-BFP's frontend PWA (offline-first)

---

## CVE-2026-29057 — Request Smuggling (Medium)

**Affected:** Next.js 9.5.0 through <15.5.13, and 16.0.0 through <16.1.7
**CVSS:** AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N (5.3)
**Type:** Request Smuggling, Remote

**Description:** A request smuggling vulnerability exists in Next.js. The issue allows an attacker to manipulate HTTP request boundaries, potentially smuggling requests through proxy servers or load balancers.

**Impact on WIMS-BFP:** WIMS-BFP uses Next.js for the frontend PWA. If deployed behind a reverse proxy or load balancer, request smuggling could bypass authentication, access restricted API routes, or poison proxy caches.

**Patch:** Upgrade to Next.js ≥15.5.13 or ≥16.1.7

---

## CVE-2026-27980 — Unbounded Image Cache DoS (Medium)

**Affected:** Next.js 10.0.0 through <16.1.7
**Type:** Denial of Service (disk exhaustion)

**Description:** The default Next.js image optimization disk cache (`/_next/image`) has no configurable upper bound. An attacker can request images with varying parameters to continuously expand the cache until disk space is exhausted.

**Impact on WIMS-BFP:** WIMS-BFP's offline-first PWA may cache images locally. An attacker exploiting this could exhaust storage on user devices or server.

**Patch:** Upgrade to Next.js ≥16.1.7. Configure: `images.maximumDiskCacheSize`

---

## CVE-2025-55182 — Critical RCE via React Server Components (Critical)

**Affected:** React (react-server-dom*) + Next.js App Router
**CVSS:** Critical (9.0+)
**Type:** Remote Code Execution (RCE), Unauthenticated

**Description:** Insecure deserialization in React Server Components (RSC) "Flight" protocol allows unauthenticated RCE on the server. Affects any framework bundling react-server (Next.js App Router, Vite RSC, Parcel RSC, RedwoodSDK, Waku).

**Impact on WIMS-BFP:** If WIMS-BFP uses Next.js App Router with Server Components, this is a critical RCE vulnerability. An attacker could execute arbitrary code on the server with no authentication.

**Patch:** Upgrade react-server-dom* and Next.js to fixed versions. If using Pages Router instead of App Router, risk is lower but still affected.

**Reference:** https://security.berkeley.edu/news/critical-vulnerabilities-react-and-nextjs

---

## Mitigation Checklist for WIMS-BFP

```
[ ] Check Next.js version: cat node_modules/next/package.json | grep version
[ ] Patch to ≥16.1.7 (fixes CVE-2026-29057 + CVE-2026-27980)
[ ] If using App Router: verify react-server-dom* is patched
[ ] Configure images.maximumDiskCacheSize in next.config.js
[ ] Monitor: https://github.com/vercel/next.js/security/advisories
```

---

## Related Pages

- [[mocs/cybersecurity]] — Cybersecurity Map of Content (CVE tracking, ZTA, frameworks)
- [[concepts/zero-trust-architecture]] — ZTA frameworks and WIMS-BFP alignment
- [[sources/cybersecurity/suricata-cves-2026]] — Suricata CVEs (detection layer)
- [[sources/cybersecurity/keycloak-cves-2026]] — Keycloak CVEs (auth layer)
