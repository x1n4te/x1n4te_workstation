# Smart Parenting App — MainApplication.kt Iterative AI Corruption (Failure Mode #3)

**Source:** Session log — smart-parenting-app Android build fix
**Date:** 2026-04-26
**Category:** operational
**Confidence:** high
**Tags:** [expo-sdk-54, android, kotlin, react-native, failure-mode-3, iterative-corruption, smart-parenting-app]

---

## Context

Smart Parenting App (commissioned project, React Native/Expo SDK 54, bare workflow) failed to build with a Kotlin compilation error in `MainApplication.kt`. The error manifested as a type mismatch: `ExpoReactHostFactory.createFromReactNativeHost()` was being called with a `List<ReactPackage>` where a `ReactNativeHost` was expected.

---

## What Went Wrong

The file had been iteratively edited by an AI coding agent across multiple sessions. Each iteration compounded the error rather than resolving it. The root cause was a **version mismatch** between the Kotlin source and the Expo SDK tooling:

### Timeline of Corruption

| Iteration | What changed | Result |
|---|---|---|
| Original (SDK 52) | `MainApplication` using legacy `ReactNativeHost` pattern | Worked at SDK 52 |
| Iteration 1 | Partial SDK 54 upgrade — `expo-modules-core` updated, android/ regenerated | `ExpoReactHostFactory` introduced |
| Iteration 2 | AI replaced the host creation with `ExpoReactHostFactory.createFromReactNativeHost()` — but this is an **SDK 55 API** | Type mismatch introduced |
| Iteration 3 | AI tried to "fix" the type error by wrapping the package list differently | Made it worse |
| Iteration N | More iterations → more errors → each compile attempt produced garbage | Degraded per SlopCodeBench trajectory |

### The Specific API Error

**Wrong (SDK 55 API — applied to SDK 54 project):**
```kotlin
override val reactNativeHost: ReactNativeHost by lazy {
    DefaultReactHost.getDefaultReactHost(
        applicationContext,
        ExpoReactHostFactory.createFromReactNativeHost(
            applicationContext,
            PackageList(this).packages.apply { ... }
        )
    )
}
```

**Correct (SDK 54 API — from official template):**
```kotlin
override val reactNativeHost: ReactNativeHost = ReactNativeHostWrapper(
    this,
    object : DefaultReactNativeHost(this) {
        override fun getPackages(): List<ReactPackage> =
            PackageList(this@MainApplication).packages.apply { ... }
        override fun getJSMainModuleName(): String = ".expo/.virtual-metro-entry"
        override fun getUseDeveloperSupport(): Boolean = BuildConfig.DEBUG
        override val isNewArchEnabled: Boolean = BuildConfig.IS_NEW_ARCHITECTURE_ENABLED
    }
)

override val reactHost: ReactHost
    get() = ReactNativeHostWrapper.createReactHost(applicationContext, reactNativeHost)
```

### Root Cause Analysis

The AI applied `ExpoReactHostFactory.createFromReactNativeHost()` — an SDK 55 API — to an SDK 54 project. The SDK 54 project has `expo-modules-core 3.0.15`, which does not have this method. The method exists only in SDK 55 (`expo-modules-core` ≥ 4.0.0).

The AI never fetched the official SDK 54 template for comparison. It reasoned from:
1. The error message ("type mismatch")
2. The Expo class name it could see (`ExpoReactHostFactory`)
3. Its internal knowledge of the Expo API

This is **exactly** Failure Mode #3 in action: the AI had the right intention (fix the ReactHost setup for newer Expo) but produced code that **doesn't work** because the feedback loop was broken. No type checker caught the version mismatch because the AI was writing code outside a CI context.

---

## How It Was Fixed

1. Ran `curl` to fetch the **canonical SDK 54 bare template** directly from GitHub (`expo/expo` repo, `sdk-54` branch)
2. Compared the template against the corrupted file — found 3 structural differences
3. Applied the SDK 54 template pattern exactly
4. Build succeeded in 22s with only deprecation warnings

**Key insight:** The fix did not come from AI reasoning. It came from **fetching a known-good reference** and doing a diff. This is the empirical antidote to iterative degradation: a canonical external source that cannot drift.

---

## Evidence of Iterative Degradation

The corruption pattern matches SlopCodeBench findings:

| Signal | Observed | SlopCodeBench finding |
|---|---|---|
| Verbosity increase | Each iteration added more boilerplate to hide the error | Agent code 2.2x more verbose than human code |
| Structural erosion | `createFromReactNativeHost` was wrapped in increasingly complex nesting | Erosion rises in 80% of trajectories |
| No reference to canonical source | AI never fetched the SDK 54 template | Anti-slop prompts don't change slope |

---

## Why AI Iteration Made It Worse

1. **No shared design concept**: The AI didn't know the project was SDK 54 (not 55)
2. **No ubiquitous language**: "ReactHost" vs "ReactNativeHost" — the AI conflated the two
3. **Outrunning headlights**: Each iteration produced more code before checking against the real API
4. **No TDD**: No test existed to catch this at compile time — it only failed at the Android build step

---

## Lessons for WIMS-BFP Multi-Agent Orchestrator

This is a concrete example for the WIMS-BFP orchestrator design:

| Safeguard | How it applies here |
|---|---|
| **Reference-first protocol** | Before touching a config file, fetch the canonical source |
| **Version pinning gate** | Reject changes that reference APIs not in the declared dependency versions |
| **Build verification per step** | Each iteration should produce a buildable artifact, not just syntactically correct code |
| **Canonical source diff** | Always diff against the official template, not against the previous corrupted state |

---

## Related

- [[concepts/feedback-loops-ai-coding]] — failure mode #3 concept
- [[concepts/slopcodebench-iterative-degradation]] — empirical evidence
- [[sources/operational/2026-04-24-spa-sdk55-schema-migration-session]] — SDK 55 upgrade attempt on same project
