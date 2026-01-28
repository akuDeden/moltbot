# Browser Testing Examples - Detailed Workflows

Contoh lengkap penggunaan Moltbot browser tool untuk automated testing.

## 🎯 Example 1: Login Test (Step-by-Step)

### User Command
```
test login staging.chronicle.rip
```

### Bot Workflow

**Step 1: Start Browser (Managed Profile)**
```bash
moltbot browser --browser-profile clawd start
```
Output:
```
✅ Browser started (clawd profile)
PID: 12345
User data: ~/.moltbot/browser/clawd
```

**Step 2: Navigate to Login Page**
```bash
moltbot browser --browser-profile clawd navigate https://staging.chronicle.rip/login
```
Output:
```
✅ Navigated to https://staging.chronicle.rip/login
Status: 200 OK
```

**Step 3: Take Snapshot (Get Element Refs)**
```bash
moltbot browser --browser-profile clawd snapshot --interactive
```
Output:
```markdown
# staging.chronicle.rip - Login

[ref=e1] main "Main Content"
  [ref=e12] heading "Welcome Back"
  [ref=e15] form "Login Form"
    [ref=e23] textbox "Email" (placeholder: "Enter your email")
    [ref=e24] textbox "Password" (type=password)
    [ref=e25] checkbox "Remember me"
    [ref=e14] button "Sign in"
  [ref=e30] link "Forgot password?"
  [ref=e31] link "Create account"
```

**Step 4: Read Test Credentials**
```python
# Bot reads test-credentials.json
import json
with open('test-credentials.json') as f:
    creds = json.load(f)
    email = creds['staging']['email']      # "test@example.com"
    password = creds['staging']['password']  # "Test123!@#"
```

**Step 5: Fill Email Field**
```bash
moltbot browser --browser-profile clawd type e23 "test@example.com"
```
Output:
```
✅ Typed into e23 (textbox "Email")
Value: "test@example.com"
```

**Step 6: Fill Password Field**
```bash
moltbot browser --browser-profile clawd type e24 "Test123!@#"
```
Output:
```
✅ Typed into e24 (textbox "Password")
Value: [hidden]
```

**Step 7: Click Sign In Button**
```bash
moltbot browser --browser-profile clawd click e14
```
Output:
```
✅ Clicked e14 (button "Sign in")
Form submitted
```

**Step 8: Wait for Dashboard**
```bash
moltbot browser --browser-profile clawd wait --url "**/dashboard" --timeout 10000
```
Output:
```
✅ URL matched: https://staging.chronicle.rip/dashboard
Wait time: 1.2s
```

**Step 9: Verify Success (Take Snapshot)**
```bash
moltbot browser --browser-profile clawd snapshot --interactive
```
Output:
```markdown
# Dashboard - Chronicle

[ref=e1] banner "Welcome, Test User!"
[ref=e5] navigation "Main Navigation"
  [ref=e10] link "Dashboard" (current)
  [ref=e11] link "Projects"
  [ref=e12] link "Settings"
```

**Step 10: Take Screenshot as Proof**
```bash
moltbot browser --browser-profile clawd screenshot --full-page --output login-success.png
```
Output:
```
✅ Screenshot saved: login-success.png
Size: 1920x1080
Format: PNG
```

**Step 11: Report to User**
```
✅ LOGIN TEST PASSED - staging.chronicle.rip

Duration: 3.5s

Steps Executed:
1. ✅ Browser started (clawd profile)
2. ✅ Navigated to login page
3. ✅ Found login form (email, password, submit)
4. ✅ Entered email: test@example.com
5. ✅ Entered password: ********
6. ✅ Clicked "Sign in" button
7. ✅ Redirected to /dashboard (1.2s)
8. ✅ Welcome banner detected: "Welcome, Test User!"

Screenshot: login-success.png
```

---

## 🐛 Example 2: Bug Reproduction with Error Detection

### User Command
```
reproduce bug: cart button not working di staging
```

