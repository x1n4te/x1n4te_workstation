---
title: Smart Parenting App — Overview
created: 2026-04-25
updated: 2026-04-25
type: concept
tags: [architecture, expo, supabase, ui-ux]
sources: [raw/readme-2026-04-25.md]
---

# Smart Parenting App — Overview

Standalone project wiki for the Smart Parenting mobile application (Expo SDK 55 + Supabase). This wiki contains implementation details, architecture decisions, and screen walkthroughs.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Expo SDK 55 |
| Router | Expo Router (file-based) |
| UI | React Native Paper |
| State | Zustand + AsyncStorage persistence |
| Backend | Supabase (PostgreSQL + Edge Functions) |
| Auth | Supabase Auth (email/password) |
| AI | OpenRouter (`inclusionai/ling-2.6-1t:free`) |
| Notifications | Expo Notifications |

---

## Quick Navigation

### Architecture
- [[repo-structure]] — File layout, navigation architecture, config files
- [[database-schema]] — Consolidated Supabase schema, RLS policies, indexes, storage
- [[auth-loading-overlay]] — Root-level auth state machine, redirect delays, z-index overlay

### Screens
- [[screen-dashboard]] — Home tab: greeting, stats grid, scheduled activities, quick log
- [[screen-activities]] — Core data entry: time inputs, chip selectors, dual-mode form
- [[screen-history]] — Read-only activity browser: calendar, filters, stats charts
- [[screen-settings]] — Profile hub, per-child config, account management, FAQ
- [[screen-auth]] — Auth flows, validation, success states

### Features
- [[ai-insights-architecture]] — Zero-shot prompting architecture, Edge Function, normalizer, audit trail
- [[ai-insights-display]] — Recommendation card UI limits and badges
- [[notification-system]] — Per-child toggles, master switch, opt-in defaults
- [[schedule-redirect]] — Instant History tab redirect after schedule creation

---

## Design System Reference

See [[design-system]] for the full token table and usage guidelines.

Quick reference:

| Token | Value | Usage |
|-------|-------|-------|
| Primary | `#FF7F60` | Buttons, active states, spinners |
| Background | `#FEFBF6` | App background |
| Surface | `#FFFDFF` | Cards, modals |
| Error | `#EF4444` | Validation, destructive actions |
| Screen Time | `#FF7F60` | Activity icon/badge |
| Sleep | `#10B981` | Activity icon/badge |
| Meals | `#F59E0B` | Activity icon/badge |
| Education | `#8B5CF6` | Activity icon/badge |
