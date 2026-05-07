---
id: keycloak-26-release-notes-001
type: source
created: 2026-04-17
updated: 2026-04-17
last_verified: 2026-04-17
review_after: 2026-07-17
stale_after: 2026-10-17
confidence: high
source_refs:
  - https://www.keycloak.org/2025/01/keycloak-2610-released
  - https://www.keycloak.org/2025/04/keycloak-2620-released
  - https://www.keycloak.org/2025/07/keycloak-2630-released
status: active
tags:
  - keycloak
  - release-notes
  - identity
  - iam
related:
  - concepts/keycloak-fastapi-security-wims-bfp
  - sources/software-dev/keycloak-production-security
  - concepts/keycloak-mfa-findings
---

# Keycloak 26.x Release Notes

Keycloak 26.x release series (2025). WIMS-BFP uses Keycloak 26 in Docker (bfp-realm.json).

---

## Keycloak 26.1.0 (January 15, 2025)

### Highlights

**Transport Stack: jdbc-ping as new default**
- Keycloak now uses its database to discover cluster nodes by default (no UDP multicast needed)
- Works out-of-the-box in cloud environments
- Previous `udp` transport is now deprecated
- Keycloak Operator continues to use `kubernetes` transport

**Virtual Threads for Infinispan and JGroups**
- Automatically enables virtual thread pool on OpenJDK 21
- Removes need to configure JGroups thread pool
- Reduces overall memory footprint

**OpenTelemetry Tracing — Fully Supported**
- Enabled by default (`opentelemetry` feature)
- Custom spans for HTTP requests, DB operations, LDAP, password hashing
- Keycloak Operator CR support

**Minimum ACR Value for clients**
- New config option on realm OIDC clients
- Enforces minimum ACR level for step-up authentication
- Community contribution by Simon Levermann

**Support for `prompt=create`**
- OIDC clients can initiate registration via `prompt=create` parameter
- Implements [Initiating User Registration](https://openid.net/specs/openid-connect-prompt-create-1_0.html) standard

---

## Keycloak 26.2.0 (April 11, 2025)

### Highlights

**Standard Token Exchange — Supported**
- Token exchange promoted from preview to supported
- Limited to internal-to-internal token exchange per RFC 8693
- Does not yet cover identity brokering or subject impersonation

**Fine-Grained Admin Permissions V2**
- New Permissions section in Admin Console (single management point)
- Resource-specific and global permissions
- Explicit operation scoping (no hidden dependencies)
- Per-realm enablement
- Replaces V1 fine-grained permissions

**Zero-configuration secure cluster communication**
- TCP-based transport stacks auto-encrypt with TLS
- Ephemeral keys/certificates auto-generated
- Strengthened secure-by-default setup

**Dynamically select authentication flows**
- New ability to dynamically select auth flows based on conditions

**Grafana dashboards for metrics**
- Keycloak troubleshooting dashboard
- Capacity planning dashboard

---

## Keycloak 26.3.0 (July 3, 2025)

### Highlights

**Recovery Authentication Codes (2FA Recovery)**
- Promoted from preview to supported feature
- Users can print recovery codes as backup 2FA
- New realms include `Recovery Authentication Code Form` as *Disabled* in browser flow
- Admin can switch to *Alternative* to enable
- Protects against lockout when losing OTP generator (e.g., phone)

**Performance improvements for import/export/migration**
- No longer degrades cumulatively per realm processed

**Simplified WebAuthn/Passkey registration**
- `skip_if_exists` parameter for AIA-based registration
- Skips action if user already has WebAuthn credential

**Simplified IdP account linking**
- Now based on Application-Initiated Action (AIA)
- Old custom protocol deprecated

**OAuth 2.0 generic broker**
- Can federate with any OAuth 2.0 compliant authorization server
- Closes gap for providers like Amazon

**Trusted email verification for OIDC brokers**
- Supports standard `email_verified` claim from OIDC providers
- Works when Trust email + Sync Mode FORCE enabled

**Asynchronous logging**
- Higher throughput, lower latency

**Rolling updates for patch releases** (experimental)
- Minimized downtime for upgrades

---

## WIMS-BFP Relevance

- **Recovery codes** — could complement our MFA setup (TOTP + recovery codes as backup)
- **Dynamic auth flow selection** — relevant to the `browser-with-mfa` vs `browser` flow issue
- **Fine-grained admin permissions V2** — relevant for the `wims-admin-service` client Camama created
- **Transport changes** — our Docker Compose uses default settings, may benefit from jdbc-ping
- **Token exchange** — relevant if we need service-to-service token delegation

---

*Source: Official Keycloak blog at keycloak.org/blog*
*Extracted: 2026-04-17*