### Bot Workflow

**Step 1-2: Start & Navigate**
```bash
moltbot browser --browser-profile clawd start
moltbot browser --browser-profile clawd navigate https://staging.chronicle.rip/products
```

**Step 3: Take Before Screenshot**
```bash
moltbot browser --browser-profile clawd screenshot --output before-cart-bug.png
```

**Step 4: Get Snapshot**
```bash
moltbot browser --browser-profile clawd snapshot --interactive
```
Output:
```markdown
[ref=e20] list "Products"
  [ref=e21] article "Product 1"
    [ref=e45] button "Add to Cart" (🛒)
  [ref=e22] article "Product 2"
    [ref=e46] button "Add to Cart" (🛒)
```

**Step 5: Click Cart Button**
```bash
moltbot browser --browser-profile clawd click e45
```
Output:
```
✅ Clicked e45 (button "Add to Cart")
```

**Step 6: Wait for Cart (With Timeout)**
```bash
moltbot browser --browser-profile clawd wait ".cart-modal" --timeout 3000
```
Output:
```
❌ Timeout waiting for selector: .cart-modal
Wait time: 3000ms (exceeded)
```

**Step 7: Check Console Errors**
```bash
moltbot browser --browser-profile clawd console --level error
```
Output:
```
[ERROR] cart.js:45 - Uncaught TypeError: Cannot read property 'id' of undefined
  at addToCart (cart.js:45:12)
  at HTMLButtonElement.onclick (products:1:25)

[ERROR] Failed to fetch cart data
  Network error: 500 Internal Server Error
```

**Step 8: Take After Screenshot**
```bash
moltbot browser --browser-profile clawd screenshot --output after-cart-bug.png
```

**Step 9: Take Snapshot Again**
```bash
moltbot browser --browser-profile clawd snapshot --interactive
```
Output:
```markdown
# Same as before - no cart modal appeared
[ref=e20] list "Products"
  [ref=e21] article "Product 1"
    [ref=e45] button "Add to Cart" (unchanged)
```

**Step 10: Auto-Create Bug Ticket**
```bash
python scripts/create-bug-ticket.py \
  "Cart button tidak berfungsi di Products page" \
  "Bug terdeteksi saat automated testing di staging.chronicle.rip/products

**Steps to Reproduce:**
1. Navigate to /products
2. Click 'Add to Cart' button (ref e45)
3. Cart modal tidak muncul

**Expected:** Cart modal should appear
**Actual:** Button tidak respond, console error detected

**Console Errors:**
- cart.js:45 - TypeError: Cannot read property 'id' of undefined
- Network error: 500 Internal Server Error

**Screenshots:**
- before-cart-bug.png (before click)
- after-cart-bug.png (after click - no change)

**Environment:**
- URL: staging.chronicle.rip/products
- Browser: Chrome (Clawd profile)
- Timestamp: 2026-01-28 15:30:00

**Element Details:**
[ref=e45] button 'Add to Cart' at Product 1" \
  "High"
```
Output:
```
✅ Bug ticket created!
ID: BUG-2026-028
URL: https://notion.so/Cart-button-tidak-berfungsi-...
Severity: High (P2)
Database: Bug Report (482be0a206b044d99fff5798db2381e4)
```

**Step 11: Report to User**
```
❌ BUG REPRODUCED - staging.chronicle.rip/products

Issue: Cart button tidak berfungsi

Test Duration: 5.2s

Steps Executed:
1. ✅ Browser started
2. ✅ Navigated to /products
3. ✅ Found cart button (ref e45)
4. ✅ Clicked button
5. ❌ Cart modal TIDAK MUNCUL (timeout 3s)
6. ❌ Console errors detected:
   - TypeError: Cannot read property 'id' of undefined
   - Network error: 500 Internal Server Error

🐛 Bug Ticket Created:
   ID: BUG-2026-028
   Severity: High (P2)
   URL: https://notion.so/...

📸 Screenshots:
   - before-cart-bug.png
   - after-cart-bug.png
```

