# AI Insights

AI Insights analyzes your child's activity data and generates personalized recommendations to help you make informed parenting decisions.

---

## How It Works

When you tap **Generate Insights**, the app does the following behind the scenes:

1. **Collects** the last 28 days of your child's logged activities from the database.
2. **Aggregates** the data into summaries — average screen time, total sleep hours, meals logged, etc.
3. **Compares** recent data to the previous 28-day period to detect trends (improving, stable, or worsening).
4. **Fetches** your child's routine schedule and any configured limits (max screen time, min sleep).
5. **Sends** all this information to an AI model via a secure server-side function.
6. **Receives** structured recommendations, which are saved to your account with a full audit trail.
7. **Displays** them as cards grouped by category.

The entire process takes a few seconds and happens at most once per day per child.

---

## What the AI Sees

The AI receives only aggregated statistics — never raw activity logs. Specifically:

- **Child's name** (first name only)
- **Age** in years and months
- **BMI assessment** (if available)
- **Activity totals** over 28 days (e.g., "12 hours of screen time across 15 days")
- **Routine schedule** (bedtime, wake-up, meal times)
- **Configured limits** (e.g., "max 2 hours screen time")
- **Previous recommendations** (last 3, to check for follow-ups)

**The AI does NOT receive:**
- Your email address
- Your location
- Raw timestamps of activities
- Any data about other children

---

## Recommendation Cards

Each insight appears as a card with:

- **Category** — Sleep, Meals, Education, Screen Time, or General
- **Priority** — High, Medium, or Low
- **Advice** — 2–3 sentences citing specific data
- **Date** — When the recommendation was generated
- **Recency Badge** — Indicates how fresh it is within its category:
  - 🟢 **Latest** — Most recent in this category
  - 🟡 **2nd Latest** — Second most recent
  - ⬜ **Oldest** — Third most recent (still one of the freshest)

### Category Limits

To prevent information overload, only the **3 most recent recommendations per category** are shown. Older recommendations remain saved in the database but are hidden from view.

---

## Confidence Levels

The app assigns a confidence score based on how much data is available:

| Data Logged | Confidence | Meaning |
|-------------|------------|---------|
| 14+ days | **High** | Solid data base |
| 7–13 days | **Medium** | Limited history |
| Fewer than 7 days | **Low** | Speculative — flagged in the UI |

If your data is sparse, the app will tell you: *"Sparse data — recommendations may be speculative."*

---

## Safety & Transparency

- **No medical claims** — Recommendations are advisory only, not clinical advice.
- **Reproducible** — Every recommendation has an audit trail (`based_on`) showing exactly what data was used.
- **Secure** — The AI model is accessed through a server-side function; your device never talks to the AI directly.
- **Free** — The model runs on OpenRouter's free tier, so insights cost nothing.

---

## When to Generate Insights

- **First time:** After about a week of logging data
- **Routine:** Once per week or whenever your child's routine changes significantly
- **After concerns:** If you notice changes in sleep, appetite, or behavior

---

## Limitations

- The AI model (`inclusionai/ling-2.6-1t:free`) is a general-purpose reasoning engine, not a pediatrician.
- Recommendations are only as good as the data you log. Missing days reduce accuracy.
- The app does not diagnose medical conditions.
