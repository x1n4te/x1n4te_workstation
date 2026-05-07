---
id: keycloak-custom-themes-001
type: concept
created: 2026-04-17
updated: 2026-04-17
last_verified: 2026-04-17
review_after: 2026-07-17
stale_after: 2026-10-17
confidence: high
source_refs:
  - https://www.keycloak.org/ui-customization/themes
  - https://docs.redhat.com/en/documentation/red_hat_build_of_keycloak/26.4/html/migration_guide/migrating-themes
  - https://docs.redhat.com/en/documentation/red_hat_build_of_keycloak/26.0/html/server_developer_guide/themes
status: active
tags:
  - keycloak
  - themes
  - frontend
  - ui
related:
  - concepts/keycloak-fastapi-security-wims-bfp
  - concepts/keycloak-mfa-findings
---

# Keycloak Custom Themes

Official documentation on Keycloak theme system — creating, configuring, and deploying custom login themes. WIMS-BFP uses a custom `wims-bfp` login theme with BFP branding.

---

## Theme Types

A theme can customize one or more of:

| Type | What it controls |
|------|-----------------|
| **Login** | Login forms, registration, password reset, OTP setup, error pages |
| **Account** | Account Console (user profile management) |
| **Admin** | Admin Console |
| **Email** | Email templates (verification, password reset, events) |
| **Welcome** | Welcome page shown on first Keycloak access |

WIMS-BFP only uses: **Login** theme.

---

## Theme Structure

```
themes/wims-bfp/
└── login/
    ├── theme.properties           ← theme config (parent, imports, styles)
    ├── login.ftl                  ← main login form template
    ├── login-config-totp.ftl      ← TOTP setup page (first MFA login)
    ├── login-update-password.ftl  ← password change forced page
    ├── register.ftl               ← registration form
    ├── register-commons.ftl       ← shared registration components
    ├── password-commons.ftl       ← shared password components
    ├── template.ftl               ← base template (HTML skeleton, head, body)
    ├── user-profile-commons.ftl   ← user profile form components
    ├── resources/
    │   ├── css/
    │   │   ├── styles.css         ← base styles (imports)
    │   │   └── wims-custom.css    ← custom BFP branding styles
    │   ├── script/
    │   │   └── cdn.min.js         ← scripts
    │   └── img/
    │       └── bfp-logo.png       ← BFP logo image
```

---

## theme.properties

```properties
# Extend the base Keycloak theme (provides translations, defaults)
parent=base
# Import common Keycloak resources (messages, CSS, JS)
import=common/keycloak
# Set login theme CSS
styles=css/wims-custom.css css/styles.css
# Set login theme scripts
scripts=script/cdn.min.js
# Locale support
locales=en,fil
```

---

## Template Inheritance (FTL)

Keycloak uses FreeMarker templates (`.ftl` files). Each page template imports `template.ftl`:

```html
<#import "template.ftl" as layout>
<@layout.registrationLayout>
  <!-- Your custom HTML here -->
</@layout.registrationLayout>
```

### template.ftl — Base Template

The `template.ftl` file defines:
- `<head>` — CSS imports, meta tags
- `<body>` — page structure, header, footer
- `<#nested>` — child template content injection
- Message display (success, error, warning)
- Info area (registration link, locale selector)

**WIMS-BFP customization:** `template.ftl` includes BFP logo, custom CSS, and branded header/footer.

### login.ftl — Login Form

```html
<#import "template.ftl" as layout>
<@layout.registrationLayout displayMessage=!messagesPerField.existsError('username','password')
                           displayInfo=realm.password && realm.registrationAllowed>
  <form id="kc-form-login" action="${url.loginAction}" method="post">
    <input id="username" name="username" type="text" />
    <input id="password" name="password" type="password" />
    <input type="submit" value="${msg("doLogIn")}" />
  </form>
</@layout.registrationLayout>
```

### login-config-totp.ftl — TOTP Setup

Shown when user has `CONFIGURE_TOTP` required action. Displays:
- QR code for authenticator app
- Secret key text input (manual entry)
- OTP code verification
- Remember device checkbox

**WIMS-BFP issue:** This template may have platform-specific rendering differences on Windows-hosted Keycloak.

---

## Configuring a Theme

### Via Admin Console:
1. Admin Console → Realm Settings → Themes tab
2. Set **Login Theme** to `wims-bfp`
3. Save

### Via realm JSON (bfp-realm.json):
```json
{
  "loginTheme": "wims-bfp"
}
```

---

## Deploying Themes

### Docker Compose (WIMS-BFP approach):
```yaml
volumes:
  - ./keycloak/themes/wims-bfp:/opt/keycloak/themes/wims-bfp:ro
```

Keycloak loads themes from `$KC_HOME/themes/` directory. Changes require Keycloak restart (unless caching is disabled).

### Disable caching for development:
```bash
bin/kc.sh start \
  --spi-theme--static-max-age=-1 \
  --spi-theme--cache-themes=false \
  --spi-theme--cache-templates=false
```

---

## Migrating Custom Themes to Keycloak 26

### Key changes in Keycloak 26:

1. **Admin Console is now React-based** (`keycloak.v2`)
   - Old AngularJS admin console (`keycloak`) is deprecated
   - No migration path from old admin themes
   - Custom admin themes must extend `keycloak.v2`

2. **Account Console is now React-based** (`keycloak.v2`)
   - Old account console (`keycloak`) is deprecated
   - Custom account themes must extend `keycloak.v2`

3. **Login themes remain FreeMarker-based**
   - Login theme templates (.ftl) are in the themes JAR
   - Path: `$KC_HOME/lib/lib/main/org.keycloak.keycloak-themes-${KC_VERSION}.jar`
   - Can be extracted with any ZIP tool

4. **Template changes between versions**
   - When upgrading, check if base templates changed
   - Custom overrides may need updates to match new base template structure
   - Key fields to watch: message keys, CSS class names, form field names

---

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Theme not showing | Not set in realm settings | Set loginTheme in Admin Console or realm JSON |
| Broken CSS | Wrong `styles` path in theme.properties | Check relative paths from login/ directory |
| MFA page broken | `login-config-totp.ftl` references old base template | Update template imports to match Keycloak 26 base |
| Template not found | FTL file missing from theme directory | Copy from base theme, then customize |
| Windows rendering differences | Platform-specific Freemarker behavior | Test on target platform; use platform-neutral CSS |

---

*Source: Official Keycloak UI Customization Guide + Red Hat Keycloak 26 Developer Guide*
*Extracted: 2026-04-17*
