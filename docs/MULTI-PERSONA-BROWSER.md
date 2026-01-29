# 🤝 Multi-Persona Browser Automation

Bot sekarang support **browser automation di multiple personas** dengan **scope berbeda** dan **smart handoff**!

---

## 🎯 Persona Mapping

### 🤖 ASSISTANT Persona
**Scope:** Simple browsing tasks

**Can Handle:**
- ✅ Google search + screenshot
- ✅ Navigate to URL + screenshot
- ✅ Basic web browsing
- ✅ Simple form filling (search boxes)

**Cannot Handle:**
- ❌ Login testing
- ❌ Form verification
- ❌ Multi-step workflows
- ❌ Bug ticket creation
- ❌ Complex element verification

**Trigger Keywords:**
- `cari di google [keyword]`
- `google search [keyword]`
- `screenshot [URL]`
- `buka [URL]` (simple navigation)

---

### 🔍 QA Persona
**Scope:** Complex testing workflows

**Can Handle:**
- ✅ Login testing
- ✅ Form verification & testing
- ✅ Multi-step workflows (checkout, registration)
- ✅ Element verification
- ✅ Bug ticket creation
- ✅ Test case execution
- ✅ UAT automation

**Trigger Keywords:**
- `test login [URL]`
- `test form [URL]`
- `verify element [description]`
- `test workflow [description]`
- `buka browser` (dalam konteks testing)

---

## 🔄 Smart Handoff System

### Example 1: Simple Task → ASSISTANT handles

**User kirim:**
```
cari di google ahmad faris
```

**Bot behavior:**
1. ✅ Detect keyword "cari di google"
2. ✅ Load ASSISTANT persona
3. ✅ Execute browser automation (navigate, search, screenshot)
4. ✅ Reply dengan hasil

**Output:**
```
✅ Pencarian selesai!

🔍 Keyword: ahmad faris
📸 Screenshot terlampir

[Screenshot hasil Google]
```

---

### Example 2: Complex Task → Auto-switch to QA

**User kirim:**
```
test login staging.chronicle.rip dengan email test@example.com
```

**Bot behavior:**
1. ✅ Detect keyword "test login"
2. ✅ Load QA persona (auto-switch dari ASSISTANT jika aktif)
3. ✅ Execute complex testing workflow
4. ✅ Reply dengan hasil test + screenshot

**Output:**
```
✅ Login Test PASSED

📧 Email: test@example.com
🎯 Result: Login successful
⏱️ Time: 2.3s

📸 Screenshot dashboard:
[Screenshot]
```

---

### Example 3: ASSISTANT Handoff to QA

**User kirim (ke ASSISTANT):**
```
test form registration di staging
```

**ASSISTANT detects complex task:**
```
🔄 Request untuk testing kompleks terdeteksi!

⚠️ Form testing memerlukan QA persona yang lebih advanced.
Silakan gunakan command:

📋 Cara 1: Force QA mode
mode qa

📋 Cara 2: Use QA keyword
"test form staging.chronicle.rip"

💡 Atau bisa langsung bilang: "test login" / "verify element" untuk auto-switch ke QA mode.
```

**User follow-up:**
```
mode qa
test form registration di staging
```

**QA persona handles:**
1. ✅ Execute complex form testing
2. ✅ Verify all fields
3. ✅ Submit & verify response
4. ✅ Screenshot hasil
5. ✅ Create bug ticket jika ada issue

---

## 📊 Comparison Table

| Feature | ASSISTANT | QA |
|---------|-----------|-----|
| **Google Search** | ✅ Yes | ✅ Yes |
| **Screenshot URL** | ✅ Yes | ✅ Yes |
| **Navigate to URL** | ✅ Yes | ✅ Yes |
| **Login Testing** | ❌ No → Handoff | ✅ Yes |
| **Form Testing** | ❌ No → Handoff | ✅ Yes |
| **Element Verification** | ❌ No → Handoff | ✅ Yes |
| **Multi-step Workflows** | ❌ No → Handoff | ✅ Yes |
| **Bug Ticket Creation** | ❌ No → Handoff | ✅ Yes |
| **Test Case Execution** | ❌ No → Handoff | ✅ Yes |

---

## 🎬 Real-World Scenarios

### Scenario 1: User tidak tahu persona mana

**User kirim:**
```
cari di google best restaurants jakarta
```

**Bot behavior:**
✅ ASSISTANT auto-detect & handle
✅ No need to specify persona
✅ Simple task = ASSISTANT territory

---

### Scenario 2: User mix simple & complex

**User kirim:**
```
cari di google staging.chronicle.rip, lalu test login dengan email test@example.com
```

**Bot behavior:**
1. ✅ ASSISTANT: Execute Google search
2. ✅ Detect "test login" → Auto-switch to QA
3. ✅ QA: Execute login testing
4. ✅ Reply dengan hasil both tasks

