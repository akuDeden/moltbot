# Browser Testing Setup - Moltbot Browser Tool

Bot sekarang bisa melakukan **automated browser testing** menggunakan **Moltbot Built-in Browser Tool**!

## 🎯 Capabilities

Bot dapat menggunakan `browser` tool untuk:
- ✅ Navigate ke URLs
- ✅ Test login workflows
- ✅ Fill forms & submit
- ✅ Click buttons & links (dengan refs dari snapshot)
- ✅ Type text ke input fields
- ✅ Read page content (snapshot)
- ✅ Take screenshots (full page atau per element)
- ✅ Verify elements exist
- ✅ Check for errors & console logs
- ✅ Auto-create bug tickets jika test fail
- ✅ Wait for elements/URL/load state
- ✅ Drag & drop
- ✅ Select dropdowns
- ✅ Handle file uploads
- ✅ Handle dialogs (alert/confirm)

## 🚀 Two Modes Available

### Mode 1: Managed Browser (Recommended for Testing)
- Profile: `clawd` (isolated, safe, tidak touch personal browser)
- Auto-managed by Moltbot
- No extension needed
- Dedicated user data directory
- **Best for:** Automated testing, CI/CD, safe automation

### Mode 2: Chrome Extension (Control Existing Browser)
- Profile: `chrome` (control your existing Chrome tabs)
- Requires Chrome extension installed & attached
- **Best for:** Manual testing, debugging, live demos

## 📋 Quick Start

### Option A: Managed Browser (Easiest)

```bash
# Check status
moltbot browser --browser-profile clawd status

# Start browser
moltbot browser --browser-profile clawd start

# Open URL
moltbot browser --browser-profile clawd open https://staging.chronicle.rip

# Take snapshot (get page structure)
moltbot browser --browser-profile clawd snapshot --interactive

# Take screenshot
moltbot browser --browser-profile clawd screenshot
```

### Option B: Chrome Extension

```bash
# 1. Install extension
moltbot browser extension install

# 2. Get extension path
moltbot browser extension path

# 3. Load ke Chrome
# chrome://extensions → Enable "Developer mode" → "Load unpacked"
# Select directory from step 2

# 4. Open tab → Click extension icon → Badge shows "ON"

# 5. Use it
moltbot browser --browser-profile chrome tabs
moltbot browser --browser-profile chrome snapshot --interactive
```

## 🎬 Browser Tool Usage

### Basic Commands

```bash
# Status & control
moltbot browser status
moltbot browser start
moltbot browser stop
moltbot browser tabs

# Navigation
moltbot browser navigate https://example.com
moltbot browser open https://example.com  # Opens new tab

# Snapshot (get page structure with refs)
moltbot browser snapshot --interactive  # Role-based refs (e12, e13)
moltbot browser snapshot                # AI snapshot with numeric refs (12, 13)

# Screenshot
moltbot browser screenshot              # Current viewport
moltbot browser screenshot --full-page  # Full page
moltbot browser screenshot --ref e12    # Specific element

# Actions (require refs from snapshot)
moltbot browser click e12               # Click element
moltbot browser type e23 "test@example.com" --submit
moltbot browser press Enter
moltbot browser hover e44
moltbot browser select e9 OptionA       # Select dropdown

# Wait for conditions
moltbot browser wait "#main"                    # Wait for selector
moltbot browser wait --url "**/dashboard"       # Wait for URL
moltbot browser wait --load networkidle         # Wait for network idle
moltbot browser wait --fn "window.ready===true" # Wait for JS condition

# Debug
moltbot browser console --level error
moltbot browser errors
moltbot browser highlight e12           # Highlight element on page
```

### Refs System

Moltbot uses **refs** (references) untuk identify elements:

1. **Get snapshot** dengan refs:
   ```bash
   moltbot browser snapshot --interactive
   ```
   Output:
   ```
   [ref=e12] button "Sign in"
   [ref=e23] textbox "Email"
   [ref=e24] textbox "Password"
   ```

2. **Use refs** untuk actions:
   ```bash
   moltbot browser type e23 "user@example.com"
   moltbot browser type e24 "password123"
   moltbot browser click e12
   ```

