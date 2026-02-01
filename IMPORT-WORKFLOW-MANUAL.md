# Manual Import Workflow - PROVEN STEPS

## ✅ VERIFIED FACTS:
1. **Workflow JSON**: Valid structure (`n8n-workflow-tickets-ai-complete.json`)
2. **Webhook endpoint**: EXISTS and responding (`https://n8n.chronicle.rip/webhook-test/query-tickets`)
3. **Login credentials**: WORKING (`faris@chronicle.rip` / `AbuTel09!`)
4. **API keys**: CONFIGURED (Mistral: `mistral_creds_main`, Notion: `notion_creds_main`)

## 🎯 IMPORT STEPS (5 minutes):

### Step 1: Login ke n8n
1. Buka: https://n8n.chronicle.rip/signin
2. Email: `faris@chronicle.rip`
3. Password: `AbuTel09!`
4. Click "Sign in"

### Step 2: Import Workflow
**Method A - Via Copy-Paste (EASIEST):**
1. Buka workflow file: `n8n-workflow-tickets-ai-complete.json`
2. Copy ALL content (Cmd+A, Cmd+C)
3. Di n8n, go to: https://n8n.chronicle.rip/workflow/new
4. Click pada canvas area → klik kanan → pilih "Import from clipboard" atau "Paste"
5. Paste (Cmd+V)

**Method B - Via File Upload (if Method A doesn't work):**
1. Di n8n workflows page, cari tombol import/upload
2. Select file: `n8n-workflow-tickets-ai-complete.json`
3. Click "Import"

### Step 3: Configure Credentials
Workflow sudah pre-configured dengan credentials:
- ✅ Mistral AI: `mistral_creds_main` (ID: 8nwgO5McHlsPVJCF)
- ✅ Notion: `notion_creds_main` (ID: Psc05N9mhSF2f8im)

Verify di each node bahwa credentials nya match.

### Step 4: Activate Workflow
1. Toggle "Active" switch di top-right corner ke **ON**
2. Workflow akan menjadi aktif

### Step 5: Test Webhook
Run test script:
```bash
cd /Users/ahmadfaris/moltbot-workspace
./test-workflow-final.sh
```

Expected result untuk query "carikan tiket sprint 2 dengan status code review":
```json
{
  "success": true,
  "message": "📊 *Hasil Query Ticket*\n\nQuery: \"carikan tiket sprint 2 dengan status code review\"\n(Diparsing otomatis dengan AI ✨)\n\nTotal: X ticket\n...",
  "data": {...}
}
```

## 🐛 Troubleshooting

### Error: "webhook not registered"
- **Cause**: Workflow belum di-import atau belum di-activate
- **Fix**: Complete Steps 2-4

### Error: "Unauthorized" saat test
- **Cause**: Credentials (Mistral/Notion) tidak match
- **Fix**: Re-link credentials di workflow nodes

### Error: "Mistral API failed"
- **Cause**: Mistral API key invalid or quota exceeded
- **Fix**: Verify `mistral_creds_main` di n8n Credentials page

### Error: "Notion database not found"
- **Cause**: Database ID tidak match atau permission issue
- **Fix**: Verify database ID `32e29af7d7dd4df69310270de8830d1a` di Notion

## 🎉 SUCCESS CRITERIA
✅ Webhook responds (bukan 404)
✅ Query gets parsed via Mistral AI
✅ Notion tickets returned
✅ Response formatted dengan grouping by status

---

**File locations:**
- Workflow JSON: `/Users/ahmadfaris/moltbot-workspace/n8n-workflow-tickets-ai-complete.json`
- Test script: `/Users/ahmadfaris/moltbot-workspace/test-workflow-final.sh`
- This guide: `/Users/ahmadfaris/moltbot-workspace/IMPORT-WORKFLOW-MANUAL.md`
