# Windows → iOS Development Setup

This guide walks you through setting up the Smart Parenting App on a **Windows PC** for development and testing on a **physical iOS device**.

> **Important:** You cannot run the iOS Simulator on Windows, and you cannot build native iOS binaries (.ipa) locally without a Mac. However, you can develop, test, and preview the app on your iPhone using **Expo Go**, and you can build production iOS binaries using **EAS Build** (cloud builds).

---

## Table of Contents

1. [What You Can and Cannot Do on Windows](#what-you-can-and-cannot-do-on-windows)
2. [Prerequisites](#prerequisites)
3. [Step 1: Install Node.js](#step-1-install-nodejs)
4. [Step 2: Install Git](#step-2-install-git)
5. [Step 3: Install VS Code](#step-3-install-vs-code)
6. [Step 4: Install Expo CLI](#step-4-install-expo-cli)
7. [Step 5: Clone the Repository](#step-5-clone-the-repository)
8. [Step 6: Install Dependencies](#step-6-install-dependencies)
9. [Step 7: Set Up Supabase](#step-7-set-up-supabase)
10. [Step 8: Configure Environment Variables](#step-8-configure-environment-variables)
11. [Step 9: Install Expo Go on Your iPhone](#step-9-install-expo-go-on-your-iphone)
12. [Step 10: Start the Development Server](#step-10-start-the-development-server)
13. [Step 11: Connect Your iPhone](#step-11-connect-your-iphone)
14. [Step 12: EAS Build for Production](#step-12-eas-build-for-production)
15. [Troubleshooting](#troubleshooting)

---
## Prerequisites

Before starting, ensure you have:
- A Windows 10 or Windows 11 PC with admin rights
- An iPhone (iOS 15 or newer recommended)
- Your iPhone and PC on the **same Wi-Fi network**
- A free Expo account ([sign up](https://expo.dev/signup))
- A free Supabase account ([sign up](https://supabase.com))
- (Optional) A free GitHub account for cloning

---

## Step 1: Install Node.js

Node.js is required to run the JavaScript tooling.

1. Go to [https://nodejs.org](https://nodejs.org)
2. Download the **LTS** version (recommended for most users) — the button on the left.
3. Run the installer.
4. Keep clicking **Next** until installation is complete. The default settings are fine.
5. Verify installation by opening **Command Prompt** or **PowerShell** and typing:

```bash
node --version
npm --version
```

You should see version numbers like `v22.x.x` and `10.x.x`.

> **Why LTS?** Long-Term Support versions are stable and receive security updates. Expo SDK 55 requires Node 18 or newer.

---

## Step 2: Install Git

Git is needed to clone the repository and track code changes.

1. Go to [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. The download should start automatically. If not, click the link for your system (64-bit Git for Windows Setup).
3. Run the installer.
4. Use these recommended settings during setup:
   - **Select Components:** Keep defaults checked
   - **Editor:** Select "Use Visual Studio Code as Git's default editor" (if you plan to install VS Code) or "Use Vim" (if comfortable)
   - **Adjusting PATH:** Select "Git from the command line and also from 3rd-party software"
   - **HTTPS Transport:** "Use the OpenSSL library"
   - **Line endings:** "Checkout Windows-style, commit Unix-style line endings"
5. Finish installation.
6. Verify in Command Prompt:

```bash
git --version
```

You should see something like `git version 2.47.x`.

---

## Step 3: Install VS Code

VS Code is the recommended code editor for this project.

1. Go to [https://code.visualstudio.com](https://code.visualstudio.com)
2. Download the **User Installer** for Windows (64-bit).
3. Run the installer with default settings.
4. (Recommended) Install these extensions after opening VS Code:
   - **ES7+ React/Redux/React-Native snippets** (for React Native code)
   - **TypeScript Importer** (auto-imports)
   - **Prettier** (code formatting)
   - **ESLint** (linting)
   - **Expo Tools** (if available)

---

## Step 4: Install Expo CLI

Expo provides command-line tools for running and building the app.

Open **Command Prompt** or **PowerShell** and run:

```bash
npm install -g expo-cli
```

Wait for installation to complete. Then verify:

```bash
expo --version
```

> **Note:** As of Expo SDK 55, the local CLI is bundled with the project. The global `expo-cli` is still useful for some legacy commands, but you'll mostly use `npx expo` commands inside the project.

Also install EAS CLI for cloud builds:

```bash
npm install -g eas-cli
```

Verify:

```bash
eas --version
```

---

## Step 5: Clone the Repository

You need to get the project code onto your PC.

### Option A: Clone from GitHub (if the repo is hosted there)

1. Open Command Prompt or PowerShell.
2. Navigate to where you want the project folder. Example:

```bash
cd Documents
```

3. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/smart-parenting-app.git
```

4. Enter the project folder:

```bash
cd smart-parenting-app
```

### Option B: Download as ZIP (if no GitHub access)

1. Download the project ZIP file.
2. Extract it to `C:\Users\YOUR_NAME\Documents\smart-parenting-app\`
3. Open VS Code.
4. Go to **File** → **Open Folder** and select the extracted folder.

---

## Step 6: Install Dependencies

Inside the project folder, install all required packages.

Open Command Prompt or PowerShell in the project folder and run:

```bash
npm install
```

This will download hundreds of packages (React Native, Expo, Supabase, Zustand, etc.) into the `node_modules` folder. It may take 5–10 minutes depending on your internet speed.

> **Common Windows issue:** If you see errors about Python or Visual Studio build tools, ignore them unless the install fails. Most React Native packages provide prebuilt Windows binaries.

If installation fails, try clearing the cache:

```bash
npm cache clean --force
rmdir /s /q node_modules
npm install
```

---

## Step 7: Set Up Supabase

The app requires a Supabase backend. You have two options:

### Option A: Use the Existing Cloud Project (Recommended for Team Development)

If the project already has a Supabase project set up:

1. Ask the project owner for the **Project URL** and **Anon Key**.
2. Skip to [Step 8: Configure Environment Variables](#step-8-configure-environment-variables).

### Option B: Create a New Supabase Project (for Fresh Setup)

1. Go to [https://supabase.com](https://supabase.com) and sign in.
2. Click **New Project**.
3. Choose an organization and name the project `smart-parenting`.
4. Set a secure database password. **Save this password** — you cannot recover it later.
5. Wait 1–2 minutes for the project to initialize.
6. Once ready, click the **Connect** button or go to **Project Settings** → **API**.
7. Copy these two values:
   - **Project URL** (e.g., `https://abcdefghijklmnopqrst.supabase.co`)
   - **anon public** API key (starts with `eyJ...`)

8. Go to the **SQL Editor** in the Supabase dashboard.
9. Open the file `database/schema.sql` from your cloned project.
10. Copy the entire contents and paste it into the SQL Editor.
11. Click **Run**. This creates all tables, indexes, RLS policies, and triggers.

#### Set Up Storage for Avatars

1. In Supabase dashboard, go to **Storage**.
2. Click **New Bucket**.
3. Name it `avatars`.
4. Check **Public bucket**.
5. Click **Save**.

#### Set Up Edge Function (for AI Insights)

1. Install Supabase CLI locally (for Edge Function deployment):

```bash
npm install -g supabase
```

2. Log in to Supabase CLI:

```bash
supabase login
```

This opens a browser window. Click **Accept** to authorize.

3. Link your local project to the Supabase project:

```bash
supabase link --project-ref YOUR_PROJECT_REF
```

Your project ref is the random string in your Project URL (e.g., `abcdefghijklmnopqrst`).

4. Deploy the Edge Function:

```bash
supabase functions deploy analyze-child
```

5. Set the OpenRouter API key as a secret:

```bash
supabase secrets set OPENROUTER_API_KEY=your_openrouter_api_key
```

Get a free API key at [https://openrouter.ai/keys](https://openrouter.ai/keys).

---

## Step 8: Configure Environment Variables

The app needs to know where your Supabase project is.

1. In VS Code or File Explorer, go to the project root.
2. Create a new file named `.env`.
3. Paste the following, replacing the placeholders with your actual values:

```env
EXPO_PUBLIC_SUPABASE_URL=https://your-project-url.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
```

4. Save the file.

> **Security:** Never commit `.env` to Git. The file is already listed in `.gitignore` by default, but double-check that `.gitignore` contains `.env`.

### Verify Configuration

Create a quick test script to confirm connectivity. In the project root, create `test-supabase.js`:

```javascript
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(
  process.env.EXPO_PUBLIC_SUPABASE_URL,
  process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY
);

async function test() {
  const { data, error } = await supabase.from('children').select('*').limit(1);
  if (error) console.error('Error:', error.message);
  else console.log('Connected! Sample data:', data);
}

test();
```

Run it:

```bash
node test-supabase.js
```

If you see `Connected!`, your configuration is correct. Delete the test file afterward.

---

## Step 9: Install Expo Go on Your iPhone

Expo Go is the app that lets you preview your project on a physical device without building a native binary.

1. Open the **App Store** on your iPhone.
2. Search for **"Expo Go"**.
3. Download the official app by Expo (orange icon with white brackets).
4. Open Expo Go and sign in with the same Expo account you created earlier.

> **Important:** Your iPhone and Windows PC must be on the **same Wi-Fi network** for the development server to communicate with Expo Go.

---

## Step 10: Start the Development Server

Now you're ready to run the app.

1. Open Command Prompt or PowerShell in the project folder.
2. Run:

```bash
npx expo start
```

3. Wait for the Metro bundler to start. You'll see a QR code in the terminal and a developer tools UI in your browser.

```
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║    Scan the QR code above with Expo Go (Android) or               ║
║    the Camera app (iOS) to open the project.                      ║
║                                                                   ║
║    Press 'a' to open Android.                                     ║
║    Press 'i' to open iOS simulator (requires macOS).              ║
║    Press 'w' to open web.                                         ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

> **Note:** On Windows, pressing `i` will **not** work because there is no iOS Simulator. Pressing `a` will attempt to open an Android emulator.

---

## Step 11: Connect Your iPhone

### Method 1: QR Code (Recommended)

1. Open the **Camera app** on your iPhone.
2. Point it at the QR code displayed in your terminal.
3. A notification banner appears: "Open in Expo Go"
4. Tap the banner.
5. The app loads on your iPhone.

### Method 2: Manual URL Entry

1. In the terminal running Metro, look for a line like:
   ```
   Metro waiting on exp://192.168.1.45:8081
   ```
2. Open Expo Go on your iPhone.
3. Tap **"Enter URL manually"**.
4. Type the exact URL from the terminal (e.g., `exp://192.168.1.45:8081`).
5. Tap **Connect**.

### Method 3: Expo Dev Tools in Browser

1. Metro automatically opens a browser tab at `http://localhost:8081`.
2. In the browser UI, find the QR code.
3. Scan it with your iPhone Camera app.

---

## Development Workflow

Once connected, your workflow is:

1. **Edit code** in VS Code on Windows.
2. **Save the file.**
3. **See changes instantly** on your iPhone (Fast Refresh).
4. **Test features** directly on the device — camera, notifications, and gestures all work.

### Useful Metro Commands

While Metro is running, you can press these keys in the terminal:

| Key | Action |
|-----|--------|
| `r` | Reload the app |
| `m` | Toggle performance monitor on device |
| `j` | Open Chrome DevTools for debugging |
| `Ctrl + C` | Stop the server |

### Viewing Logs

To see console logs from your iPhone:

```bash
npx expo start --ios
```

Or use the browser-based DevTools that open automatically. Logs from `console.log()` in your code will appear there.

---

## Step 12: EAS Build for Production

When you're ready to create a real iOS app (.ipa) for TestFlight or the App Store, use **EAS Build** — Expo's cloud build service. This runs on Expo's servers, so you don't need a Mac.

### 1. Configure EAS

In the project root, run:

```bash
eas login
```

Sign in with your Expo account.

Then configure the project:

```bash
eas build:configure
```

Select **iOS** when prompted. This creates an `eas.json` file.

### 2. Set Up iOS Credentials

EAS Build can automatically manage your iOS credentials, but you'll need an Apple Developer account ($99/year) for App Store distribution.

For ad-hoc testing (no developer account needed initially):

```bash
eas build --platform ios --profile development
```

For production builds:

```bash
eas build --platform ios --profile production
```

### 3. First Build

Run:

```bash
eas build --platform ios
```

EAS will ask you to:
- Choose the build type (`apk`, `aab`, or `ipa` — choose `ipa`)
- Generate or provide iOS credentials
- Wait for the build to complete (10–20 minutes)

When finished, you'll receive a download link or the build will appear in your [Expo dashboard](https://expo.dev).

### 4. Install on Your iPhone

#### Option A: Direct Install (Development Builds Only)

If you built a development client:
1. Download the `.ipa` file from the Expo dashboard.
2. Use [AltStore](https://altstore.io/) or Apple Configurator 2 (on a Mac) to sideload it.

#### Option B: TestFlight (Requires Apple Developer Account)

1. Complete the production build with EAS.
2. Use EAS Submit to upload to App Store Connect:

```bash
eas submit --platform ios
```

3. Log in to [App Store Connect](https://appstoreconnect.apple.com).
4. Add the build to TestFlight.
5. Invite yourself as a tester.
6. Download via the TestFlight app on your iPhone.

#### Option C: Use a Mac for Final Steps

If you have access to a Mac (even temporarily):
1. Download the `.ipa` from EAS Build.
2. Use Apple Configurator 2 or Xcode to install it on your device.
3. Or use Transporter to upload to App Store Connect.

---

## Project-Specific Setup Notes

### Remove Incompatible Dependencies

The project previously had issues with `@expo/dom-webview` breaking Android builds. Ensure it is not installed:

```bash
npm uninstall @expo/dom-webview
```

If you ever need to clean and rebuild:

```bash
rmdir /s /q node_modules
rmdir /s /q .expo
npm install
npx expo prebuild --clean
```

### Supabase Local Development (Optional)

If you want to run Supabase locally instead of using the cloud project:

1. Install Docker Desktop for Windows.
2. Start Docker Desktop.
3. In your project folder, run:

```bash
supabase start
```

This starts a local PostgreSQL instance, Auth service, and Storage. Update your `.env` to use the local URL printed in the terminal.

To stop:

```bash
supabase stop
```

---

## Troubleshooting

### "Could not connect to development server"

**Cause:** iPhone and PC are on different networks, or Windows Firewall is blocking port 8081.

**Fix:**
1. Ensure both devices are on the **same Wi-Fi**.
2. Allow Node.js through Windows Firewall:
   - Open **Windows Security** → **Firewall & network protection** → **Allow an app through firewall**
   - Find **Node.js** and check both **Private** and **Public** boxes.
3. Try entering the URL manually in Expo Go instead of using the QR code.

### "Unable to resolve module"

**Cause:** Dependencies not installed correctly.

**Fix:**
```bash
rmdir /s /q node_modules
npm cache clean --force
npm install
```

### Expo Go shows "Something went wrong"

**Cause:** JavaScript bundle failed to compile.

**Fix:**
1. Look at the Metro terminal on Windows — red error messages will show the file and line number.
2. Fix the error in VS Code.
3. The app should automatically reload.

### iPhone won't scan the QR code

**Fix:**
1. Make sure you're using the **Camera app**, not the Expo Go scanner (on iOS, Camera app handles `exp://` URLs).
2. Try the manual URL entry method instead.
3. Check that your phone is on the same Wi-Fi as your PC.

### "Network response timed out"

**Cause:** Supabase URL or key is incorrect.

**Fix:**
1. Double-check your `.env` file values.
2. Make sure there are no extra spaces or quotes around the values.
3. Restart Metro (`Ctrl + C`, then `npx expo start`).

### EAS Build fails with iOS credential errors

**Cause:** Missing Apple Developer account or invalid provisioning profile.

**Fix:**
1. For development testing, use the `--profile development` flag.
2. For production, ensure you have a valid Apple Developer account.
3. Let EAS auto-generate credentials by choosing "Yes" when it asks to generate a new profile.

### "command not found: npx"

**Cause:** Node.js wasn't installed correctly or PATH wasn't updated.

**Fix:**
1. Restart Command Prompt or PowerShell.
2. If still failing, reinstall Node.js and check "Automatically install necessary tools" during setup.

---

## Quick Reference: Common Commands

| Task | Command |
|------|---------|
| Start development server | `npx expo start` |
| Start with cleared cache | `npx expo start --clear` |
| Run on Android (if emulator connected) | `npx expo run:android` |
| Build iOS (cloud) | `eas build --platform ios` |
| Build Android (cloud) | `eas build --platform android` |
| Submit to App Store | `eas submit --platform ios` |
| Update OTA (no store needed) | `eas update` |
| Deploy Supabase Edge Function | `supabase functions deploy analyze-child` |
| View Supabase logs | `supabase functions logs analyze-child` |

---

## Summary Checklist

- [ ] Node.js installed (LTS version)
- [ ] Git installed
- [ ] VS Code installed
- [ ] `expo-cli` and `eas-cli` installed globally
- [ ] Repository cloned and `npm install` completed
- [ ] Supabase project created and schema applied
- [ ] `.env` file created with Supabase URL and anon key
- [ ] Expo Go installed on iPhone and signed in
- [ ] iPhone and PC on same Wi-Fi
- [ ] `npx expo start` running and app loading on iPhone
- [ ] (Optional) EAS Build configured for iOS

Once all items are checked, you're ready to develop the Smart Parenting App on Windows with your iPhone as the target device.