---

### Scenario 3: Parallel requests from multiple users

**User A (via WhatsApp):**
```
cari di google ahmad faris
```

**User B (via Telegram, same time):**
```
test login staging.chronicle.rip
```

**Bot behavior:**
✅ User A → ASSISTANT persona instance
✅ User B → QA persona instance
✅ Both run in parallel
✅ No conflict, each user gets proper persona

---

## 🔧 Technical Implementation

### Persona Detection Logic

```typescript
function detectPersona(userMessage: string): Persona {
  // Check QA keywords first (more specific)
  if (message.match(/test login|test form|verify element|test workflow/)) {
    return 'QA';
  }
  
  // Check ASSISTANT keywords (simpler)
  if (message.match(/cari di google|google search|screenshot|buka \w+/)) {
    // If message also has complex keywords, upgrade to QA
    if (message.match(/test|verify|form|login/)) {
      return 'QA';
    }
    return 'ASSISTANT';
  }
  
  // Default to AUTO mode
  return 'AUTO';
}
```

### Handoff Mechanism

**ASSISTANT detects complex task:**
1. Check if message contains testing keywords
2. If yes: Suggest mode switch or auto-switch
3. Reply with handoff message
4. Wait for user confirmation OR auto-switch

**QA detects simple task:**
1. Can handle simple tasks too (no handoff needed)
2. Execute dengan full capabilities
3. QA is superset of ASSISTANT browser capabilities

---

## 📝 Configuration Updates

### Files Modified

1. **`persona/ASSISTANT.md`**
   - ✅ Added COMMAND 3: BROWSER AUTOMATION (SIMPLE)
   - ✅ Clear scope definition
   - ✅ Handoff mechanism to QA

2. **`persona/QA.md`**
   - ✅ Updated to clarify complex testing scope
   - ✅ Cross-reference to ASSISTANT for simple tasks
   - ✅ Existing complex testing workflows intact

3. **`CONTEXT.md`**
   - ✅ Updated ASSISTANT keywords (added browser keywords)
   - ✅ Updated QA keywords (refined for complex testing)
   - ✅ Clear persona boundaries

---

## 🚀 Usage Examples

### Simple Tasks (ASSISTANT)

```bash
# Google search
"cari di google best pizza jakarta"

# Screenshot URL
"screenshot google.com"

# Navigate
"buka staging.chronicle.rip"

# Simple search on any site
"buka google dan cari moltbot github"
```

### Complex Tasks (QA)

```bash
# Login testing
"test login staging.chronicle.rip dengan email test@example.com"

# Form testing
"test form registration di staging"

# Element verification
"buka staging.chronicle.rip dan cek apakah ada tombol Create New"

# Multi-step workflow
"test checkout flow di staging"

# Bug verification
"verify bug TECH-123: user tidak bisa login dengan gmail"
```

### Mixed Tasks (Auto-switch)

```bash
# Start simple, escalate to complex
"cari di google staging.chronicle.rip, lalu test login"

# Will auto-switch from ASSISTANT to QA when "test login" detected
```

---

## 💡 Best Practices

### For Users:
1. ✅ Use natural language - bot will detect right persona
2. ✅ For simple browsing, any persona works
3. ✅ For testing, use "test" keyword to ensure QA persona
4. ✅ Can force persona switch: `mode qa` then command

### For Bot Operators:
1. ✅ Keep ASSISTANT scope simple (browsing only)
2. ✅ Keep QA scope complex (testing workflows)
3. ✅ Clear handoff messages when scope mismatch
4. ✅ Document new testing workflows in QA persona
5. ✅ Update keywords in CONTEXT.md when adding features

---

## 🎯 Success Metrics

### ASSISTANT Persona:
- ✅ Handles 80% of simple browsing requests
- ✅ <2s response time for searches
- ✅ Auto-handoff success rate: 95%+

### QA Persona:
- ✅ Handles 100% of testing workflows
- ✅ Bug ticket creation rate: 100% for test failures
- ✅ Test execution accuracy: 98%+

### Cross-Persona:
- ✅ Zero conflicts between personas
- ✅ Smooth handoff (no user confusion)
- ✅ Parallel execution support

---

## 🔗 Related Docs

- [BROWSER-AUTOMATION-EXAMPLES.md](BROWSER-AUTOMATION-EXAMPLES.md) - Detailed examples
- [persona/ASSISTANT.md](../persona/ASSISTANT.md) - ASSISTANT persona instructions
- [persona/QA.md](../persona/QA.md) - QA persona instructions
- [CONTEXT.md](../CONTEXT.md) - Keyword routing config

---

**Last Updated:** 2026-01-29
**Author:** Ahmad Faris
**Version:** 2.0 (Multi-Persona)