## 🚀 Usage Examples

### Test Login
```
User: test login staging.chronicle.rip

Bot:
- Navigate to URL
- Find login form
- Enter credentials
- Submit & verify
- Report hasil + screenshot
```

### Test Form
```
User: test form registration di staging

Bot:
- Navigate to registration page
- Fill form dengan test data
- Submit
- Verify response
- Report hasil
```

### Custom Browser Action
```
User: buka browser staging.chronicle.rip dan cek halaman dashboard

Bot:
- Navigate to URL
- Check dashboard elements
- Take screenshot
- Report findings
```

## 🔐 Security Setup

### Test Credentials

Create file: `test-credentials.json`
```json
{
  "staging": {
    "url": "https://staging.chronicle.rip",
    "username": "test@example.com",
    "password": "test_password_here"
  },
  "production": {
    "url": "https://chronicle.rip",
    "username": "test@example.com",
    "password": "test_password_here"
  }
}
```

**⚠️ IMPORTANT:**
- Add `test-credentials.json` to `.gitignore`
- Never commit credentials to git
- Use dedicated test accounts only
- Never test on production with real user data

## 🎭 Chrome Profile Setup (Recommended)

Create dedicated Chrome profile for testing:

1. Chrome → Profile → Add Profile → "Testing"
2. Use this profile for bot testing only
3. Separate from your personal browsing
4. Extension attached to this profile's tabs

## 📝 Test Workflow

### 1. User Request
```
User: test login staging.chronicle.rip
```

### 2. Bot Detection
- Keyword: "test login" → Load QA persona
- Load persona/QA.md → COMMAND 6: BROWSER TESTING

### 3. Bot Execution
```python
1. Read test-credentials.json (staging)
2. Browser navigate to staging.chronicle.rip
3. Find login form elements
4. Enter username & password
5. Click submit
6. Wait for redirect
7. Verify dashboard/success page
8. Take screenshot
```

### 4. Bot Report
```
✅ Login test PASSED - staging.chronicle.rip

Steps executed:
1. ✅ Navigate to staging.chronicle.rip
2. ✅ Form found (username, password fields)
3. ✅ Credentials entered
4. ✅ Submit clicked
5. ✅ Redirect to /dashboard
6. ✅ Welcome message visible

Screenshot: [link]
Time: 3.2s
```

### 5. If Test Fails
```
❌ Login test FAILED - staging.chronicle.rip

Error: Submit button tidak response

Steps executed:
1. ✅ Navigate to staging.chronicle.rip
2. ✅ Form found
3. ✅ Credentials entered
4. ❌ Submit click - no response
5. Console error: "Uncaught TypeError..."

🐛 Bug ticket created: BUG-2026-001
   URL: https://notion.so/...
   Severity: High

Screenshot: [link]
```

## 🛠️ Troubleshooting

### Extension Badge Shows `!`
- Gateway/relay server not running
- Solution: Restart moltbot gateway

### Extension Badge Shows `…`
- Connecting to relay
- Wait a few seconds

### Can't Control Tab
- Make sure extension is attached (click icon → `ON`)
- Refresh page if needed
- Detach & re-attach

### Security Warning
- Extension uses Chrome debugger API
- Only attach to test tabs
- Use dedicated Chrome profile
- Keep Gateway on local/tailnet only

## 📚 Related Docs

- [Moltbot Chrome Extension](https://docs.molt.bot/tools/chrome-extension)
- [Browser Tool Overview](https://docs.molt.bot/tools/browser)
- [Security Best Practices](https://docs.molt.bot/gateway/security)

## ✨ Integration with Persona System

Browser testing integrated dengan QA Persona:

**Keywords:** `test login`, `test browser`, `buka browser`, `test staging`

**Workflow:**
1. User kirim command dengan trigger keyword
2. Bot detect → Load persona/QA.md
3. Execute COMMAND 6: BROWSER TESTING
4. Report hasil + auto-create bug ticket if fail

**Files:**
- `persona/QA.md` - Contains COMMAND 6 with browser testing instructions
- `CONTEXT.md` - Keyword routing
- `test-credentials.json` - Test credentials (create this, don't commit)

Ready untuk automated testing! 🎉
