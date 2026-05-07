# Frequently Asked Questions

## General

**Q: Is my data safe?**  
A: Yes. All data is stored in a PostgreSQL database protected by Row-Level Security (RLS). This means the database enforces that you can only access your own data. Additionally, avatar images are stored in a secure bucket, and passwords are never stored in plain text.

**Q: Can I use this on both iPhone and Android?**  
A: Yes. The app is built with Expo and React Native, so it runs on both iOS and Android from a single codebase.

**Q: Does it work offline?**  
A: You need an internet connection to log in and fetch data. Once logged in, some screens may cache data temporarily, but the app is designed to be online-first.

**Q: Is there a web version?**  
A: Not currently. The app is mobile-only.

---

## Accounts

**Q: I forgot my password. What do I do?**  
A: There is no in-app password reset yet. Contact support or, if you're a developer, use the Supabase dashboard to send a password reset email.

**Q: Can I change my email address?**  
A: Yes. Go to **Settings** → **Change Email**. You'll need to enter your current password for security. A confirmation link will be sent to your new email.

**Q: Can I share my account with a co-parent?**  
A: Not yet. Each parent needs their own account. Multi-parent support is planned for a future release.

---

## Children & Data

**Q: Can I add more than one child?**  
A: Yes. Tap **+ Add** in the child selector on the Dashboard, or go to **Settings** → **+ Add Child**.

**Q: What happens if I delete a child's profile?**  
A: The profile and reminders are removed, but the logged activities remain in the database. This preserves your history in case you want to reference it later.

**Q: Can I edit or delete a past activity log?**  
A: Not from the History screen. History is read-only. If you made a mistake while logging, you'll need to log a correcting entry.

**Q: Why does the BMI calculator only work for ages 2–5?**  
A: The app uses the WHO BMI-for-age reference tables, which are standardized for children aged 24 to 60 months. Outside this range, the reference data is not available.

---

## Activities & Scheduling

**Q: What's the difference between "Log" and "Schedule"?**  
A: **Log** records something that already happened. **Schedule** plans a future activity and sets reminder notifications for it.

**Q: Can I schedule recurring activities (e.g., "bedtime every day")?**  
A: Not yet. Each schedule is a one-time event. Daily reminders for routines are handled by the Notifications system instead.

**Q: Why does scheduling redirect me to the History tab?**  
A: So you can immediately see and confirm your new schedule in the upcoming list.

---

## AI Insights

**Q: Is the AI a doctor?**  
A: No. The AI provides general advisory recommendations based on your logged data. It is not a medical device and does not diagnose conditions.

**Q: What data does the AI see?**  
A: Only aggregated summaries — total hours of screen time, average sleep, meal counts, etc. It does not see raw timestamps, your location, or your email address.

**Q: How often can I generate insights?**  
A: At most once per day per child. If you already generated insights today, the app will show the existing ones instead of calling the AI again.

**Q: Why do I only see 3 recommendations per category?**  
A: To prevent information overload. All recommendations are still saved; only the display is limited to the 3 most recent per category.

---

## Notifications

**Q: Why am I not getting reminders?**  
A: Check three things:
1. The master **All Notifications** toggle in Settings is ON.
2. The specific reminder type is toggled ON for your child.
3. The corresponding routine time is set (e.g., a bedtime reminder needs a bedtime).

**Q: Will notifications work if I close the app?**  
A: Yes. Local notifications are handled by your phone's operating system and do not require the app to be open.

**Q: Can I set custom notification sounds?**  
A: Not yet. The app uses the default system notification sound.

---

## Troubleshooting

**Q: The app is stuck on a loading screen.**  
A: Force-close and reopen the app. If the issue persists, check your internet connection.

**Q: My activities aren't showing up.**  
A: Make sure you have the correct child selected in the child picker. Also try pulling down to refresh the screen.

**Q: The AI Insights tab says "Not enough data."**  
A: Log at least 7 days of activities. The AI needs a minimum amount of data to generate meaningful recommendations.
