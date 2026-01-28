# 📝 Setup Notion Integration

Guide lengkap untuk setup integrasi Notion dengan bot.

## 🎯 Fitur

Bot bisa:
- Review tiket dari WhatsApp command
- Tulis hasil review ke Notion database
- Update status dan notes di Notion

## 📋 Prerequisites

### 1. Buat Notion Integration

1. Buka: https://www.notion.so/my-integrations
2. Klik **"+ New integration"**
3. Isi nama integration (misal: "WhatsApp Bot")
4. Select workspace yang ingin dipakai
5. Klik **Submit**
6. **Copy API token** yang muncul (rahasia!)

### 2. Setup Notion Database

Database harus punya properties berikut (sesuaikan nama):
- **Ticket ID** atau **Name** (Title) - untuk search tiket
- **UAT Status** (Status) - untuk UAT review
- **UAT Notes** (Rich Text) - untuk catatan UAT
- **Review** (Rich Text) - untuk review general
- **Last Updated** (Date) - timestamp auto-update

### 3. Share Database dengan Integration

1. Buka Notion database yang mau dipakai
2. Klik **Share** di kanan atas
3. **Invite** integration yang tadi dibuat
4. Klik **Invite** untuk confirm

### 4. Dapat Database ID

Database ID ada di URL Notion:
```
https://notion.so/workspace/[DATABASE_ID]?v=...
                          ^^^^^^^^^^^^^^^^
                          Copy bagian ini
```

Atau dari database URL yang full:
```
https://www.notion.so/myworkspace/a8aec43384f447ed84390e8e42c2e089?v=...
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                  Ini database ID
```

## ⚙️ Configuration

### 1. Edit Credentials File

Edit file: `/Users/ahmadfaris/moltbot-workspace/notion-credentials.json`

```json
{
  "notion_token": "secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "database_id": "a8aec43384f447ed84390e8e42c2e089"
}
```

**⚠️ PENTING:** File ini rahasia! Jangan commit ke git!

### 2. Install Notion SDK

```bash
pip install notion-client
```

### 3. Test Script

```bash
cd /Users/ahmadfaris/moltbot-workspace
python3 scripts/review-ticket-notion.py "TECH-123" "UAT" "Test passed"
```

Expected output:
```
🔍 Searching for ticket: TECH-123
✅ Found ticket page
📝 Updating review: UAT
✅ Review berhasil ditulis ke Notion!
   Ticket: TECH-123
   Type: UAT
   Content: Test passed...
```

## 📱 WhatsApp Commands

### Review Tiket

**Format:**
```
review tiket [TICKET_ID] isi [REVIEW_TYPE] [CONTENT]
```

**Contoh:**
```
review tiket Tech-n-1_files_cleaner-2880 isi UAT all test cases passed
review tiket TECH-123 isi QA needs improvement on error handling
```

**Bot akan:**
1. Parse ticket ID, review type, dan content
2. Cari tiket di Notion database
3. Update field yang sesuai
4. Reply konfirmasi

## 🔧 Customize Script

Edit `/Users/ahmadfaris/moltbot-workspace/scripts/review-ticket-notion.py`:

### Sesuaikan Property Names

Di function `find_ticket_page()`:
```python
"property": "Ticket ID",  # ← Ganti sesuai nama property di database Anda
```

Di function `update_notion_page()`:
```python
properties["UAT Status"] = {  # ← Ganti nama property
    "status": {
        "name": "In Progress"  # ← Ganti status value
    }
}
```

### Tambah Review Types

Tambah condition baru:
```python
elif review_type.upper() == "QA":
    properties["QA Status"] = {
        "status": {
            "name": "Reviewed"
        }
    }
    properties["QA Notes"] = {
        "rich_text": [{"text": {"content": review_content}}]
    }
```

## 🚀 Integration dengan Bot

Bot sudah di-configure untuk handle command `review tiket`. 

Lihat [CONTEXT.md](/Users/ahmadfaris/moltbot-workspace/CONTEXT.md) untuk detail command.

## 🔍 Troubleshooting

### "Ticket not found"
- Pastikan ticket ID match dengan property di Notion
- Cek apakah database sudah di-share dengan integration
- Coba search dengan format ticket ID yang berbeda

### "notion-client not installed"
```bash
pip install notion-client
```

### "Notion token not configured"
- Edit `notion-credentials.json`
- Pastikan token dimulai dengan `secret_`

### "Error updating page"
- Cek property names di script match dengan database
- Pastikan property type sesuai (Status, Rich Text, Date)
- Lihat error detail untuk property yang salah

## 📖 Notion API Docs

- [Getting Started](https://developers.notion.com/docs/getting-started)
- [Working with Databases](https://developers.notion.com/docs/working-with-databases)
- [Property Values](https://developers.notion.com/reference/property-value-object)

## 🎮 Test Flow Complete

1. **Buat test ticket di Notion**
2. **Setup credentials** (token + database ID)
3. **Test script manual:**
   ```bash
   python3 scripts/review-ticket-notion.py "TEST-001" "UAT" "Testing integration"
   ```
4. **Test via WhatsApp:**
   ```
   review tiket TEST-001 isi UAT all good
   ```
5. **Check Notion** - lihat apakah page updated

## ✅ Success Checklist

- [ ] Notion integration created
- [ ] API token copied
- [ ] Database shared dengan integration
- [ ] Database ID copied
- [ ] `notion-credentials.json` filled
- [ ] `notion-client` installed
- [ ] Script test berhasil
- [ ] WhatsApp command works

---

**🎉 Setelah setup, tinggal kirim command di WhatsApp dan hasil review langsung masuk Notion!**
