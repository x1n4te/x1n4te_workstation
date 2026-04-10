---
id: smart-parenting-app-tech-stack-001
type: concept
created: 2026-04-10
updated: 2026-04-10
last_verified: 2026-04-10
review_after: 2026-07-10
stale_after: 2026-10-09
confidence: high
status: active
tags:
  - react-native
  - expo
  - firebase
  - supabase
  - openrouter
  - mobile-development
  - commission
related:
  - concepts/llm-applied-learning-path
  - entities/hermes-agent-setup
---

# Smart Parenting App — Tech Stack & Documentation

**Project:** Smart Parenting App with AI-Based Child Activity Monitoring
**Client:** Freelance commission (₱12K)
**Deadline:** 1 week
**Platforms:** Android + iOS

---

## Tech Stack Overview

| Layer | Technology | Role |
|---|---|---|
| Mobile | React Native + Expo SDK 52 | Cross-platform Android + iOS app |
| Auth | Firebase Auth | Email/password + social login |
| Database | Supabase (PostgreSQL) | Cloud database + realtime |
| AI | OpenRouter API | Activity analysis + recommendations |
| Build | Expo EAS Build | Cloud APK/IPA builds |
| Backend (optional) | FastAPI | If needed beyond Firebase |

---

## React Native + Expo

**What:** Framework for building native mobile apps with JavaScript/TypeScript. Expo adds tooling, cloud builds, and pre-built modules.

**Key docs:**
- Expo docs: https://docs.expo.dev/
- Expo Router (file-based routing): https://docs.expo.dev/router/introduction/
- Expo SDK 52 overview: https://medium.com/@onix_react/what-to-expo-from-expo-sdk-52
- React Native Directory (library search): https://reactnative.directory/

**Quick start:**
```bash
npx create-expo-app@latest smart-parenting-app
cd smart-parenting-app
npx expo install expo-router expo-dev-client
npx expo start
```

**Key concepts:**
- File-based routing (like Next.js App Router)
- Expo Go for development (phone simulator)
- EAS Build for production APKs
- OTA updates (push code changes without app store)

**Why Expo over bare React Native:**
- No Android Studio / Xcode setup for development
- Cloud builds via EAS
- Pre-built modules (camera, notifications, storage)
- Faster iteration cycle

---

## Firebase Auth

**What:** Google's authentication service. Handles email/password, social login, MFA. Free tier: 10K monthly active users.

**Key docs:**
- Firebase console: https://console.firebase.google.com/
- Firebase Auth docs: https://firebase.google.com/docs/auth
- Expo + Firebase guide: https://docs.expo.dev/guides/using-firebase/
- React Native Firebase setup (YouTube): https://www.youtube.com/watch?v=H-vG4G8eKNE

**Setup:**
```bash
# 1. Create project at console.firebase.google.com
# 2. Enable Email/Password auth
# 3. Add Android app → download google-services.json
# 4. Add iOS app → download GoogleService-Info.plist
# 5. Install in Expo project
npx expo install @react-native-firebase/app @react-native-firebase/auth
```

**Key features for this project:**
- Email/password signup + login
- Session management (automatic token refresh)
- Password reset flow
- Free tier covers expected usage

**Alternative:** Supabase Auth (integrated with Supabase DB, simpler setup)

---

## Supabase

**What:** Open-source Firebase alternative. PostgreSQL database with auth, realtime, storage, and edge functions. Free tier: 500MB database, 50K monthly active users.

**Key docs:**
- Supabase docs: https://supabase.com/docs/
- React Native quickstart: https://supabase.com/docs/guides/auth/quickstarts/react-native
- Supabase JS SDK: https://supabase.com/docs/reference/javascript/start
- Database guide: https://supabase.com/docs/guides/database

**Quick start:**
```bash
# 1. Create project at supabase.com
# 2. Get project URL + anon key
# 3. Install in React Native
npx expo install @supabase/supabase-js @react-native-async-storage/async-storage react-native-url-polyfill
```

