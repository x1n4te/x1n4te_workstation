---
id: keycloak-26-upgrading-guide-001
type: concept
created: 2026-04-17
updated: 2026-04-17
last_verified: 2026-04-17
review_after: 2026-07-17
stale_after: 2026-10-17
confidence: high
source_refs:
  - https://docs.redhat.com/en/documentation/red_hat_build_of_keycloak/26.4/html/upgrading_guide/migration-changes
  - https://www.keycloak.org/docs/latest/upgrading/index.html
status: active
tags:
  - keycloak
  - migration
  - breaking-changes
  - security
related:
  - sources/software-dev/keycloak-26-release-notes
  - concepts/keycloak-authentication-flows
  - concepts/keycloak-docker-deployment
---

# Keycloak 26 Upgrading Guide — Breaking Changes

Breaking changes across Keycloak 26.x releases relevant to WIMS-BFP. Based on Red Hat's release-specific migration documentation.

---

## Breaking Changes at 26.4.11 (Latest)

### Stricter Access Control for Permission Tickets
- Only users/service accounts with `uma-protection` role can manage permission tickets
- Exception: resource server can manage its own tickets
- **WIMS-BFP impact:** None (we don't use UMA)

### Stricter Access Control for Realm/Client Roles
- `query-*` role alone is no longer sufficient to list roles
- Need explicit `view-realm`/`manage-realm` or `view-clients`/`manage-clients`
- **WIMS-BFP impact:** If `wims-admin-service` client uses `query-*` for role listing, may need additional role grants

### Stricter Access Control for User Profile Metadata
- Cannot fetch user profile config/metadata with just any admin role
- Need explicit: `view-realm`, `manage-realm`, `view-users`, `manage-users`, or `query-users`
- **WIMS-BFP impact:** Ensure `wims-admin-service` service account has `view-users` or `manage-users`

---

## Breaking Changes at 26.4.10

### SAML SubjectConfirmationData Validation
- Keycloak now validates `SubjectConfirmationData` for bearer type
- Checks `NotBefore`, `NotOnOrAfter`, `Recipient` in assertion
- **WIMS-BFP impact:** None (we use OIDC, not SAML)

---

## Breaking Changes at 26.4.4

### Normalized Paths Only
- Keycloak rejects HTTP requests with `..` or `//` in paths (returns HTTP 400)
- Previous behavior accepted and normalized them
- **WIMS-BFP impact:** Low — ensure Nginx gateway normalizes paths before forwarding

---

## Breaking Changes at 26.2.0

### Legacy Token Exchange Deprecated
- Old token exchange implementation deprecated
- Must migrate to standard token exchange per RFC 8693
- **WIMS-BFP impact:** None (we don't use token exchange yet)

### Fine-Grained Admin Permissions V1 → V2
- V1 permissions deprecated
- V2 provides explicit operation scoping (no hidden dependencies)
- **WIMS-BFP impact:** If using fine-grained permissions, migrate to V2

---

## Default Browser Flow Changes (26.3+)

New realms in Keycloak 26.3+ include:
- `Browser - Conditional OTP` sub-flow with `Recovery Authentication Code Form` as *Disabled*
- Recovery codes promoted from preview to supported

**WIMS-BFP impact:** Our `bfp-realm.json` was created before 26.3, so it doesn't have recovery codes flow. When reimporting the realm, Keycloak may add default flows that weren't in our JSON.

---

## Theme Migration (26.x)

### Login Themes
- Login themes remain FreeMarker-based (`.ftl`)
- Template structure changed in subtle ways between 24→26
- Check if `template.ftl`, `login.ftl`, `login-config-totp.ftl` match Keycloak 26 base

### Admin Console
- Now React-based (`keycloak.v2`)
- Old AngularJS themes don't work
- **WIMS-BFP impact:** None (we don't customize admin theme)

### Account Console
- Now React-based (`keycloak.v2`)
- **WIMS-BFP impact:** None (we don't customize account theme)

---

## User Profile Attribute Changes

- If user has email set, profile update during auth flow may change behavior
- `email_verified` claim support for OIDC brokers
- **WIMS-BFP impact:** Low — our users have emails set, verify auth flow doesn't break

---

## Pre-Upgrade Checklist for WIMS-BFP

1. [ ] Backup `bfp-realm.json` before any upgrade
2. [ ] Test realm import on new Keycloak version with `docker compose up` on clean volumes
3. [ ] Verify all 5 test users can authenticate after upgrade
4. [ ] Check that custom theme (`wims-bfp`) renders correctly on new version
5. [ ] Verify `wims-admin-service` client credentials still work
6. [ ] Test MFA flow (TOTP) on new version
7. [ ] Check RLS policies still match Keycloak user attributes
8. [ ] Verify Nginx proxy configuration is compatible

---

## Version Compatibility Matrix

| Keycloak Version | WIMS-BFP Status | Notes |
|-----------------|-----------------|-------|
| 24.x | Previously used | Old admin console, JWT issuer bug |
| 26.0.0-26.0.1 | Multiple realm import bug | Avoid |
| 26.0.2+ | Realm import fixed | Minimum recommended |
| 26.1.0 | jdbc-ping default, virtual threads | Good for production |
| 26.2.0 | Standard token exchange, admin V2 | Stable |
| 26.3.0 | Recovery codes, simplified IdP | Recommended |

---

*Source: Red Hat Keycloak 26.4 Upgrading Guide*
*Extracted: 2026-04-17*
