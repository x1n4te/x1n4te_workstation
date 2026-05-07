---
id: spa-sdk55-schema-migration-session-2026-04-24
type: source
created: 2026-04-24
updated: 2026-04-24
last_verified: 2026-04-24
review_after: 2026-05-24
stale_after: 2026-07-23
confidence: high
source_refs:
  - /home/xynate/local-projects/smart-parenting-app/package.json
  - /home/xynate/local-projects/smart-parenting-app/lib/database.types.ts
  - /home/xynate/local-projects/smart-parenting-app/lib/image.ts
  - /home/xynate/local-projects/smart-parenting-app/lib/notifications.ts
  - /home/xynate/local-projects/smart-parenting-app/android
  - /home/xynate/local-projects/smart-parenting-app/ios
status: active
tags:
  - smart-parenting-app
  - mobile-dev
  - expo
  - react-native
  - supabase
  - database
  - operational
related:
  - concepts/smart-parenting-app-tech-stack
  - concepts/smart-parenting-app-tech-stack-details
  - concepts/expo-local-notifications
  - concepts/react-native-text-input-centering
---

# Smart Parenting App — SDK 55 + Supabase Schema Migration Session

## Scope

Upgraded the Smart Parenting App from Expo SDK 52 / partial SDK 54 state to Expo SDK 55, and fixed the `scheduled_activities.food_groups` schema/type mismatch.

This was treated as a controlled platform migration, not a blind `expo@latest` upgrade. Existing app feature work was preserved; no commit was made.

## Schema Fix

The missing `scheduled_activities.food_groups` issue was not only a generated TypeScript cache problem. Remote Supabase generated types initially showed the `scheduled_activities` table without `food_groups`, and local `lib/database.types.ts` did not include `scheduled_activities` at all.

Actions:
- Applied the existing additive migration `database/migration_scheduled_activities_v3.sql` to the linked Supabase project.
- Regenerated types with linked Supabase schema output into `lib/database.types.ts`.
- Verified `scheduled_activities.food_groups` appears in Row, Insert, and Update types as `string[] | null` / optional `string[] | null`.

## SDK 55 Package State

Verified package set after upgrade:

| Package | Version |
|---|---:|
| Expo | `~55.0.0` |
| React | `19.2.0` |
| React Native | `0.83.6` |
| Expo Router | `~55.0.13` |
| Expo Notifications | `~55.0.20` |
| Expo File System | `~55.0.17` |
| Expo System UI | `~55.0.16` |
| TypeScript | `~5.9.2` |
| @types/react | `~19.2.10` |

`expo-system-ui` was added because SDK 55 prebuild requires it when `userInterfaceStyle` is configured.

## Compatibility Fixes

- Removed invalid `expo.main` from `app.json`; Expo Router entry remains managed through package/app entry behavior.
- Updated legacy file upload import in `lib/image.ts` to `expo-file-system/legacy` so `readAsStringAsync` and `EncodingType.Base64` remain available under SDK 55.
- Updated foreground notification handler in `lib/notifications.ts` from `shouldShowAlert` to SDK 55-compatible `shouldShowBanner` + `shouldShowList`.
- Added `MonthWeekRange` typing in `app/(tabs)/history.tsx` so full TypeScript no longer fails on implicit `weeks` type inference.
- Added a type-only local `Deno` declaration in `supabase/functions/analyze-child/index.ts` so repo-level TypeScript can verify the Edge Function without changing runtime behavior.

## Native Regeneration

Ran Expo prebuild cleanly for SDK 55 native folders:

```bash
CI=1 npx expo prebuild --clean --no-install
```

Android native output now uses SDK 55/RN 0.83 generated configuration, including Android SDK 36 compile/target settings and `edgeToEdgeEnabled=true`.

## `@expo/dom-webview` Guardrail

SDK 55 lockfile metadata references `@expo/dom-webview` transitively through Expo internals, but the physical package was not installed after the project postinstall cleanup.

Verified state:
- `node_modules/@expo/dom-webview` is absent.
- App/native source grep returned zero `@expo/dom-webview` matches.
- iOS and Android Metro exports succeeded with `@expo/dom-webview` absent.
- Android Gradle debug assemble succeeded without the historical missing `expo-module-gradle-plugin` failure.

## Verification

Passed:
- `npx expo install --check`
- `npx tsc --noEmit`
- `git diff --check`
- Forbidden pattern grep: no `Alert.alert`, no `fetch().blob()`, no direct `from 'expo-file-system'`, no app/native `@expo/dom-webview`
- `npx expo export --platform ios --output-dir /tmp/spa-expo-export-ios --no-minify`
- `npx expo export --platform android --output-dir /tmp/spa-expo-export-android --no-minify`
- `./gradlew :app:assembleDebug -x lint -x test` from `android/`

Known Expo Doctor result:
- `17/18` checks pass.
- Remaining warning: native `android/` and `ios/` folders exist while app config contains native properties. This is expected for a prebuild-managed repo; rerun `npx expo prebuild --clean --no-install` after future native config edits.

## Notes for Future Work

- Do not reintroduce physical `node_modules/@expo/dom-webview`.
- Keep using `expo-file-system/legacy` for current base64 upload code until the upload path is deliberately migrated to the new SDK 55 file-system API.
- Re-run prebuild after changes to `orientation`, `userInterfaceStyle`, `ios`, `android`, `plugins`, or `scheme` in `app.json`.
- iOS native compilation still requires macOS/Xcode; Linux verification covered Metro iOS export and Android native Gradle build.
