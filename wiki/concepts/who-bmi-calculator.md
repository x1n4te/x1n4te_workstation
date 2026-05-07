---
id: who-bmi-calculator-001
type: concept
created: 2026-04-18
updated: 2026-04-18
last_verified: 2026-04-18
review_after: 2026-07-18
stale_after: 2026-10-18
confidence: high
source_refs:
  - raw/articles/smart-parenting-app-codebase-2026-04-18
  - lib/bmi.ts
status: active
tags:
  - bmi-calculator
  - mobile-dev
  - smart-parenting-app
  - health
  - pediatrics
  - expo
related:
  - concepts/smart-parenting-app-tech-stack
  - concepts/expo-local-notifications
---

# WHO BMI-for-Age Calculator — Pediatric Assessment

Smart Parenting App implements the WHO Child Growth Standards BMI-for-age assessment for children 2-5 years using the LMS method.

## Why Raw BMI is Useless for Children

A raw BMI of 17 means nothing for a 3-year-old. Pediatric BMI is **age- and gender-adjusted** — the same absolute BMI is "obese" at age 3 but "healthy" at age 10. The app uses WHO's LMS method to compute percentiles.

## LMS Method (WHO Standard)

The LMS method converts raw BMI to a z-score, then to a percentile:

```
z = ((BMI / M)^L - 1) / (L * S)
```

Where:
- **L** = Box-Cox power (skewness correction)
- **M** = Median (50th percentile)
- **S** = Coefficient of variation (spread)

Each parameter is tabulated by **age in months** and **gender** from WHO reference data.

## WHO Reference Tables

The app embeds two lookup tables in `lib/bmi.ts`:

### Boys (24-60 months)
Sample entries:

| Age (mo) | L | M | S |
|---|---|---|---|
| 24 | -0.1581 | 16.4397 | 0.08305 |
| 36 | -0.2784 | 15.9313 | 0.08507 |
| 48 | -0.3375 | 15.8093 | 0.08752 |
| 60 | -0.3594 | 15.9976 | 0.09008 |

### Girls (24-60 months)
Sample entries:

| Age (mo) | L | M | S |
|---|---|---|---|
| 24 | -0.0349 | 16.0696 | 0.08561 |
| 36 | -0.2139 | 15.5336 | 0.08813 |
| 48 | -0.3015 | 15.4116 | 0.09102 |
| 60 | -0.3344 | 15.6371 | 0.09396 |

## Implementation Functions

### `calculateBmi(heightCm, weightKg)`
```typescript
export function calculateBmi(heightCm: number, weightKg: number): number | null {
  if (!heightCm || !weightKg || heightCm <= 0) return null;
  const heightM = heightCm / 100;
  return Math.round((weightKg / (heightM * heightM)) * 10) / 10;
}
```
Returns raw BMI rounded to 1 decimal. Returns null for invalid input.

### `calculateZScore(bmi, ageMonths, gender)`
1. Clamps age to 24-60 months range
2. Looks up L/M/S from gender-specific table
3. Applies LMS formula
4. Returns null if age outside reference range

### `zScoreToPercentile(z)`
Abramowitz-Stegun approximation of the normal CDF:
```typescript
// Returns percentile 0.01 to 99.99
const percentile = 50 * (1 + sign * y);
// y = 1 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t * exp(-z^2/2)
// where t = 1/(1 + p*|z|)
```

### `getCategory(percentile)` — WHO/CDC thresholds

| Percentile | Category |
|---|---|
| < 5th | underweight |
| 5th - < 85th | normal |
| 85th - < 95th | overweight |
| ≥ 95th | obese |

### `assessBmi(height, weight, ageMonths, gender)` — Main Entry Point

Returns:
```typescript
interface BmiResult {
  bmi: number;           // raw BMI e.g. 16.8
  zScore: number;        // z-score e.g. 0.75
  percentile: number;    // e.g. 77.3
  category: 'underweight' | 'normal' | 'overweight' | 'obese';
  label: string;         // e.g. "Healthy weight"
  ageMonths: number;
}
```

Returns `null` if age < 24 or > 60 months (outside WHO reference range).

## Integration

**`app/child/routine.tsx` (Step 4 — Physical):**
1. Parent enters height (cm) and weight (kg)
2. `getAgeMonths(child.dateOfBirth)` computes age from DOB
3. `assessBmi(height, weight, ageMonths, gender)` returns BmiResult
4. Result displayed with category color and label
5. Stored to `children` table (height_cm, weight_kg, bmi)

**Gender-aware:** Previous version hardcoded gender as `'male'`. Since 2026-04-14, uses actual child gender from `children.gender`.

## Reference Source

WHO Child Growth Standards — BMI-for-age 5-19 years:
https://www.who.int/tools/growth-reference-data/5-19-years/bmi-for-age

**Note:** WHO reference starts at 60 months (5 years) for BMI-for-age. The app uses LMS parameters extrapolated down to 24 months for the toddler range. For ages outside 24-60 months, assessment returns null.
