# 🚀 Quick Start: Browser Automation Bot (Multi-Persona)

## ✅ Setup Complete!

Bot Anda sekarang sudah **fully equipped** untuk browser automation **di multiple personas**!

---

## 📋 What's Been Added

### 1. ✅ ASSISTANT Persona Updated
**File:** `persona/ASSISTANT.md`

Added: **COMMAND 3: BROWSER AUTOMATION (SIMPLE)**
- Google search & screenshot
- Navigate to URL
- Simple browsing tasks
- **Smart handoff** to QA for complex testing

### 2. ✅ QA Persona Updated
**File:** `persona/QA.md`

Added section: **🤖 AUTOMATED BROWSER ACTIONS**
- Complex testing workflows
- Login testing
- Form verification
- Bug ticket creation
- **Cross-reference** to ASSISTANT for simple tasks

### 3. ✅ CONTEXT.md Updated
**File:** `CONTEXT.md`

Updated keywords untuk both personas:
- **ASSISTANT:** `cari di google`, `screenshot`, `buka [URL]` (simple)
- **QA:** `test login`, `test form`, `verify element` (complex)

Bot akan auto-load persona yang sesuai based on keywords.

### 4. ✅ Multi-Persona Documentation
**Files:**
- `docs/MULTI-PERSONA-BROWSER.md` - Persona mapping & handoff system
- `docs/BROWSER-AUTOMATION-EXAMPLES.md` - Detailed examples

---

## 🎯 How to Use (User Perspective)

User cukup kirim perintah natural language via **WhatsApp/Telegram**. Bot akan **auto-detect** persona yang tepat!

### Simple Tasks → ASSISTANT

```
cari di google ahmad faris
screenshot google.com
buka staging.chronicle.rip
```

Bot behavior:
✅ ASSISTANT persona handles
✅ Quick response (<2s)
✅ Screenshot included

### Complex Tasks → QA

```
test login staging.chronicle.rip dengan email test@example.com
test form registration di staging
verify bug TECH-123
```

Bot behavior:
✅ QA persona handles
✅ Full test execution
✅ Bug ticket creation (if fail)
✅ Detailed report + screenshots

---

## 🔧 Technical Flow

```
┌─────────────────────────────────────────────────┐
│ User sends: "buka google, cari ahmad faris"     │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│ Bot detects keyword: "buka google", "cari"      │
│ → Auto-load persona/QA.md                       │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│ Bot reads QA persona instructions:              │
│ "MUST use mcp_playwright_browser_* tools"       │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│ Bot executes MCP tools:                         │
│ 1. mcp_playwright_browser_navigate              │
│ 2. mcp_playwright_browser_fill_form             │
│ 3. mcp_playwright_browser_press_key             │
│ 4. mcp_playwright_browser_take_screenshot       │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│ Bot replies via WhatsApp/Telegram:              │
│ "✅ Pencarian selesai! [screenshot]"            │
└─────────────────────────────────────────────────┘
```

---

## 🧪 Test It Now!

### Step 1: Send test message
Via WhatsApp atau Telegram, kirim:
```
buka google dan cari ahmad faris
```

### Step 2: Watch the magic ✨
Bot akan:
1. Auto-detect keyword "buka google"
2. Load persona QA
3. Execute browser automation tools
4. Reply dengan screenshot

### Step 3: Verify
Check reply dari bot:
- ✅ Ada screenshot hasil pencarian?
- ✅ Format reply sesuai QA persona?
- ✅ No errors?

---

## 📝 Available Commands

### Google Search
```
buka google, cari [keyword]
buka google dan cari [keyword], screenshot
```

### URL Navigation
```
buka [URL]
buka staging.chronicle.rip
buka staging.chronicle.rip dan screenshot
```

### Login Testing
```
test login staging dengan email [email]
test login [URL] username [user] password [pass]
```

### Element Verification
```
buka [URL] dan cek apakah ada [element]
cek ada tombol Submit di staging
```

### Form Testing
```
test form di [URL] dengan nama [name] email [email]
```

### Screenshot Only
```
screenshot google.com
screenshot staging.chronicle.rip
```

---

## 🎨 Customization

### Add More Commands

Edit `persona/QA.md` untuk tambah custom workflows:

```markdown
**User:** "test checkout flow"

**Bot MUST EXECUTE:**
1. Login
2. Add to cart
3. Checkout
4. Verify order
5. Screenshot each step
```

### Add Test Credentials

Store di environment variables:
```bash
export TEST_EMAIL="test@example.com"
export TEST_PASSWORD="secure_password"
```

Bot akan auto-read dari env vars.

### Custom Keywords

Edit `CONTEXT.md` untuk tambah trigger keywords:
```markdown
### QA Keywords
**Triggers:** ... , `new_keyword`, `another_trigger`
```

---

## 🔒 Security Notes

### ✅ Safe Practices
- Use **staging environment** only
- Store credentials di **env vars** atau **secure config**
- **Separate Chrome profile** untuk testing
- **Never commit** credentials to git

### ❌ Avoid
- Testing di production dengan real data
- Hard-coding credentials
- Over-testing (rate limiting)
- Running tests pada peak hours

---

## 🐛 Troubleshooting

### Issue: Bot tidak respond
**Solution:**
1. Check keyword di CONTEXT.md
2. Verify persona/QA.md loaded
3. Check bot logs

### Issue: Browser tidak buka
**Solution:**
1. Verify Playwright installed
2. Check browser config di Moltbot
3. Run `moltbot browser status`

### Issue: Screenshot tidak attach
**Solution:**
1. Check file permissions
2. Verify screenshot path writable
3. Check media upload config

---

## 📚 Resources

### Documentation
- [BROWSER-AUTOMATION-EXAMPLES.md](BROWSER-AUTOMATION-EXAMPLES.md) - Examples
- [BROWSER-TESTING.md](BROWSER-TESTING.md) - Technical setup
- [persona/QA.md](../persona/QA.md) - Persona instructions

### Code References
- Moltbot browser tools: `moltbot/src/browser/`
- MCP Playwright integration: Built-in

---

## 🎉 You're Ready!

Bot Anda sekarang bisa:
- ✅ Auto-detect browser commands
- ✅ Execute Playwright automation
- ✅ Reply dengan screenshot & status
- ✅ Handle complex workflows

**Try it now via WhatsApp/Telegram!** 🚀

---

**Setup by:** Ahmad Faris
**Date:** 2026-01-29
**Status:** ✅ Production Ready