---

## 🧪 Example 3: Form Validation Testing

### User Command
```
test form validation di login page staging
```

### Bot Workflow

**Setup**
```bash
moltbot browser --browser-profile clawd start
moltbot browser --browser-profile clawd navigate https://staging.chronicle.rip/login
moltbot browser --browser-profile clawd snapshot --interactive
```

### Test Case 1: Empty Form Submission

**Action:**
```bash
# Don't fill any fields, just click submit
moltbot browser --browser-profile clawd click e14
```

**Wait for validation:**
```bash
moltbot browser --browser-profile clawd wait ".error-message" --timeout 2000
```

**Check snapshot:**
```bash
moltbot browser --browser-profile clawd snapshot --interactive
```
Output:
```markdown
[ref=e23] textbox "Email" 
  [ref=e26] alert "Email is required" (error)
[ref=e24] textbox "Password"
  [ref=e27] alert "Password is required" (error)
```

**Result:**
```
✅ TEST CASE 1 PASSED
Empty form submission → Validation errors shown
- Email field: "Email is required"
- Password field: "Password is required"
```

### Test Case 2: Invalid Email Format

**Action:**
```bash
moltbot browser --browser-profile clawd type e23 "not-an-email"
moltbot browser --browser-profile clawd click e14
```

**Check snapshot:**
```bash
moltbot browser --browser-profile clawd snapshot --interactive
```
Output:
```markdown
[ref=e23] textbox "Email" (value: "not-an-email")
  [ref=e26] alert "Please enter a valid email address" (error)
```

**Result:**
```
✅ TEST CASE 2 PASSED
Invalid email → Validation error shown
- "Please enter a valid email address"
```

### Test Case 3: Password Too Short

**Action:**
```bash
moltbot browser --browser-profile clawd type e23 "test@example.com" --submit
moltbot browser --browser-profile clawd type e24 "123" --submit
moltbot browser --browser-profile clawd click e14
```

**Check snapshot:**
```bash
moltbot browser --browser-profile clawd snapshot --interactive
```
Output:
```markdown
[ref=e24] textbox "Password" (value: "***")
  [ref=e27] alert "Password must be at least 8 characters" (error)
```

**Result:**
```
✅ TEST CASE 3 PASSED
Weak password → Validation error shown
- "Password must be at least 8 characters"
```

### Test Case 4: Valid Credentials

**Action:**
```bash
# Clear and re-fill with valid data
moltbot browser --browser-profile clawd type e23 "test@example.com" --submit
moltbot browser --browser-profile clawd type e24 "Test123!@#" --submit
moltbot browser --browser-profile clawd click e14
```

**Wait for success:**
```bash
moltbot browser --browser-profile clawd wait --url "**/dashboard" --timeout 10000
```
Output:
```
✅ URL matched: https://staging.chronicle.rip/dashboard
```

**Result:**
```
✅ TEST CASE 4 PASSED
Valid credentials → Login successful
- Redirected to /dashboard
```

### Final Report

```
✅ FORM VALIDATION TEST COMPLETED - staging.chronicle.rip/login

Duration: 8.3s

Test Results: 4/4 PASSED ✅

1. ✅ Empty form submission
   Expected: Validation errors
   Actual: ✅ "Email is required", "Password is required"

2. ✅ Invalid email format
   Expected: Email validation error
   Actual: ✅ "Please enter a valid email address"

3. ✅ Password too short
   Expected: Password length validation
   Actual: ✅ "Password must be at least 8 characters"

4. ✅ Valid credentials
   Expected: Login success → /dashboard
   Actual: ✅ Redirected to dashboard in 1.2s

Overall: Login form validation working correctly! ✅
```

---

## 🎬 Example 4: Multi-Step E2E Test (Complete User Flow)

### User Command
```
test checkout flow di staging
```

### Bot Workflow

