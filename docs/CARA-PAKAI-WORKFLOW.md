# 🚀 Cara Pakai Workflow Notion Tickets + AI

## Setup

### 1. Import Workflow
1. Buka n8n: `http://localhost:5678`
2. Klik **Import from File**
3. Pilih file: `n8n-workflow-tickets-ai-complete.json`

### 2. Set Mistral API Key
1. Buka workflow yang sudah diimport
2. Klik node **"Mistral AI"**
3. Klik **"Select Credential"** → **"Create New"**
4. Masukkan API Key: `jXiU2TQZM4Rj13JJD44Gp0mm4iLZVCJx`
5. Klik **"Save"**

### 3. Aktifkan Workflow
1. Klik toggle **"Active"** di kanan atas
2. Copy webhook URL (biasanya: `http://localhost:5678/webhook/query-tickets`)

---

## 🎯 Cara Input User

Ada **2 cara** kirim request:

### 1. **Natural Language (Pakai AI)** 🤖

Kirim query dalam bahasa natural, AI akan parsing otomatis!

**Contoh 1: Cari ticket sprint tertentu**
```bash
curl -X POST http://localhost:5678/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{
    "query": "cari ticket sprint 1 yang in progress"
  }'
```

**Contoh 2: Cari ticket by assignee**
```bash
curl -X POST http://localhost:5678/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{
    "message": "ticket ahmad yang high priority"
  }'
```

**Contoh 3: Cari ticket dengan keywords**
```bash
curl -X POST http://localhost:5678/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{
    "query": "tampilkan semua bug yang belum selesai"
  }'
```

**Contoh 4: Bahasa campuran**
```bash
curl -X POST http://localhost:5678/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{
    "query": "show me all blocked tickets in sprint 2"
  }'
```

---

### 2. **Structured Parameters (Skip AI)** ⚡

Kalau sudah tahu parameter yang mau dipakai, langsung kirim structured data (lebih cepat, skip AI):

**Contoh 1: Filter by sprint + status**
```bash
curl -X POST http://localhost:5678/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{
    "sprint": "Sprint 1",
    "status": "In progress"
  }'
```

**Contoh 2: Filter by assignee + priority**
```bash
curl -X POST http://localhost:5678/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{
    "assignee": "ahmad",
    "priority": "High"
  }'
```

**Contoh 3: Search keywords**
```bash
curl -X POST http://localhost:5678/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "bug",
    "limit": 20
  }'
```

**Contoh 4: Multiple filters**
```bash
curl -X POST http://localhost:5678/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{
    "sprint": "Sprint 2",
    "status": "Blocked",
    "tags": ["urgent", "bug"],
    "limit": 50
  }'
```

---

## 📋 Parameter yang Tersedia

| Parameter | Type | Contoh | Keterangan |
|-----------|------|--------|------------|
| `query` atau `message` | string | "cari ticket sprint 1" | Natural language query (pakai AI) |
| `sprint` | string | "Sprint 1" | Filter by sprint |
| `status` | string | "In progress" | Filter by status (Not started, In progress, Done, Blocked) |
| `keywords` | string | "bug fix" | Search in ticket title |
| `assignee` | string | "ahmad" | Filter by assignee name |
| `priority` | string | "High" | Filter by priority (High, Medium, Low) |
| `tags` | array | ["bug", "urgent"] | Filter by tags |
| `limit` | number | 50 | Max results (default: 100) |
| `database_id` | string | "32e29..." | Custom database ID (optional) |

---

## 🔄 Flow Logic

```
┌─────────────┐
│  Webhook    │ ← User kirim request
└──────┬──────┘
       │
       v
┌─────────────┐
│ Check Input │ ← Cek: natural language atau structured?
└──────┬──────┘
       │
       v
    ┌──┴──┐
    │ IF? │
    └──┬──┘
       │
   ┌───┴────────────────┐
   │                    │
   v                    v
[AI Path]          [Direct Path]
   │                    │
   v                    v
Mistral AI         Parse Direct
   │                    │
   v                    v
Parse AI Response      │
   │                    │
   └────────┬───────────┘
            │
            v
    ┌───────────┐
    │   Merge   │ ← Gabungkan hasil
    └─────┬─────┘
          │
          v
    ┌─────────────┐
    │Build Filter │ ← Buat Notion filter
    └──────┬──────┘
          │
          v
    ┌─────────────┐
    │Get Tickets  │ ← Query Notion
    └──────┬──────┘
          │
          v
    ┌──────────────┐
    │Extract Data  │ ← Parse ticket data
    └──────┬───────┘
          │
          v
    ┌──────────┐
    │  Format  │ ← Format output
    └─────┬────┘
          │
          v
    ┌──────────┐
    │ Respond  │ ← Return hasil
    └──────────┘
```

---

## 🎨 Response Format

Response akan berupa JSON dengan format:

```json
{
  "success": true,
  "message": "📊 *Hasil Query Ticket*\n\nQuery: \"cari ticket sprint 1 yang in progress\"\n(Diparsing otomatis dengan AI ✨)\n\nTotal: 3 ticket\nSprint: Sprint 1\nStatus: In progress\n\n---\n\n*In progress* (3):\n\n1. *Fix login bug*\n   Sprint: Sprint 1\n   Assignee: Ahmad\n   Priority: High\n   🔗 https://notion.so/...\n\n2. *Update dashboard*\n   Sprint: Sprint 1\n   Assignee: Budi\n   🔗 https://notion.so/...\n...",
  "data": {
    "count": 3,
    "params": {...},
    "tickets": [...]
  },
  "formatted": {
    "text": "...",
    "count": 3,
    "grouped_by_status": {...}
  }
}
```

---

## 🧪 Test Commands

Coba test dengan berbagai query:

```bash
# Test 1: Natural language Indonesia
curl -X POST http://localhost:5678/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{"query": "cari ticket sprint 1 yang in progress"}'

# Test 2: Natural language English
curl -X POST http://localhost:5678/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{"message": "show me all blocked tickets"}'

# Test 3: Structured (skip AI)
curl -X POST http://localhost:5678/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{"sprint": "Sprint 1", "status": "In progress"}'

# Test 4: Keywords search
curl -X POST http://localhost:5678/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{"keywords": "bug"}'

# Test 5: By assignee
curl -X POST http://localhost:5678/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{"query": "ticket yang di-assign ke ahmad"}'
```

---

## 💡 Tips

1. **Natural language** → Lebih flexible, bisa pakai bahasa sehari-hari
2. **Structured params** → Lebih cepat, skip AI processing
3. Kalau kirim structured params, AI akan di-skip otomatis
4. Bisa mix: kirim structured + tambahan query natural language
5. Response selalu include indicator "Diparsing dengan AI" kalau pakai AI

---

## 🐛 Troubleshooting

**Problem: Mistral node ada tanda tanya (?)**
- **Solusi**: Set credential Mistral API di node "Mistral AI"

**Problem: Webhook tidak muncul URL**
- **Solusi**: Aktifkan workflow dengan toggle di kanan atas

**Problem: Error "filter is not defined"**
- **Solusi**: Pastikan semua connections ter-connect dengan benar

**Problem: AI parsing tidak akurat**
- **Solusi**: Gunakan structured params untuk hasil yang lebih akurat
