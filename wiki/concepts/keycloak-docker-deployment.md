---
id: keycloak-docker-deployment-001
type: concept
created: 2026-04-17
updated: 2026-04-17
last_verified: 2026-04-17
review_after: 2026-07-17
stale_after: 2026-10-17
confidence: high
source_refs:
  - https://stackoverflow.com/questions/78903192/keycloak-import-realm-docker-compose
  - https://github.com/keycloak/keycloak/issues/34095
  - https://github.com/keycloak/keycloak/issues/38096
status: active
tags:
  - keycloak
  - docker
  - deployment
  - infrastructure
related:
  - concepts/docker-security-wims-bfp
  - concepts/keycloak-fastapi-security-wims-bfp
  - concepts/keycloak-authentication-flows
  - concepts/keycloak-26-upgrading-guide
---

# Keycloak Docker Deployment & Realm Import

Documentation on running Keycloak in Docker with realm auto-import. Critical for WIMS-BFP's Docker Compose setup and the `--import-realm` behavior that caused UUID drift.

---

## Docker Compose Configuration (WIMS-BFP)

```yaml
services:
  keycloak:
    image: quay.io/keycloak/keycloak:26.0
    command: start --import-realm
    environment:
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin
      KC_DB: postgres
      KC_DB_URL: jdbc:postgresql://postgres:5432/keycloak
      KC_DB_USERNAME: keycloak
      KC_DB_PASSWORD: keycloak
      KC_HOSTNAME_STRICT: "false"
      KC_HTTP_ENABLED: "true"
    volumes:
      - ./keycloak/bfp-realm.json:/opt/keycloak/data/import/bfp-realm.json:ro
      - ./keycloak/themes/wims-bfp:/opt/keycloak/themes/wims-bfp:ro
    ports:
      - "8080:8080"
    depends_on:
      postgres:
        condition: service_healthy
```

---

## Realm Import Behavior

### `--import-realm` flag

When `--import-realm` is set, Keycloak imports all `.json` files from `/opt/keycloak/data/import/` on startup.

**Critical behaviors:**

1. **First import:** Creates the realm with all users, roles, clients, flows
2. **Subsequent imports:** The behavior depends on Keycloak version and what already exists:
   - If realm exists: **SKIPPED** (does not update)
   - If realm doesn't exist: **CREATED** fresh
3. **User IDs:** If `id` field is NOT set in the JSON, Keycloak **generates a new UUID** each time

### The UUID Drift Problem (WIMS-BFP)

**Root cause of auth loop (PR #23):**

When `id` is omitted from user definitions in `bfp-realm.json`:
```json
{
  "users": [
    {
      "username": "encoder_test",
      "email": "encoder@bfp.gov.ph",
      "enabled": true,
      "credentials": [{"type": "password", "value": "WimsBFP2026!", "temporary": false}]
    }
  ]
}
```

Keycloak generates UUIDs like:
- First import: `a1b2c3d4-e5f6-7890-abcd-ef1234567890`
- After volume reset + reimport: `f9e8d7c6-b5a4-3210-fedc-ba9876543210`

Since `wims.users.keycloak_id` stores the first UUID, the second import creates a **mismatch** → auth fails → redirect loop.

### The Fix: Deterministic User IDs

Set explicit `id` values in `bfp-realm.json`:
```json
{
  "users": [
    {
      "id": "11111111-1111-4111-8111-111111111111",
      "username": "encoder_test",
      "email": "encoder@bfp.gov.ph",
      "enabled": true,
      "realmRoles": ["REGIONAL_ENCODER"],
      "credentials": [{"type": "password", "value": "WimsBFP2026!", "temporary": false}]
    }
  ]
}
```

**AND** use `ON CONFLICT` upsert in `01_wims_initial.sql`:
```sql
INSERT INTO wims.users (user_id, keycloak_id, username, role, ...)
VALUES ('11111111-1111-4111-8111-111111111111', '11111111-1111-4111-8111-111111111111', 'encoder_test', ...)
ON CONFLICT (username) DO UPDATE
SET keycloak_id = EXCLUDED.keycloak_id;
```

---

## Import Directory

Keycloak expects realm files at:
```
/opt/keycloak/data/import/
```

In Docker, mount the file:
```yaml
volumes:
  - ./bfp-realm.json:/opt/keycloak/data/import/bfp-realm.json:ro
```

**Note:** The `:ro` (read-only) prevents accidental modifications.

---

## Multiple Realm Import

Keycloak 26.0-26.0.1 had a [bug](https://github.com/keycloak/keycloak/issues/34095) with importing multiple realms. Fixed in 26.0.2+.

For multiple realms, use separate files:
```
/opt/keycloak/data/import/
├── realm-one.json
└── realm-two.json
```

---

## Health Check

Docker health check for Keycloak:
```yaml
healthcheck:
  test: ["CMD-SHELL", "exec 3<>/dev/tcp/localhost/8080 && echo -e 'GET /health/ready HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n' >&3 && cat <&3 | grep -q 'HTTP/1.1 200\\|HTTP/1.1 302'"]
  interval: 30s
  timeout: 10s
  retries: 5
  start_period: 60s
```

**Note:** Keycloak may return 302 (redirect to admin console) before realm is fully loaded. Accept both 200 and 302.

---

## Theme Deployment

Mount custom themes at:
```
/opt/keycloak/themes/{theme-name}/
```

For WIMS-BFP:
```yaml
volumes:
  - ./keycloak/themes/wims-bfp:/opt/keycloak/themes/wims-bfp:ro
```

Theme is selected in realm JSON:
```json
{
  "loginTheme": "wims-bfp"
}
```

---

## Common Docker Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Realm not importing | Wrong mount path | Mount at `/opt/keycloak/data/import/` |
| Import skipped on restart | Realm already exists (not idempotent) | Delete realm first, or use `--override` flag |
| UUID drift on reimport | Users missing `id` field | Set deterministic UUIDs in realm JSON |
| Keycloak crash loop | PostgreSQL not ready | Add `depends_on` with healthcheck |
| Theme not loading | Wrong mount path | Mount at `/opt/keycloak/themes/{name}/` |
| Health check failing | Port not exposed | Check `ports: ["8080:8080"]` |

---

## Environment Variables Reference

| Variable | Purpose | WIMS-BFP Value |
|----------|---------|----------------|
| `KEYCLOAK_ADMIN` | Admin username | `admin` |
| `KEYCLOAK_ADMIN_PASSWORD` | Admin password | (from env_file) |
| `KC_DB` | Database type | `postgres` |
| `KC_DB_URL` | JDBC URL | `jdbc:postgresql://postgres:5432/keycloak` |
| `KC_DB_USERNAME` | DB user | `keycloak` |
| `KC_DB_PASSWORD` | DB password | `keycloak` |
| `KC_HOSTNAME_STRICT` | Strict hostname check | `false` (Docker networking) |
| `KC_HTTP_ENABLED` | Allow HTTP (no TLS) | `true` (internal network) |

---

*Sources: Keycloak GitHub issues, Stack Overflow, Official Keycloak Docker docs*
*Extracted: 2026-04-17*
