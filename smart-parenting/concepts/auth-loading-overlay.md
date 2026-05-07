---
title: Auth Loading Overlay & Auth Guard
created: 2026-04-25
updated: 2026-04-25
type: concept
tags: [auth, architecture, navigation, ui-ux]
sources: [raw/technical-reference.md]
---

# Auth Loading Overlay & Auth Guard

The loading overlay lives in `app/_layout.tsx` — a full-screen overlay rendered ON TOP of the entire app while auth state is being determined.

---

## Component Tree During Load

```
<PaperProvider>
  <StatusBar>
  <Stack>
    (auth) screens
    (tabs) screens
    child/wizard screen
  </Stack>

  {/* Always mounted, pointerEvents='none' when hidden */}
  {(loading || redirecting) && (
    <View pointerEvents="auto" style={styles.loadingOverlay}>
      <ActivityIndicator size="large" color="#FF7F60" />
      <Text style={styles.loadingText}>
        {redirecting ? 'Setting things up…' : 'Smart Parenting'}
      </Text>
    </View>
  )}
</PaperProvider>
```

Because it's rendered inside `<PaperProvider>` but OUTSIDE `<Stack>`, it's **always on top**. `pointerEvents="auto"` blocks all interaction when visible.

---

## Three States

| State | Condition | Text shown |
|-------|-----------|------------|
| **Auth loading** | `loading = true` (initial session check) | `"Smart Parenting"` |
| **Auth redirecting** | `redirecting = true` (logged-in user on auth screens, 1800ms delay) | `"Setting things up…"` |
| **Hidden** | Both false | Not rendered |

---

## State Machine

**Initial load:**
```typescript
useEffect(() => {
  loadSession();   // Async — fetches Supabase session
  initNotifications();
}, []);
```

**Redirect delay (logged-in user hits auth screens):**
```typescript
useEffect(() => {
  if (!isMounted.current) return;
  if (loading) return;

  const inAuthGroup = segments[0] === '(auth)';

  if (!user && !inAuthGroup) {
    router.replace('/(auth)/login');
  } else if (user && inAuthGroup) {
    setRedirecting(true);
    redirectTimer.current = setTimeout(() => {
      setRedirecting(false);
      if (isMounted.current) {
        try { router.replace('/(tabs)'); } catch {}
      }
    }, 1800);
  }
}, [user, loading, segments]);
```

The `isMounted` ref prevents "Attempted to navigate before mounting" errors from synchronous `onAuthStateChange`.

---

## Why `redirecting` State Exists

Without it, a logged-in user would see:
1. Auth check passes → `router.replace('/(tabs)')` fires immediately
2. Tab navigator briefly flashes behind the overlay

With `redirecting = true`, the overlay persists for 1800ms AFTER auth check passes, giving time for the "Welcome back!" animation, then smoothly transitions.

---

## Z-Index Stack

```typescript
loadingOverlay: {
  ...StyleSheet.absoluteFillObject,
  zIndex: 999,
  elevation: 999,
  backgroundColor: '#FEFBF6',  // matches app background — seamless
}
```

`backgroundColor: '#FEFBF6'` matches the PaperProvider theme background, so when the overlay disappears there's no visual flash. The overlay is triggered by [[screen-auth]] login/signup flows.

---

## Deep-Link Notification Handling

Polls auth readiness every 100ms (max 1s) before routing based on notification `type`. See [[notification-system]] for notification routing details.
