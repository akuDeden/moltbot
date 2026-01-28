# 🤖 Moltbot/Clawbot Notion Database Reader

> **Role Model Scripts** - Contoh cara query dan membaca Notion database untuk AI agent/persona

## 📁 Folder Ini

Folder ini berisi **contoh implementasi** cara membaca Notion database yang dapat digunakan sebagai **role model** untuk persona AI (moltbot/clawbot).

**Tujuan:**
- ✅ Menunjukkan cara query Notion database via API
- ✅ Contoh extract properties dan content dari tickets
- ✅ Template untuk integrasi AI agent dengan Notion
- ✅ Reference implementation untuk project lain

**Bukan bagian dari main project reviewTicket** - ini hanya reference/example code.

---

## 📦 Files dalam Folder Ini

**Core Scripts:**
- `notion_database_reader.py` - Core library untuk query Notion
- `list_all_pages.py` - List semua pages/databases
- `list_dev_tickets.py` - Query dev tickets (contoh dengan 2 DB IDs)
- `list_bug_tickets.py` - Query bug tickets
- `clawbot_ticket_reader.py` - AI agent integration example
- `test_notion_connection.py` - Test connection & setup

**Documentation:**
- `INDEX.txt` - Quick reference guide
- `README_NOTION_SCRIPTS.md` - Detailed documentation
- `NOTION_DATABASE_GUIDE.md` - Complete API reference
- `SUMMARY.md` - Implementation summary

**Setup:**
- `setup_notion_scripts.sh` - Setup helper
- `copy_to_clawd.sh` - Copy script ke target directory

---

## 🎯 Use Case

### Untuk Moltbot/Clawbot di `/Users/ahmadfaris/moltbot-workspace/scripts`

Script ini dibuat untuk digunakan di folder clawbot:

```bash
# Copy ke target directory
cd /Users/ahmadfaris/work/chronicle/ai_project/reviewticket/GIT_reviewTicket_V2/reviewTicket_web/reviewTicket/scripts/moltbot_notion_reader

# Run copy script
./copy_to_clawd.sh

# Files akan di-copy ke:
# /Users/ahmadfaris/moltbot-workspace/scripts/
```

### Database IDs yang Dikonfigurasi

**Dev Tickets:**
- Database 1: `482be0a206b044d99fff5798db2381e4`
- Database 2: `32e29af7d7dd4df69310270de8830d1a`

**Bug Tickets:**
- Set via env: `export BUG_DATABASE_ID="your_id"`

---

## 🚀 Quick Start

```bash
# 1. Set Notion token
export NOTION_TOKEN="secret_your_token_here"

# 2. Test connection
python3 test_notion_connection.py

# 3. List databases
python3 list_all_pages.py --show-databases

# 4. Query dev tickets
python3 list_dev_tickets.py

# 5. Get full content untuk AI
python3 clawbot_ticket_reader.py \
  --database-id 482be0a206b044d99fff5798db2381e4 \
  --status "Ready for Review" \
  --output tickets.json
```

---

## 📚 Documentation

- **Quick Start:** `README_NOTION_SCRIPTS.md`
- **API Reference:** `NOTION_DATABASE_GUIDE.md`
- **Quick Reference:** `INDEX.txt`
- **Summary:** `SUMMARY.md`

---

## ⚠️ Note

**Folder ini BUKAN bagian dari workflow reviewTicket utama.**

Ini adalah:
- ✅ Standalone scripts untuk reference
- ✅ Example implementation
- ✅ Template untuk project lain (moltbot/clawbot)

Jika Anda sedang menggunakan reviewTicket system, gunakan:
- `automated_ticket_review.py` (main workflow)
- `main.py` (interactive mode)

---

## 📞 Support

Untuk dokumentasi lengkap, lihat:
- `README_NOTION_SCRIPTS.md` - Getting started
- `NOTION_DATABASE_GUIDE.md` - Complete guide
- `INDEX.txt` - Quick reference

---

**Created for:** Moltbot/Clawbot AI Agent (reference implementation)  
**Version:** 1.0.0  
**Date:** January 28, 2026  
**Location:** `/scripts/moltbot_notion_reader/` (isolated from main project)
