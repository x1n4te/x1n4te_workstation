---
id: wims-bfp-codebase-offline-pwa-001
type: concept
created: 2026-04-21
updated: 2026-04-21
last_verified: 2026-04-21
review_after: 2026-06-21
stale_after: 2026-10-21
confidence: high
source_refs:
  - raw/sources/wims-bfp-codebase/docs/FRONTEND.md
status: active
tags:
  - wims-bfp
  - frontend
  - pwa
  - offline
related:
  - entities/wims-bfp-codebase-frontend-pages
  - concepts/wims-bfp-codebase-data-flow
  - concepts/wims-bfp-sprint-timeline
---

# Offline PWA

Service Worker + IndexedDB for offline-first incident management. Constitution mandate.

## Architecture

The offline store is a **queue buffer**, not a database mirror. Encoders create incidents offline → stored in IndexedDB → on reconnect, queue flushes to backend → backend is source of truth.

## Components

| Component | File | Lines | Status |
|-----------|------|-------|--------|
| Offline Store | `src/frontend/src/lib/offlineStore.ts` | 64 | Queue/getPending/markSynced works |
| Service Worker | `src/frontend/public/sw.js` | 141 | Background Sync handler exists |
| Network Indicator | `src/frontend/src/components/NetworkStatusIndicator.tsx` | — | Shows online/offline status |

## Current Capabilities

- ✅ Queue incident creation offline (IndexedDB via `idb`)
- ✅ Get pending incidents from queue
- ✅ Mark incident as synced
- ✅ Network status indicator UI

## Missing (Sprint 1)

- ❌ Queue encryption (AES-256-GCM before IndexedDB write)
- ❌ Queue management UI (view/edit/delete queued items)
- ❌ Integrity verification (AES-GCM tag check before upload)
- ❌ Atomic sync (backend transaction per incident)
- ❌ Exponential backoff retry (max 5) in SW
- ❌ Frontend toast handler for sync events

## Related

- [[entities/wims-bfp-codebase-frontend-pages]] — frontend page architecture
- [[concepts/wims-bfp-sprint-timeline]] — Sprint 1 schedule for offline features
- [[concepts/wims-bfp-codebase-data-flow]] — sync pipeline
