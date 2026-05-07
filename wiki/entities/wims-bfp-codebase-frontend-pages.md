---
id: wims-bfp-codebase-frontend-pages-001
type: entity
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
  - nextjs
  - pwa
related:
  - entities/wims-bfp-codebase-api-endpoints
  - concepts/wims-bfp-codebase-offline-pwa
  - sources/wims-bfp-codebase/wims-bfp-codebase-architecture-summary
---

# Frontend Pages

Next.js 16 App Router. All pages in `src/frontend/src/app/`.

## Public Pages

| Route | Purpose | Auth Required |
|-------|---------|---------------|
| `/` | Landing page | No |
| `/report` | Civilian incident submission | No |

## Authenticated Pages

| Route | Purpose | Role |
|-------|---------|------|
| `/dashboard` | Role-based redirect hub | Any |
| `/dashboard/regional` | Regional encoder dashboard | REGIONAL_ENCODER |
| `/dashboard/analyst` | Analyst dashboard (analytics) | NATIONAL_ANALYST |
| `/incidents/create` | Create new incident | REGIONAL_ENCODER |
| `/incidents/triage` | Pending incidents queue | NATIONAL_VALIDATOR |
| `/admin/system` | System admin dashboard | SYSTEM_ADMIN |
| `/profile` | User self-service profile | Any |

## Key Components

| Component | Path | Purpose |
|-----------|------|---------|
| `IncidentForm.tsx` | `components/` | Main incident data entry (60KB) |
| `HeatmapViewer.tsx` | `components/analytics/` | Leaflet-based heatmap |
| `TrendCharts.tsx` | `components/analytics/` | Chart.js trend visualization |
| `NetworkStatusIndicator.tsx` | `components/` | Offline/online status indicator |
| `MapPickerInner.tsx` | `components/` | Leaflet map for location pinning |

## Key Libraries

| Library | Path | Purpose |
|---------|------|---------|
| `offlineStore.ts` | `lib/` | IndexedDB offline queue (64 lines) |
| `api.ts` | `lib/` | API client with JWT handling |
| `edgeFunctions.ts` | `lib/` | Edge function stubs |

## Service Worker

`public/sw.js` (141 lines) — Background Sync handler for offline incident queue.

## Related

- [[entities/wims-bfp-codebase-api-endpoints]] — routes these pages call
- [[concepts/wims-bfp-codebase-offline-pwa]] — offline capabilities
- [[concepts/wims-bfp-codebase-data-flow]] — end-to-end data pipeline