**Full E2E Test: Login → Add Product → Checkout → Payment**

```bash
# 1. Login
moltbot browser --browser-profile clawd start
moltbot browser --browser-profile clawd navigate https://staging.chronicle.rip/login
moltbot browser --browser-profile clawd snapshot --interactive
moltbot browser --browser-profile clawd type e23 "test@example.com"
moltbot browser --browser-profile clawd type e24 "Test123!@#"
moltbot browser --browser-profile clawd click e14
moltbot browser --browser-profile clawd wait --url "**/dashboard"
# ✅ Login complete

# 2. Navigate to Products
moltbot browser --browser-profile clawd navigate https://staging.chronicle.rip/products
moltbot browser --browser-profile clawd snapshot --interactive
# Found: [ref=e45] button "Add to Cart"

# 3. Add Product to Cart
moltbot browser --browser-profile clawd click e45
moltbot browser --browser-profile clawd wait ".cart-badge[data-count='1']" --timeout 3000
# ✅ Product added to cart

# 4. Open Cart
moltbot browser --browser-profile clawd snapshot --interactive
# Found: [ref=e50] link "Cart (1)"
moltbot browser --browser-profile clawd click e50
moltbot browser --browser-profile clawd wait --url "**/cart"
# ✅ Cart page loaded

# 5. Proceed to Checkout
moltbot browser --browser-profile clawd snapshot --interactive
# Found: [ref=e60] button "Proceed to Checkout"
moltbot browser --browser-profile clawd click e60
moltbot browser --browser-profile clawd wait --url "**/checkout"
# ✅ Checkout page loaded

# 6. Fill Shipping Info
moltbot browser --browser-profile clawd snapshot --interactive
# Found form fields:
# [ref=e70] textbox "Full Name"
# [ref=e71] textbox "Address"
# [ref=e72] textbox "City"
# [ref=e73] textbox "Postal Code"

moltbot browser --browser-profile clawd fill \
  e70 "Test User" \
  e71 "123 Test Street" \
  e72 "Test City" \
  e73 "12345"
# ✅ Shipping info filled

# 7. Continue to Payment
moltbot browser --browser-profile clawd snapshot --interactive
# Found: [ref=e80] button "Continue to Payment"
moltbot browser --browser-profile clawd click e80
moltbot browser --browser-profile clawd wait --url "**/checkout/payment"
# ✅ Payment page loaded

# 8. Select Payment Method
moltbot browser --browser-profile clawd snapshot --interactive
# Found: [ref=e90] radio "Credit Card"
moltbot browser --browser-profile clawd click e90

# 9. Fill Payment Details
# Found fields:
# [ref=e95] textbox "Card Number"
# [ref=e96] textbox "Expiry (MM/YY)"
# [ref=e97] textbox "CVV"

moltbot browser --browser-profile clawd fill \
  e95 "4242424242424242" \
  e96 "12/28" \
  e97 "123"
# ✅ Payment details filled

# 10. Complete Order
moltbot browser --browser-profile clawd snapshot --interactive
# Found: [ref=e100] button "Complete Order"
moltbot browser --browser-profile clawd click e100
moltbot browser --browser-profile clawd wait --url "**/order-confirmation" --timeout 15000
# ✅ Order completed

# 11. Verify Order Confirmation
moltbot browser --browser-profile clawd snapshot --interactive
```

Output:
```markdown
[ref=e1] main "Order Confirmation"
  [ref=e5] heading "Thank you for your order!"
  [ref=e10] text "Order #TEST-2026-001"
  [ref=e15] text "Confirmation sent to test@example.com"
```

**Final Screenshot:**
```bash
moltbot browser --browser-profile clawd screenshot --full-page --output checkout-success.png
```

