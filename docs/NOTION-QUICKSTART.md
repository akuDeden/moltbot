# 🎯 Quick Start - Notion Review Tiket

Setup cepat untuk mulai review tiket ke Notion via WhatsApp.

## ⚡ Setup dalam 5 Menit

### 1. Buat Notion Integration (2 menit)
1. Buka: https://www.notion.so/my-integrations
2. Klik **"+ New integration"**
3. Copy **token** yang muncul (mulai dengan `secret_`)

### 2. Get Database ID (1 menit)
1. Buka Notion database tickets kamu
2. Copy URL, ambil ID dari sini:
   ```
   https://notion.so/workspace/a8aec43384f447ed84390e8e42c2e089?v=...
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                              Ini database ID
   ```

### 3. Share Database (30 detik)
1. Di database, klik **Share**
2. Invite integration yang tadi dibuat

### 4. Setup Credentials (1 menit)
Edit file: `/Users/ahmadfaris/moltbot-workspace/notion-credentials.json`

```json
{
  "notion_token": "secret_abc123...",
  "database_id": "a8aec43384f447ed84390e8e42c2e089"
}
```

### 5. Test! (30 detik)
```bash
cd /Users/ahmadfaris/moltbot-workspace
python3 scripts/review-ticket-notion.py "TEST-001" "UAT" "Testing"
```

## 📱 Pakai via WhatsApp

```
review tiket Tech-n-1_files_cleaner-2880 isi UAT semua test case passed
```

Bot akan:
1. Cari tiket di Notion
2. Update field UAT
3. Reply: "✅ Review berhasil ditulis ke Notion!"

## ✅ Done!

Full docs: [NOTION-SETUP.md](NOTION-SETUP.md)

---

**Pertanyaan?** Tanya aja di WhatsApp! 😊
