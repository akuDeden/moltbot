# 🤖 Browser Automation Examples

Bot sekarang bisa melakukan **automated browser testing** langsung dari WhatsApp/Telegram!

## ✅ Cara Kerja

1. **User kirim perintah** via WhatsApp/Telegram
2. **Bot detect keywords** → Auto-load `persona/QA.md`
3. **Bot execute MCP Playwright tools** → Navigate, click, type, screenshot
4. **Bot reply dengan hasil** → Screenshot + status (success/fail)

---

## 🎯 Contoh Perintah User

### Example 1: Google Search + Screenshot

**User mengetik:**
```
buka google, cari ahmad faris, dan screenshot hasilnya
```

**Bot akan otomatis:**
1. ✅ Buka https://www.google.com
2. ✅ Isi search box dengan "ahmad faris"
3. ✅ Tekan Enter
4. ✅ Tunggu hasil load
5. ✅ Ambil screenshot full page
6. ✅ Reply dengan screenshot

**Expected Output:**
```
✅ Pencarian selesai!

🔍 Keyword: ahmad faris
📸 Screenshot terlampir

[Screenshot hasil pencarian Google]
```

---

### Example 2: Test Login Staging

**User mengetik:**
```
test login staging.chronicle.rip dengan email test@example.com
```

**Bot akan otomatis:**
1. ✅ Navigate ke staging.chronicle.rip/login
2. ✅ Ambil snapshot untuk get form refs
3. ✅ Isi email field: test@example.com
4. ✅ Isi password field (dari config)
5. ✅ Click tombol "Sign in"
6. ✅ Wait for dashboard page
7. ✅ Verify login sukses
8. ✅ Screenshot dashboard
9. ✅ Reply hasil

**Expected Output (Success):**
```
✅ Login Test PASSED

📧 Email: test@example.com
🔐 Password: [hidden]
🎯 Result: Login successful
⏱️ Time: 2.3s

📸 Screenshot dashboard:
[Screenshot halaman dashboard]
```

**Expected Output (Failed):**
```
❌ Login Test FAILED

📧 Email: test@example.com
🔐 Password: [hidden]
❗ Error: Invalid credentials

📸 Screenshot error page:
[Screenshot halaman error]

🐛 Bug ticket created: [Notion link]
```

---

### Example 3: Browse & Verify Element

**User mengetik:**
```
buka staging.chronicle.rip dan cek apakah ada tombol "Create New"
```

**Bot akan otomatis:**
1. ✅ Navigate ke staging.chronicle.rip
2. ✅ Ambil snapshot page
3. ✅ Search untuk button "Create New" di snapshot
4. ✅ Screenshot page
5. ✅ Reply hasil

**Expected Output (Found):**
```
✅ Element Found!

🔍 Looking for: button "Create New"
📍 Location: Top right corner
✅ Status: Element exists

📸 Screenshot:
[Screenshot dengan highlight element]
```

**Expected Output (Not Found):**
```
❌ Element Not Found!

🔍 Looking for: button "Create New"
❌ Status: Element does not exist on page

📸 Screenshot:
[Screenshot full page]

💡 Suggestion: Mungkin element masih loading atau ID/class berubah?
```

---

### Example 4: Form Testing

**User mengetik:**
```
test form contact di staging, isi nama Ahmad, email test@mail.com, pesan "Testing automation"
```

**Bot akan otomatis:**
1. ✅ Navigate ke staging contact form
2. ✅ Ambil snapshot form
3. ✅ Fill fields:
   - Name: Ahmad
   - Email: test@mail.com
   - Message: Testing automation
4. ✅ Click submit
5. ✅ Verify success message
6. ✅ Screenshot hasil
7. ✅ Reply

**Expected Output:**
```
✅ Form Test PASSED

📝 Test Data:
• Name: Ahmad
• Email: test@mail.com
• Message: Testing automation

✅ Result: Form submitted successfully
📩 Confirmation: "Thank you for your message"

📸 Screenshot:
[Screenshot success message]
```

---

### Example 5: Multi-Step Workflow

**User mengetik:**
```
test checkout flow di staging: 
1. Login
2. Tambah produk ke cart
3. Checkout
4. Verifikasi order
```

