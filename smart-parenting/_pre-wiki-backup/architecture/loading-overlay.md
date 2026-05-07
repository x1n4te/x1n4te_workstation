The loading overlay lives in `app/_layout.tsx` — it's a full-screen overlay rendered ON TOP of the entire app while auth state is being determined. Here's how it works:

---

## The Loading Overlay Mechanism

### The Component Tree During Load

```
<PaperProvider>
  <StatusBar>
  <Stack>
    (auth) screens
    (tabs) screens
    child/wizard screen
  </Stack>
  
  {/* This View is ALWAYS mounted, but pointerEvents is 'none' when hidden */}
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

Because it's rendered inside `<PaperProvider>` but OUTSIDE `<Stack>`, it's **always on top** — above every route. The `pointerEvents="auto"` means when visible, it blocks all interaction with screens beneath it.

---

### Three States

| State | Condition | Text shown |
|-------|-----------|------------|
| **Auth loading** | `loading = true` (initial session check) | `"Smart Parenting"` |
| **Auth redirecting** | `redirecting = true` (logged-in user on auth screens, 1800ms delay) | `"Setting things up…"` |
| **Hidden** | Both false | Not rendered |

---

### How Each State Fires

**State 1 — Initial load:**

```typescript
// On mount
useEffect(() => {
  loadSession();   // Async — fetches Supabase session
  initNotifications();
}, []);
```

`loadSession()` sets `loading: false` when done. While it's running, the overlay shows with "Smart Parenting".

**State 2 — Redirect delay (logged-in user hits auth screens):**

```typescript
// Auth redirect effect
useEffect(() => {
  if (!isMounted.current) return;
  if (loading) return;

  const inAuthGroup = segments[0] === '(auth)';

  if (!user && !inAuthGroup) {
    // Not logged in → go to login immediately
    router.replace('/(auth)/login');
  } else if (user && inAuthGroup) {
    // Logged in but on auth screens → delay 1800ms
    if (redirectTimer.current) clearTimeout(redirectTimer.current);
    setRedirecting(true);           // ← OVERLAY SHOWS "Setting things up…"
    redirectTimer.current = setTimeout(() => {
      setRedirecting(false);        // ← OVERLAY HIDES
      if (isMounted.current) {
        try { router.replace('/(tabs)'); } catch {}
      }
    }, 1800);
  }
}, [user, loading, segments]);
```

The `isMounted` ref is critical — it prevents the redirect effect from firing during `loadSession()` before the `<Stack>` is even mounted:

```typescript
// Prevents: "Attempted to navigate before mounting the Root Layout"
useEffect(() => {
  isMounted.current = true;
  return () => { isMounted.current = false; };
}, []);
```

---

### Why `redirecting` State Exists

Without it, when a logged-in user opens the app, they'd see:
1. Auth check passes (user exists)
2. `router.replace('/(tabs)')` fires immediately
3. The (tabs) screens briefly flash behind the overlay
4. Tab navigator mounts

With `redirecting = true`, the overlay persists for 1800ms AFTER auth check passes, giving time for the "Welcome back!" animation on the login screen to play, then smoothly transitions to the tabs. The user never sees blank screens or half-mounted routes.

---

### The Z-Index Stack

```typescript
loadingOverlay: {
  ...StyleSheet.absoluteFillObject,   // covers entire screen
  zIndex: 999,                       // above everything
  elevation: 999,                    // Android elevation
  backgroundColor: '#FEFBF6',       // matches app background — looks seamless
}
```

`absoluteFillObject` = `{ top: 0, left: 0, right: 0, bottom: 0 }`. Combined with `zIndex: 999`, it covers everything. The `backgroundColor: '#FEFBF6'` matches the app's cream background — so when the overlay disappears, there's no visual "flash" since the screen beneath already shows the same color.

---

### How the Auth Guard Works (Full Sequence)

```
App launches
    ↓
RootLayout mounts
    ↓
isMounted = true
    ↓
useEffect fires → loadSession() starts
    loading = true → overlay shows "Smart Parenting"
    ↓
loadSession() resolves (Supabase returns session or null)
    loading = false
    ↓
Auth redirect effect fires:
  ├─ No user + not in auth group → redirect to /login (no overlay delay)
  ├─ No user + in auth group → stay on login (no overlay)
  └─ User exists + in auth group → setRedirecting(true)
       overlay text changes to "Setting things up…"
       1800ms timer starts
       ↓
       Timer fires → redirecting = false
       overlay hides
       router.replace('/(tabs)')
```

---

### Why There's No Flash on Navigation

The overlay uses `backgroundColor: '#FEFBF6'` which is the same as the app's `background` theme color (`#FEFBF6` in the PaperProvider theme). So when the overlay disappears, the screen beneath is already rendered in the same color — no white flash.