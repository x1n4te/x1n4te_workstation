---
title: AI Insights Display
created: 2026-04-25
updated: 2026-04-25
type: concept
tags: [ai-insights, feature, ui-ux]
sources: [raw/feature-ai-insights-display.md, raw/changelog-2026-04-25.md]
---

# AI Insights Display

**Route:** `app/(tabs)/ai.tsx`  
**Role:** Recommendation card UI — filtered, ranked, and visually annotated insights.

See [[ai-insights-architecture]] for the backend Edge Function, model, and normalizer. Insights are surfaced to the user via [[screen-dashboard]] recommendation cards.

---

## What Changed

The AI Insights recommendations screen was redesigned to show **more focused, contextual information** — limiting noise while helping parents instantly identify the most relevant advice.

---

## Date Display on Every Recommendation

Every recommendation card now shows the exact generation date (e.g., "Apr 25, 2026") in the bottom-right footer.

---

## Three-Per-Category Limit

Instead of showing *all* recommendations, the screen shows **only the 3 most recent per category** (Sleep, Meals, Education, Screen Time, General).

### Algorithm
```
1. Group all recommendations by category
2. Within each category, sort by date (newest first)
3. Keep only the top 3
4. Assign recency rank (0=Latest, 1=2nd Latest, 2=Oldest)
5. Sort final list by category name → date
```

All recommendations are still stored in Supabase. Only the *display* is limited.

---

## Recency Badges

Color-coded labels indicating freshness **within the category**:

| Badge | Color | Meaning |
|-------|-------|---------|
| **Latest** | Green (`#10B981`) | Most recent in this category |
| **2nd Latest** | Amber (`#F59E0B`) | Second most recent |
| **Oldest** | Gray (`#94A3B8`) | Third most recent (oldest of the 3 shown) |

> "Oldest" does **not** mean outdated — it's the third-most-recent insight in that category.

---

## Filter Behavior

When a parent selects a filter (e.g., "Sleep" or "High Priority"):
1. Filter is applied first
2. Then the 3-per-category limit is applied
3. Only the 3 most recent matching recommendations are shown

---

## Technical Summary

### `filtered` useMemo
Returns an array of objects containing both the recommendation and its recency rank:

```typescript
const filtered = useMemo(() => {
  let base = recommendations;
  if (activeFilter !== 'all') {
    // Apply category/priority/insight_type filter
  }

  const grouped = new Map<string, Recommendation[]>();
  for (const rec of base) {
    const cat = rec.category || 'general';
    if (!grouped.has(cat)) grouped.set(cat, []);
    grouped.get(cat)!.push(rec);
  }

  const result: { rec: Recommendation; recencyRank: number }[] = [];
  for (const [cat, list] of grouped) {
    const sorted = [...list].sort(
      (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    );
    const top3 = sorted.slice(0, 3);
    for (let i = 0; i < top3.length; i++) {
      result.push({ rec: top3[i], recencyRank: i });
    }
  }

  result.sort((a, b) => {
    const catA = a.rec.category || 'general';
    const catB = b.rec.category || 'general';
    if (catA !== catB) return catA.localeCompare(catB);
    return new Date(b.rec.created_at).getTime() - new Date(a.rec.created_at).getTime();
  });

  return result;
}, [recommendations, activeFilter]);
```

### Rendering
```tsx
{paginated.map(({ rec, recencyRank }, i) => (
  <RecommendationCard key={rec.id || i} rec={rec} recencyRank={recencyRank} />
))}
```

### Constants
```typescript
const RECENCY_LABELS = ['Latest', '2nd Latest', 'Oldest'];
const RECENCY_COLORS = ['#10B981', '#F59E0B', '#94A3B8'];
```