**Bot akan otomatis:**
1. ✅ Login ke staging
2. ✅ Navigate ke product page
3. ✅ Click "Add to Cart"
4. ✅ Go to cart page
5. ✅ Click "Checkout"
6. ✅ Fill shipping info
7. ✅ Complete payment (test mode)
8. ✅ Verify order success
9. ✅ Screenshot setiap step
10. ✅ Reply summary

**Expected Output:**
```
✅ Checkout Flow Test PASSED

📋 Test Steps:
1. ✅ Login successful
2. ✅ Product added to cart
3. ✅ Checkout page loaded
4. ✅ Shipping info filled
5. ✅ Payment completed (test mode)
6. ✅ Order confirmed

📦 Order ID: ORD-12345
💰 Total: $99.99

📸 Screenshots:
[4 screenshots dari step penting]

⏱️ Total time: 8.2s
```

---

## 🔧 Technical Details

### MCP Tools Used

Bot menggunakan **Playwright MCP tools** yang sudah terintegrasi:

1. **`mcp_playwright_browser_navigate`**
   - Buka URL
   - Wait for page load

2. **`mcp_playwright_browser_snapshot`**
   - Ambil struktur page
   - Get element refs (e1, e2, dll)

3. **`mcp_playwright_browser_click`**
   - Klik element (butuh ref)
   - Support double-click, right-click

4. **`mcp_playwright_browser_fill_form`**
   - Isi multiple form fields sekaligus
   - Support textbox, checkbox, radio, combobox

5. **`mcp_playwright_browser_press_key`**
   - Tekan keyboard key
   - Support: Enter, Tab, Escape, Arrow keys, dll

6. **`mcp_playwright_browser_take_screenshot`**
   - Full page atau element-specific
   - Format: PNG/JPEG

7. **`activate_form_and_file_management_tools`**
   - Activate tools untuk form filling
   - File upload support

---

## 📝 Configuration

### Trigger Keywords (Auto-load QA Persona)

Keywords yang memicu bot untuk auto-load `persona/QA.md`:

- `buka browser`
- `buka google`
- `cari di google`
- `screenshot`
- `test login`
- `test [feature]`
- `buka [URL]`

### Test Credentials

Credentials untuk testing stored di:
- Environment variables
- Secure config files
- **NEVER** commit credentials to git

---

## 🚀 Usage Tips

### Do's ✅
- Gunakan staging environment untuk automated tests
- Berikan detail yang cukup di perintah user
- Verifikasi hasil dengan screenshot
- Create bug ticket otomatis jika test fail

### Don'ts ❌
- ❌ Jangan test di production dengan real data
- ❌ Jangan hard-code credentials di code
- ❌ Jangan skip verification steps
- ❌ Jangan over-test (rate limiting)

---

## 🎭 Real-World Scenarios

### Scenario 1: Daily Smoke Test

**User schedule di cron:**
```
test smoke harian staging:
- Login page load
- Dashboard widgets render
- API health check
```

Bot will auto-run setiap pagi dan report hasil.

### Scenario 2: Bug Verification

**User:**
```
verify bug TECH-123: user tidak bisa login dengan email gmail
```

Bot will:
1. Try login dengan email gmail
2. Document hasil
3. Update Notion ticket dengan screenshot

### Scenario 3: Performance Check

**User:**
```
cek loading speed homepage staging
```

Bot will:
1. Navigate dengan network tracking
2. Measure load time
3. Screenshot dengan timing info
4. Report jika > threshold

---

## 📊 Success Metrics

Bot tracks dan report:
- ✅ Tests passed
- ❌ Tests failed
- ⏱️ Execution time
- 📸 Screenshot count
- 🐛 Bugs found & reported

---

## 🔗 Related Docs

- [BROWSER-TESTING.md](BROWSER-TESTING.md) - Setup & capabilities
- [BROWSER-EXAMPLES.md](BROWSER-EXAMPLES.md) - Detailed step-by-step examples
- [persona/QA.md](../persona/QA.md) - QA persona instructions

---

**Last Updated:** 2026-01-29
**Author:** Ahmad Faris
**Version:** 1.0
