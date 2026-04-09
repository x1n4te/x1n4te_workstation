---
id: ops-2026-04-09-auth-loop-fix-001
type: source
created: 2026-04-09
confidence: high
source_refs:
  - ~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/src/docker-compose.yml
status: active
tags:
  - operational
  - docker
  - auth
  - keycloak
  - wims-bfp
related:
  - sources/operational/2026-04-09-database-refactor-integration-tests
  - concepts/docker-security-wims-bfp
---

# Auth Loop Fix — 2026-04-09

**Problem:** Infinite authentication loop on dashboard login. User authenticates via Keycloak, gets redirected, app can't validate session, loops back to login.

**Root causes (3):**

---

## 1. All WIMS containers except postgres/redis/keycloak/ollama had exited

Backend, frontend, nginx-gateway, celery-worker all dead for 4 days. No backend = `/api/user/me` always unreachable = auth failure loop.

**Fix:** `docker compose up -d`

---

## 2. Keycloak had no port mapping to host

Frontend's OIDC config baked `NEXT_PUBLIC_AUTH_API_URL: http://localhost:8080/auth` at build time. Browser redirects to `http://localhost:8080/auth/realms/bfp/...` but port 8080 wasn't exposed — connection refused.

**Fix:** Added `ports: - "8080:8080"` to keycloak service.

---

## 3. Keycloak health check expected 200 OK, got 302 Found

Health check: `GET /auth/` → `grep -q '200 OK'`. Keycloak returns `302 Found` (redirect). Health check always failed → downstream services (backend) refused to start via `depends_on: condition: service_healthy`.

**Fix:** Changed health check to `grep -qE '200 OK|302'`.

---

## 4. Frontend had no port mapping (discovered by Claude Code)

After Keycloak auth, redirect goes to `http://localhost:3000/callback`. Port 3000 wasn't exposed — "this site can't be reached."

**Fix:** Added `ports: - "3000:3000"` to frontend service.

---

## 5. Ollama health check broken (pre-existing)

Ollama image has no `curl` or `wget`. Health check `curl -sf http://localhost:11434/api/tags` always failed → backend couldn't start (depends_on: ollama, condition: service_healthy).

**Fix:** Removed ollama healthcheck. Changed backend dependency to `condition: service_started`.

---

## Docker Compose Changes Summary

| Service | Change | Why |
|---|---|---|
| keycloak | +ports 8080:8080 | Browser → OIDC endpoint |
| keycloak | healthcheck accepts 302 | Keycloak redirects /auth/ |
| frontend | +ports 3000:3000 | Browser → callback URL |
| ollama | -healthcheck | No curl/wget in image |
| backend | ollama: service_started | Don't gate on ollama health |

---

## 6. BACKEND_URL bypassed nginx — cookies never reached backend

Session route at `/api/auth/session` (Next.js server-side) was calling `http://backend:8000` directly. Cookie was set on `localhost` origin (via nginx port 80). Direct call to `backend:8000` = different origin = browser doesn't send cookie = 401 on every session check.

**Fix:** Changed `BACKEND_URL` from `http://backend:8000` to `http://nginx-gateway:80` — routes through nginx so cookies flow properly.

---

## 7. Service worker intercepted API and auth routes (CORS + OIDC state)

`sw.js` was a naive cache-first implementation with no URL filtering. Intercepted ALL requests including `/api/*` and `/callback`. Caused:
- CORS errors on `/api/ref/regions` (SW fetch didn't include CORS headers)
- OIDC "No matching state found in storage" (cached callback page had stale state)

**Fix:** Added early return in fetch handler — skip intercepting `/api/` and `/auth/` routes.

---

## 8. JWT issuer mismatch (Invalid issuer)

Backend expected issuer `http://keycloak:8080/auth/realms/bfp/` (KEYCLOAK_REALM_URL). Token had `http://localhost/auth/realms/bfp` (from `KC_HOSTNAME=localhost`). Backend couldn't reach `localhost:8080` inside Docker (port mapping is host→container only).

**Fix:** Added `KEYCLOAK_ISSUER` env var to separate issuer validation from JWKS fetching. Backend fetches keys from `keycloak:8080`, validates issuer as `http://localhost/auth/realms/bfp`.

---

## 9. Dual entry points + cookie domain mismatch

Frontend exposed on both `localhost:80` (nginx) and `localhost:3000` (direct port mapping). Cookie set at `localhost:3000` was host-only (port-specific). Session check at `localhost:80` didn't send the cookie → 401 → redirect loop.

**Fix:** Removed `ports: "3000:3000"`. Single entry point via nginx port 80. All URLs changed to `http://localhost` (no port). Added `proxy_cookie_domain nginx-gateway localhost;` in nginx to rewrite backend cookie domain.

---

## 10. React 18 StrictMode double-calls signinCallback()

StrictMode double-invokes `useEffect` in dev. First `signinCallback()` succeeds and consumes OIDC state. Second call fails with "No matching state found."

**Fix:** Added `didRun` guard in callback page's useEffect.

---

## Lesson

Docker `depends_on: condition: service_healthy` is a hard gate. If the health check is wrong (Keycloak 302, ollama missing tools), ALL dependent services refuse to start. Always verify health checks actually work in the target container.

Service workers are dangerous in auth flows — they can serve stale pages, break OIDC state, and cause CORS issues. Always exclude API and auth routes from SW interception.