**Report:**
```
✅ CHECKOUT FLOW TEST PASSED - staging.chronicle.rip

Total Duration: 24.5s

Steps Executed:
1. ✅ Login (1.2s)
2. ✅ Navigate to Products (0.8s)
3. ✅ Add to Cart (2.1s)
4. ✅ Open Cart page (0.9s)
5. ✅ Proceed to Checkout (1.3s)
6. ✅ Fill Shipping Info (3.5s)
7. ✅ Continue to Payment (1.1s)
8. ✅ Select Payment Method (0.5s)
9. ✅ Fill Payment Details (2.8s)
10. ✅ Complete Order (8.2s)
11. ✅ Order Confirmation received

Order Details:
- Order ID: TEST-2026-001
- Confirmation: test@example.com
- Total: Rp 150.000

Screenshot: checkout-success.png

🎉 Complete checkout flow working end-to-end!
```

---

## 🔥 Example 5: Performance Testing with Timing

### User Command
```
test performance loading dashboard staging
```

### Bot Workflow

```bash
# 1. Start with timing
START_TIME=$(date +%s%3N)

# 2. Navigate
moltbot browser --browser-profile clawd navigate https://staging.chronicle.rip/dashboard

# 3. Wait for different load states
moltbot browser --browser-profile clawd wait --load domcontentloaded
DOMLOADED=$(date +%s%3N)

moltbot browser --browser-profile clawd wait --load networkidle
NETWORKIDLE=$(date +%s%3N)

# 4. Check for specific elements
moltbot browser --browser-profile clawd wait ".dashboard-widgets"
WIDGETS_LOADED=$(date +%s%3N)

# 5. Get performance metrics
moltbot browser --browser-profile clawd evaluate --function "() => {
  const perf = performance.getEntriesByType('navigation')[0];
  return {
    dns: perf.domainLookupEnd - perf.domainLookupStart,
    tcp: perf.connectEnd - perf.connectStart,
    request: perf.responseStart - perf.requestStart,
    response: perf.responseEnd - perf.responseStart,
    dom: perf.domComplete - perf.domLoading,
    load: perf.loadEventEnd - perf.loadEventStart
  };
}"
```

**Report:**
```
⚡ PERFORMANCE TEST - staging.chronicle.rip/dashboard

Load Times:
- DNS Lookup: 45ms
- TCP Connection: 32ms
- Request: 128ms
- Response: 245ms
- DOM Processing: 456ms
- Load Event: 89ms

Milestones:
- DOMContentLoaded: 810ms
- Network Idle: 1,234ms
- Dashboard Widgets: 1,567ms
- Fully Interactive: 2,100ms

Assessment:
✅ DNS: 45ms (Good - under 100ms)
✅ Response: 245ms (Good - under 500ms)
⚠️ Widgets: 1,567ms (Slow - should be under 1s)
⚠️ Interactive: 2,100ms (Slow - should be under 2s)

Recommendations:
1. Optimize dashboard widgets loading
2. Consider lazy loading for below-fold content
3. Reduce initial bundle size
```

---

## 📊 Summary: Test Command Patterns

| User Command | Bot Action | Use Case |
|-------------|-----------|----------|
| `test login staging` | Login flow test | Verify auth works |
| `reproduce bug [description]` | Bug reproduction + ticket | Validate & document bugs |
| `test form validation [page]` | All validation scenarios | QA form rules |
| `test checkout flow` | E2E multi-step test | Integration testing |
| `test performance [page]` | Load time metrics | Performance QA |
| `screenshot [page]` | Take full-page screenshot | Visual verification |
| `test [feature] staging` | Custom feature test | Ad-hoc testing |

---

## 🎯 Best Practices

1. **Always get fresh snapshot** before using refs
2. **Use `--interactive` flag** for role-based refs (clearer)
3. **Wait with timeouts** to avoid infinite hangs
4. **Check console errors** after failed interactions
5. **Take screenshots** before & after for bug reports
6. **Auto-create tickets** for reproducible bugs
7. **Use managed profile** (`clawd`) for testing, not `chrome`
8. **Test in staging first**, never production

Ready untuk automated testing! 🚀
