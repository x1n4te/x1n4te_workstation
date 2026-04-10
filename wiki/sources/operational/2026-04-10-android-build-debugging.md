---
id: android-build-debugging-2026-04-10-001
type: source
created: 2026-04-10
updated: 2026-04-10
last_verified: 2026-04-10
review_after: 2026-07-10
stale_after: 2026-10-09
confidence: high
status: active
tags:
  - operational
  - react-native
  - expo
  - android
  - debugging
  - mobile-development
related:
  - concepts/smart-parenting-app-tech-stack
  - concepts/mldc-mobile-development-lifecycle
---

# Android Build Debugging Session — 2026-04-10

**Project:** Smart Parenting App (React Native + Expo SDK 54)
**Duration:** ~2 hours of debugging
**Result:** Android build succeeds, app installs on device

---

## Errors Encountered and Fixes

### 1. `expo-build-properties` plugin not found
**Error:** `PluginError: Failed to resolve plugin for module "expo-build-properties"`
**Cause:** Plugin listed in `app.json` but not installed
**Fix:** Remove from `app.json` plugins array — not needed for development

### 2. `expo-notifications` plugin not found
**Error:** Same as above
**Cause:** Not installed
**Fix:** Remove from `app.json` plugins — add back later when needed

### 3. Missing `expo-asset`
**Error:** `The required package expo-asset cannot be found`
**Cause:** Required by Metro bundler but not installed
**Fix:** `npm install expo-asset expo-font`

### 4. Project incompatible with Expo Go
**Error:** `This project requires a newer version of expo go`
**Cause:** Project on SDK 55, Expo Go only supports up to SDK 54
**Fix:** Downgrade all packages to SDK 54 compatible versions

### 5. Missing `expo-linking`
**Error:** `Unable to resolve "expo-linking" from expo-router`
**Cause:** Peer dependency not installed
**Fix:** `npm install expo-linking expo-web-browser expo-constants`

### 6. `setCustomSourceTransformer is not a function`
**Error:** `TypeError: 0, _resolveAssetSource.setCustomSourceTransformer is not a function`
**Cause:** `expo-asset` version 11.x incompatible with SDK 54
**Fix:** `npm install expo-asset@~10.0.0 expo-font@~13.0.0`

### 7. Expo Router version mismatch
**Error:** Various routing errors
**Cause:** `expo-router@5.0.7` is for SDK 55, not SDK 54
**Fix:** `npm install expo-router@~4.0.0`

### 8. Missing `expo-keep-awake`
**Error:** `useOptionalKeepAwake is not a function`
**Cause:** Peer dependency of Expo not installed
**Fix:** `npm install expo-keep-awake`

### 9. Invalid MaterialCommunityIcons names
**Error:** Runtime errors in profile page
**Cause:** `child-care`, `add`, `notifications`, `security`, `help` are not valid MCI names
**Fix:** Replace with `child`, `plus`, `bell`, `shield-lock`, `help-circle`

### 10. Missing runtime env validation
**Error:** Silent failures when Supabase URL undefined
**Cause:** No null check on `process.env.EXPO_PUBLIC_SUPABASE_URL`
**Fix:** Add throw at module load if env vars missing

### 11. `Unsupported class file major version 70` (Gradle)
**Error:** `BUG! exception in phase 'semantic analysis'`
**Cause:** Java 26 installed, React Native needs Java 17
**Fix:** `sudo archlinux-java set java-17-openjdk`

### 12. Android SDK not found
**Error:** `ANDROID_HOME not set`
**Cause:** Android SDK at `/opt/android-sdk` but no env var
**Fix:** `export ANDROID_HOME=/opt/android-sdk` + add to `~/.zshrc`

### 13. NDK license not accepted
**Error:** `LicenceNotAcceptedException: ndk;27.1.12297006`
**Cause:** NDK license not accepted in sdkmanager
**Fix:** `$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses --sdk_root=$ANDROID_HOME`

---

## Package Versions (SDK 54 Compatible)

| Package | Version | Notes |
|---|---|---|
| expo | ~54.0.0 | SDK 54 |
| expo-router | ~4.0.0 | NOT ~5.0.0 |
| expo-asset | ~10.0.0 | NOT ~11.0.0 |
| expo-font | ~13.0.0 | NOT ~14.0.0 |
| @expo/vector-icons | ^14.0.0 | NOT ^15.0.3 |
| react | 19.0.0 | SDK 54 |
| react-native | 0.79.2 | SDK 54 |
| expo-keep-awake | ~14.0.0 | Required by Expo |

---

## Environment Setup

```bash
# Java
sudo archlinux-java set java-17-openjdk

# Android SDK
export ANDROID_HOME=/opt/android-sdk
export PATH=$ANDROID_HOME/platform-tools:$PATH
# Add to ~/.zshrc

# Accept licenses
$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses --sdk_root=$ANDROID_HOME

# Build
npx expo run:android
```

---

## Additional Fixes (Web + SSR)

### 14. `crypto.randomUUID` not available (Hermes + web)
**Error:** `TypeError: crypto.randomUUID is not a function`
**Cause:** Hermes engine (used by Expo) doesn't have Web Crypto API
**Fix:** Polyfill in `polyfills.js` — fallback to UUID generation with `Math.random()`

### 15. `uuidv4` from expo-modules-core not found
**Error:** `(0 , _expoModulesCore.uuidv4) is not a function`
**Cause:** `expo-linking@7.0.5` bundles its own `expo-constants` that imports `uuidv4` from `expo-modules-core` — the native bridge function isn't available in SDK 52 + Expo Go 54
**Fix:** Patch `node_modules/expo-linking/node_modules/expo-constants/build/ExponentConstants.web.js` — inline `uuidv4` with `crypto.randomUUID()` fallback

### 16. `window is not defined` (SSR)
**Error:** `ReferenceError: window is not defined` in `ExponentConstants.web.js`
**Cause:** Expo Router renders on server first (SSR) — `window`, `navigator`, `localStorage` don't exist
**Fix:** Add `typeof window !== 'undefined'` checks before all browser API references

### 17. Supabase asyncStorage SSR error
**Error:** `ReferenceError: window is not defined` in `AsyncStorage.js`
**Cause:** Supabase client initializes at module load time (SSR) — `asyncStorage` uses `window.localStorage`
**Fix:** Lazy-load AsyncStorage via Proxy pattern — defer to client-side only

---

## Key Lessons

1. **Expo Go version matters** — SDK 55 requires newer Expo Go than what's in the app store
2. **Package versions must match SDK** — expo-router ~5.0.0 is for SDK 55, not 54
3. **Java version matters** — React Native needs Java 17, not 26
4. **Android SDK needs license acceptance** — sdkmanager --licenses is required
5. **Permissions matter** — SDK directory must be writable by the build user
6. **Missing peer dependencies** — expo-keep-awake, expo-linking, expo-constants are required but not auto-installed
7. Icon names must match the library — MaterialCommunityIcons uses specific names, not all Material Icons names
8. `node_modules` patches are temporary — overwritten on `npm install`, need postinstall script
9. Expo SDK 52 + Expo Go 54.0.7 = incompatible native bridge for `uuidv4`
10. SSR requires `typeof window` checks for all browser APIs
11. `useLayoutEffect` warnings on web are harmless — React Navigation SSR support
12. **Always reference the wiki before debugging** — we already documented these patterns

---

## Related

- [[concepts/smart-parenting-app-tech-stack]] — Full tech stack documentation
- [[concepts/mldc-mobile-development-lifecycle]] — MDLC methodology
