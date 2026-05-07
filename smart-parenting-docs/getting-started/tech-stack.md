# Tech Stack Overview

The Smart Parenting App is built with modern, open-source technologies chosen for reliability, developer productivity, and zero server costs.

---

## Frontend

| Technology             | Purpose                                                               |
| ---------------------- | --------------------------------------------------------------------- |
| **Expo SDK 55**        | React Native framework — handles builds, OTA updates, and native APIs |
| **Expo Router**        | File-based routing — screens are files in the `app/` directory        |
| **React Native Paper** | Material Design UI components                                         |
| **Zustand**            | Lightweight state management                                          |
| **AsyncStorage**       | Persistent local storage for selected child and app state             |

---

## Backend

| Technology | Purpose |
|------------|---------|
| **Supabase** | Open-source Firebase alternative — PostgreSQL database, auth, and storage |
| **PostgreSQL** | Primary database with Row-Level Security (RLS) |
| **Supabase Edge Functions** | Serverless TypeScript functions (Deno runtime) for AI processing |
| **Supabase Auth** | Email/password authentication with JWT sessions |
| **Supabase Storage** | Avatar image uploads |

---

## AI

| Technology | Purpose |
|------------|---------|
| **OpenRouter** | API gateway for LLMs — provides access to multiple models |
| **inclusionai/ling-2.6-1t:free** | 1-trillion parameter Mixture-of-Experts model (free tier) |
| **Zero-shot prompting** | No fine-tuning — the model reasons over structured data injected into the prompt |

---

## Notifications

| Technology | Purpose |
|------------|---------|
| **Expo Notifications** | Local scheduled push notifications — bedtime, meal, and activity reminders |

---

## Development Tools

| Technology | Purpose |
|------------|---------|
| **TypeScript** | Strict typing across the entire codebase |
| **EAS (Expo Application Services)** | Cloud builds and over-the-air updates |
| **Supabase CLI** | Local development, migrations, and Edge Function deployment |

---

## Why This Stack?

1. **Zero server costs** — Supabase free tier + OpenRouter free tier = ₱0 infrastructure cost.
2. **Single codebase** — One React Native app runs on both iOS and Android.
3. **Type safety** — Supabase generates TypeScript types from the database schema.
4. **Privacy by design** — PostgreSQL RLS ensures users can only access their own data.
5. **Scalable AI** — OpenRouter abstraction means we can swap to GPT-4o or Claude without changing app code.
