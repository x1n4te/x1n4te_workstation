---
id: keycloak-admin-rest-api-001
type: concept
created: 2026-04-17
updated: 2026-04-17
last_verified: 2026-04-17
review_after: 2026-07-17
stale_after: 2026-10-17
confidence: high
source_refs:
  - https://www.keycloak.org/docs-api/latest/rest-api/index.html
  - https://docs.redhat.com/en/documentation/red_hat_build_of_keycloak/26.0/html/server_developer_guide/admin_rest_api
  - https://documentation.cloud-iam.com/resources/keycloak-api.html
status: active
tags:
  - keycloak
  - admin-api
  - rest-api
  - security
related:
  - concepts/keycloak-fastapi-security-wims-bfp
  - concepts/keycloak-custom-themes
---

# Keycloak Admin REST API

Official Keycloak Admin REST API reference. WIMS-BFP uses the Admin API via `services/keycloak_admin.py` (Camama's implementation) for user lifecycle management.

---

## Authentication

The Admin REST API requires an access token with admin permissions. Two methods:

### Method 1: Master Admin (development only)
```bash
TOKEN=$(curl -s -X POST \
  "http://keycloak:8080/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "grant_type=password" \
  --data-urlencode "client_id=admin-cli" \
  --data-urlencode "username=admin" \
  --data-urlencode "password=admin" | jq -r '.access_token')
```

### Method 2: Service Account — Client Credentials (production)
```bash
TOKEN=$(curl -s -X POST \
  "http://keycloak:8080/realms/bfp/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "grant_type=client_credentials" \
  --data-urlencode "client_id=wims-admin-service" \
  --data-urlencode "client_secret=$CLIENT_SECRET" \
  --data-urlencode "scope=openid" | jq -r '.access_token')
```

### Service Account Client Setup (wims-admin-service)

In Admin Console → Clients → `wims-admin-service`:
1. **Client Authentication:** ON
2. **Service Accounts Roles:** ON
3. **Authentication Flow:** Standard flow + Service accounts roles
4. **Client Secret:** Generate and save
5. **Service Account Roles:** Assign `manage-users`, `view-users`, `query-users`

### Service Account Roles Required

| Operation | Required Role |
|-----------|--------------|
| List users | `view-users` or `query-users` |
| Create users | `manage-users` |
| Update users | `manage-users` |
| Delete users | `manage-users` |
| Reset password | `manage-users` |
| Manage roles | `manage-users` + `manage-realm` or `manage-clients` |
| List realm roles | `view-realm` or `manage-realm` |

---

## Key Endpoints

### Users

```
GET    /admin/realms/{realm}/users                    — List users
POST   /admin/realms/{realm}/users                    — Create user
GET    /admin/realms/{realm}/users/{id}               — Get user
PUT    /admin/realms/{realm}/users/{id}               — Update user
DELETE /admin/realms/{realm}/users/{id}               — Delete user
POST   /admin/realms/{realm}/users/{id}/reset-password — Reset password
PUT    /admin/realms/{realm}/users/{id}/reset-password — Set password
GET    /admin/realms/{realm}/users/{id}/role-mappings  — Get role mappings
POST   /admin/realms/{realm}/users/{id}/role-mappings/realm — Add realm role
```

### Authentication Flows

```
GET    /admin/realms/{realm}/authentication/flows                    — List flows
POST   /admin/realms/{realm}/authentication/flows/{flowAlias}/copy   — Copy flow
GET    /admin/realms/{realm}/authentication/flows/{flowAlias}/executions — Get executions
POST   /admin/realms/{realm}/authentication/flows/{flowAlias}/executions — Add execution
PUT    /admin/realms/{realm}/authentication/executions/{id}          — Update execution
```

### Realm Roles

```
GET    /admin/realms/{realm}/roles                — List realm roles
POST   /admin/realms/{realm}/roles                — Create realm role
GET    /admin/realms/{realm}/roles/{roleName}     — Get role
PUT    /admin/realms/{realm}/roles/{roleName}     — Update role
DELETE /admin/realms/{realm}/roles/{roleName}     — Delete role
```

### Clients

```
GET    /admin/realms/{realm}/clients              — List clients
POST   /admin/realms/{realm}/clients              — Create client
GET    /admin/realms/{realm}/clients/{id}          — Get client
PUT    /admin/realms/{realm}/clients/{id}          — Update client
GET    /admin/realms/{realm}/clients/{id}/service-account-user — Get service account user
```

---

## Python Integration (WIMS-BFP)

WIMS-BFP uses the `python-keycloak` library via `services/keycloak_admin.py`:

```python
from keycloak import KeycloakAdmin, KeycloakOpenIDConnection

# Client credentials (service account)
connection = KeycloakOpenIDConnection(
    server_url="http://keycloak:8080/",
    realm_name="bfp",
    client_id="wims-admin-service",
    client_secret_key=os.environ["KEYCLOAK_ADMIN_CLIENT_SECRET"],
    verify=True,
)
admin = KeycloakAdmin(connection=connection)

# Create user
new_user = admin.create_user({
    "email": "user@bfp.gov.ph",
    "username": "new_user",
    "enabled": True,
    "firstName": "First",
    "lastName": "Last",
    "credentials": [{"type": "password", "value": "TempPass123!", "temporary": True}],
})

# Reset password
admin.set_user_password(user_id=new_user, password="NewPass123!", temporary=False)

# Assign realm role
role = admin.get_realm_role("REGIONAL_ENCODER")
admin.assign_realm_roles(user_id=new_user, roles=[role])
```

---

## Rate Limiting

Keycloak Admin API does not have built-in rate limiting. For production:
- Use a reverse proxy (Nginx) to rate-limit admin API endpoints
- Restrict admin API access to internal network only
- Monitor for brute-force attempts on admin credentials

---

## Error Handling

| HTTP Code | Meaning | Common Cause |
|-----------|---------|-------------|
| 401 | Unauthorized | Invalid/expired token |
| 403 | Forbidden | Service account lacks required role |
| 404 | Not Found | User/role/flow doesn't exist |
| 409 | Conflict | User with same username already exists |
| 400 | Bad Request | Invalid request body (missing required fields) |

---

*Source: Official Keycloak Admin REST API documentation*
*Extracted: 2026-04-17*
