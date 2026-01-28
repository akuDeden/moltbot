# 📚 Dokumentasi - WhatsApp Bot

Dokumentasi lengkap untuk sistem belanja tracker & Notion integration.

## 📄 File-File Dokumentasi:

### 🦞 Moltbot Setup

### [INSTALL-MOLTBOT.md](INSTALL-MOLTBOT.md)
**Panduan install Moltbot dari awal**
- Prerequisites & dependencies
- Step-by-step installation
- WhatsApp pairing
- Configuration
- Troubleshooting

### 🛒 Belanja Tracker (Google Sheets)

### [README-SOLUTION.md](README-SOLUTION.md)
**Dokumentasi lengkap sistem auto-save belanja**
- Cara kerja sistem
- Status service auto-sync
- Command WhatsApp yang bisa dipakai
- Troubleshooting lengkap

### [TEST-NOW.md](TEST-NOW.md)
**Quick test instructions**
- Step-by-step test flow
- Expected results
- Manual sync commands

### [QUICK-TEST.md](QUICK-TEST.md)
**Quick reference & testing**
- Command list
- Troubleshooting quick fix
- Status checks

### [TEST-INSTRUCTIONS.md](TEST-INSTRUCTIONS.md)
**Instruksi test setelah fix**
- Test scenarios
- Success criteria
- Alternative approaches

### [SETUP-WEBHOOK.md](SETUP-WEBHOOK.md)
**Setup guide untuk webhook Moltbot**
- Konfigurasi webhook
- Setup steps
- File-file penting

### 📝 Notion Integration (Ticket Review)

### [NOTION-QUICKSTART.md](NOTION-QUICKSTART.md) ⭐
**Setup cepat dalam 5 menit**
- Step-by-step super singkat
- Quick test
- Ready to use!

### [NOTION-SETUP.md](NOTION-SETUP.md)
**Guide lengkap Notion integration**
- Setup Notion API & integration
- Database configuration
- Script customization
- Troubleshooting detail

---

## 🚀 Quick Start

### Belanja Tracker:
```bash
# Kirim di WhatsApp
simpan belanja teh 2 5000

# Manual sync (instant)
cd /Users/ahmadfaris/moltbot-workspace
python3 scripts/auto-sync-memory-to-sheet.py

# Check service
launchctl list | grep belanja
```

**Google Sheet:**
https://docs.google.com/spreadsheets/d/1Ibt6u5_SK4Sck9uCdLTlvkk4OYPyrjaHo92Zr33pQMc/edit

### Notion Review:
```bash
# Kirim di WhatsApp
review tiket TECH-123 isi UAT all test cases passed

# Manual test
python3 scripts/review-ticket-notion.py "TECH-123" "UAT" "Test content"
```

---

**✅ Kedua sistem sudah jalan!** 
- **Belanja** → Google Sheets
- **Review Tiket** → Notion

Baca dokumentasi di atas untuk setup detail & troubleshooting.
