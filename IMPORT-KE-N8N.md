# Import & Test Workflow - LANGKAH JELAS

## 1. Import Workflow ke n8n

1. Buka: https://n8n.chronicle.rip/
2. Klik **"+ New workflow"** (kanan atas)
3. Klik menu **"..."** → **"Import from JSON"**
4. Copy SEMUA isi file `n8n-workflow-tickets-ai-complete.json`
5. Paste ke dialog import
6. Klik **"Import"**

## 2. Set Credentials (AUTO sudah tersedia)

Workflow sudah include credential IDs:
- ✅ Mistral API: `mistral_creds_main` (ID: 8nwgO5McHlsPVJCF)
- ✅ Notion API: `notion_creds_main` (ID: Psc05N9mhSF2f8im)

Jika error credential, klik node → pilih credential dari dropdown.

## 3. Test Workflow (DI N8N EDITOR)

### Test 1: Natural Language Query
1. Klik node **"Webhook"** (paling kiri)
2. Klik **"Execute workflow"** (tombol play besar)
3. Di tab yang terbuka, POST data ini:

```bash
curl -X POST https://n8n.chronicle.rip/webhook-test/query-tickets \
  -H "Content-Type: application/json" \
  -d '{"query": "carikan tiket sprint 2 dengan status code review"}'
```

4. Lihat execution di canvas - setiap node akan show hasil
5. Klik node **"Mistral API"** → lihat AI response
6. Klik node **"Respond"** → lihat final output

### Test 2: Structured Query (No AI)
```bash
curl -X POST https://n8n.chronicle.rip/webhook-test/query-tickets \
  -H "Content-Type: application/json" \
  -d '{"sprint": "Sprint 2", "status": "Code review"}'
```

## 4. Activate Workflow

1. **PENTING:** Deactivate workflow lama dulu!
   - Buka: https://n8n.chronicle.rip/workflow/ow8azJXQ1x8yj9N9
   - Klik toggle **"Active"** → OFF

2. Balik ke workflow baru
3. Klik toggle **"Active"** (kanan atas) → ON
4. Webhook production siap: `https://n8n.chronicle.rip/webhook/query-tickets`

## 5. Test Production Webhook

```bash
curl -X POST https://n8n.chronicle.rip/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{"query": "carikan tiket sprint 2 dengan status code review"}' | jq
```

## Expected Output

```json
{
  "success": true,
  "message": "📊 *Hasil Query Ticket*\n\nQuery: \"carikan tiket sprint 2 dengan status code review\"\n(Diparsing otomatis dengan AI ✨)\n\nTotal: X ticket\nSprint: Sprint 2\nStatus: Code review\n\n---\n\n*Code review* (X):\n\n1. *[Ticket Title]*\n   Sprint: Sprint 2\n   Assignee: [Name]\n   Priority: [Priority]\n   🔗 [URL]\n\n---\n⏰ Generated: [Timestamp]",
  "data": {
    "success": true,
    "count": X,
    "params": {
      "sprint": "Sprint 2",
      "status": "Code review",
      "databaseId": "32e29af7d7dd4df69310270de8830d1a"
    },
    "tickets": [...]
  }
}
```

## Troubleshooting

❌ **"webhook not registered"** → Workflow belum active, klik "Execute workflow" dulu
❌ **Mistral API error** → Check credential ID, pastikan API key valid
❌ **No tickets found** → Check Notion database properties (Sprint, Status names case-sensitive)
❌ **Empty response** → Old workflow conflict, deactivate workflow ID ow8azJXQ1x8yj9N9

---

**LANGKAH SELANJUTNYA:** Setelah test berhasil → buat Moltbot skill untuk WhatsApp integration!