**Key features for this project:**
- PostgreSQL database (activity logs, child profiles, recommendations)
- Row Level Security (parents only see their children's data)
- Realtime subscriptions (live dashboard updates)
- Storage (child profile photos)
- Auth (alternative to Firebase — can use either)

**Why Supabase over Firebase:**
- PostgreSQL (you already know it from WIMS-BFP)
- Row Level Security (you already know RLS)
- Open source (no vendor lock-in)
- Realtime built-in
- Free tier is generous

---

## OpenRouter API

**What:** Unified API for 400+ AI models. One API key, access to GPT-4, Claude, Gemini, Llama, Qwen, and more. Pay-per-use, free tier available.

**Key docs:**
- OpenRouter docs: https://openrouter.ai/docs/quickstart
- API reference: https://openrouter.ai/docs/api/reference/overview
- Models list: https://openrouter.ai/models
- React Native integration: https://openrouter.ai/docs/guides/community/frameworks-and-integrations-overview

**Quick start:**
```javascript
const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + OPENROUTER_API_KEY,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'google/gemma-4-26b-a4b-it:free',  // free model
    messages: [{role: 'user', content: prompt}],
  }),
});
```

**Key features for this project:**
- Free models available (Gemma, Llama, Qwen)
- Structured output support (JSON mode)
- Same API as OpenAI (drop-in compatible)
- Pay-per-token (no subscription needed)
- Auto-fallback (if one provider is down, routes to another)

**Why OpenRouter over direct providers:**
- One API key for all models
- Free tier covers development + testing
- You already use it for WIMS-BFP (Nous Portal)
- Easy to switch models without code changes

---

## Expo EAS Build

**What:** Cloud build service for Expo/React Native apps. Builds APK (Android) and IPA (iOS) without local native build tools.

**Key docs:**
- EAS Build docs: https://docs.expo.dev/build/introduction/
- Build profiles: https://docs.expo.dev/build/eas-json/
- Android build: https://docs.expo.dev/build/setup/
- iOS build: https://docs.expo.dev/build-reference/ios-build/
- Submit to stores: https://docs.expo.dev/submit/introduction/

**Quick start:**
```bash
# 1. Install EAS CLI
npm install -g eas-cli

# 2. Login
eas login

# 3. Configure
eas build:configure

# 4. Build Android APK
eas build --platform android --profile preview

# 5. Build iOS IPA (requires Apple Developer account)
eas build --platform ios --profile preview
```

**Build profiles (eas.json):**
```json
{
  "build": {
    "development": { "developmentClient": true, "distribution": "internal" },
    "preview": { "distribution": "internal" },
    "production": {}
  }
}
```

**Key features:**
- Cloud builds (no local Android Studio / Xcode needed)
- Automatic credential management (keystores, provisioning profiles)
- Parallel builds (Android + iOS simultaneously)
- Build caching (faster subsequent builds)
- Free tier: 30 builds/month

---

## React Native Paper (UI Library)

**What:** Material Design components for React Native. Pre-built buttons, forms, cards, navigation.

**Docs:** https://callstack.github.io/react-native-paper/

**Install:**
```bash
npx expo install react-native-paper react-native-safe-area-context
```

**Why:** Pre-built Material Design components. Saves time on UI development. Accessible by default.

---

## react-native-chart-kit (Charts)

**What:** Pre-built chart components for React Native. Line, bar, pie charts.

**Docs:** https://github.com/indiespirit/react-native-chart-kit

**Install:**
```bash
npx expo install react-native-chart-kit react-native-svg
```

**Why:** Pre-built charts for activity reports. Minimal config, good enough for a prototype.

---

## Architecture Diagram

```
┌─────────────────────────────────┐
│   React Native App (Expo)       │
│   ┌─────────┐  ┌─────────────┐ │
│   │ Firebase │  │  Supabase   │ │
│   │  Auth    │  │  Database   │ │
│   └─────────┘  └─────────────┘ │
│          │           │          │
│          └─────┬─────┘          │
│                │                │
│         ┌──────┴──────┐         │
│         │  Activity   │         │
│         │  Logging    │         │
│         └──────┬──────┘         │
│                │                │
│         ┌──────┴──────┐         │
│         │  OpenRouter │         │
│         │  AI Engine  │         │
│         └──────┬──────┘         │
│                │                │
│         ┌──────┴──────┐         │
│         │ AI Reports  │         │
│         │ + Alerts    │         │
│         └─────────────┘         │
└─────────────────────────────────┘
```

---

## Current Versions (SDK 52)

| Package | Version | Documentation |
|---|---|---|
| Expo | 52.0.49 | https://docs.expo.dev/ |
| React Native | 0.76.3 | https://reactnative-archive-august-2025.netlify.app/docs/0.76/getting-started |
| Expo Router | 4.0.22 | https://docs.expo.dev/router/introduction/ |
| React Native Paper | 5.12.0 | https://callstack.github.io/react-native-paper/docs/guides/getting-started/ |
| Supabase JS | 2.49.0 | https://supabase.com/docs/reference/javascript/start |

### Key Documentation Links (Exact Versions)

| Technology | Link | What |
|---|---|---|
| Expo SDK 52 overview | https://medium.com/@onix_react/what-to-expect-from-expo-sdk-52-48c28c07db6a | Features, breaking changes, new architecture |
| Expo SDK 52 video | https://www.youtube.com/watch?v=gQqE55rkHO0 | Deep dive into SDK 52 updates |
| Expo Router v4 docs | https://docs.expo.dev/versions/latest/sdk/router/ | API reference, hooks, navigation |
| Expo Router intro | https://docs.expo.dev/router/introduction/ | File-based routing concepts |
| Expo Router tutorial | https://www.youtube.com/watch?v=FWYiG6OIEJw | Login → Dashboard → Profile flow |
| React Native 0.76 release | https://reactnative.dev/blog/2024/10/23/release-0.76-new-architecture | New architecture by default |
| React Native 0.76 docs | https://reactnative-archive-august-2025.netlify.app/docs/0.76/getting-started | Getting started guide |
| React Native Paper v5 | https://callstack.github.io/react-native-paper/docs/guides/getting-started/ | Setup, PaperProvider, components |
| React Native Paper v5 guide | https://callstack.github.io/react-native-paper/docs/guides/migration-guide-to-5.0/ | Material You design |
| Supabase React Native | https://supabase.com/docs/guides/auth/quickstarts/react-native | Quickstart guide |
| Expo tutorial | https://docs.expo.dev/tutorial/introduction/ | Official step-by-step tutorial |
| Expo EAS Build | https://docs.expo.dev/build/introduction/ | Cloud build for Android/iOS |

---

## Development Resources

### React Native + Expo Tutorials

| Resource | Type | Link |
|---|---|---|
| Expo Tutorial (official) | Docs | https://docs.expo.dev/tutorial/introduction/ |
| React Native Full Course 2026 (Expo) | Video | https://www.youtube.com/watch?v=RdJhqaOIWn0 |
| React Native Full Course 2026 (publish + monetize) | Video | https://www.youtube.com/watch?v=4nVoLX2taFg |
| React Native Tutorial: Build 1st App in 3 Hours | Guide | https://tech-insider.org/react-native-tutorial-mobile-app-complete-guide-2026/ |
| Expo SDK 52 overview | Blog | https://medium.com/@onix_react/what-to-expo-from-expo-sdk-52 |

### Supabase + React Native

| Resource | Type | Link |
|---|---|---|
| Supabase React Native quickstart (official) | Docs | https://supabase.com/docs/guides/auth/quickstarts/react-native |
| Supabase Setup in React Native Expo 2026 | Video | https://www.youtube.com/watch?v=o5C6cEEAKkI |
| Pocket Backend: React Native CRUD with Supabase | Blog | https://weblianz.com/blog/pocket-backend-react-native-crud-with-supabase |
| Build CRUD App with React + Supabase | Guide | https://adevait.com/react/building-crud-app-with-react-js-supabase |

### Firebase Auth + React Native

| Resource | Type | Link |
|---|---|---|
| Firebase Setup in Expo (official) | Docs | https://docs.expo.dev/guides/using-firebase/ |
| Firebase Setup in React Native Expo 2026 | Video | https://www.youtube.com/watch?v=H-vG4G8eKNE |
| React Native Firebase Tutorial (2025) | Playlist | https://www.youtube.com/playlist?list=PLuP3JaGUSq82b23OQEiUoueDTGVTYdVra |

### EAS Build + Deployment

| Resource | Type | Link |
|---|---|---|
| EAS Build docs (official) | Docs | https://docs.expo.dev/build/introduction/ |
| Build profiles config | Docs | https://docs.expo.dev/build/eas-json/ |
| Submit to app stores | Docs | https://docs.expo.dev/submit/introduction/ |
| Expo dev workflow 2026 | Blog | https://irfanqutab.dev/blog/expo-developer-workflow-2026 |

### Mobile App Architecture

| Resource | Type | Link |
|---|---|---|
| 9 Mobile App Architecture Best Practices | Guide | https://nextnative.dev/blog/mobile-app-architecture-best-practices |
| React Native Architecture (2026) | Blog | https://medium.com/@silverskytechnology/react-native-architecture-explained-2026-edition |
| React Design Patterns 2025 | Guide | https://www.telerik.com/blogs/react-design-patterns-best-practices |

### AI Integration

| Resource | Type | Link |
|---|---|---|
| OpenRouter quickstart | Docs | https://openrouter.ai/docs/quickstart |
| OpenRouter API reference | Docs | https://openrouter.ai/docs/api/reference/overview |
| OpenRouter models catalog | List | https://openrouter.ai/models |
| OpenRouter React Native integration | Guide | https://openrouter.ai/docs/guides/community/frameworks-and-integrations-overview |

---

## Related

- [[concepts/llm-applied-learning-path]] — Applied LLMs learning path
- [[entities/hermes-agent-setup]] — Hermes agent setup
