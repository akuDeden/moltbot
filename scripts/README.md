# 📁 Scripts Directory

Organized script collection for workspace automation.

## 📂 Directory Structure

```
scripts/
├── attendance/     # Auto attendance system
├── tickets/        # Ticket & project management
├── sync/          # Memory & data synchronization
├── notes/         # Notes & shopping list
└── docs/          # Documentation & requirements
```

---

## 🎯 Quick Access

### 📋 Attendance (Auto Absensi)
**Location:** `attendance/`

| Script | Purpose |
|--------|---------|
| `auto-absen.sh` | Main attendance script (clock in/out) |
| `quick-status.sh` | Quick status check (for AI) |
| `check-absen-status.sh` | Detailed status with duration |
| `dry-run-absen.sh` | Test without executing |
| `setup-absen-cron.sh` | Install cron jobs |

**Quick Commands:**
```bash
# Manual attendance
./attendance/auto-absen.sh in
./attendance/auto-absen.sh out

# Check status
./attendance/quick-status.sh

# Setup autopilot
./attendance/setup-absen-cron.sh
```

---

### 🎫 Tickets
**Location:** `tickets/`

| Script | Purpose |
|--------|---------|
| `create-bug-ticket.py` | Create bug ticket |
| `find-elasticsearch-ticket.py` | Search tickets |
| `get-sprint-tickets-status.py` | Sprint status |
| `get-tickets-sprint.py` | Get sprint tickets |
| `query-sprint-tickets.sh` | Query sprint |
| `query-tickets.py` | General ticket query |
| `update-ticket-*.py` | Update ticket properties |

**Quick Commands:**
```bash
# Query tickets
python tickets/query-tickets.py

# Create bug
python tickets/create-bug-ticket.py

# Update status
python tickets/update-ticket-status.py
```

---

### 🔄 Sync
**Location:** `sync/`

| Script | Purpose |
|--------|---------|
| `auto-sync-memory-to-sheet.py` | Sync memory to Google Sheets |
| `cron-sync.sh` | Cron job for sync |
| `instant-watch.sh` | Watch & sync instantly |
| `sync-google-auth.py` | Google auth setup |
| `sync-sheets.sh` | Manual sheet sync |
| `watch-and-sync.sh` | Watch for changes |

**Quick Commands:**
```bash
# Setup Google auth
python sync/sync-google-auth.py

# Manual sync
./sync/sync-sheets.sh

# Watch mode
./sync/watch-and-sync.sh
```

---

### 📝 Notes
**Location:** `notes/`

| Script | Purpose |
|--------|---------|
| `add-belanja.py` | Add shopping item |
| `add-note.py` | Add general note |

**Quick Commands:**
```bash
# Add shopping item
python notes/add-belanja.py "Beli susu"

# Add note
python notes/add-note.py "Meeting notes..."
```

---

### 📚 Docs
**Location:** `docs/`

| File | Description |
|------|-------------|
| `README.md` | General scripts documentation |
| `TEST-REPORT.md` | Attendance system test report |
| `TRACKING-UPDATE.md` | Tracking feature documentation |
| `requirements.txt` | Python dependencies |

---

## 🚀 Getting Started

### Python Scripts
```bash
# Install dependencies
pip install -r docs/requirements.txt

# Or with venv
python -m venv venv
source venv/bin/activate
pip install -r docs/requirements.txt
```

### Shell Scripts
All shell scripts are already executable. Just run them directly:
```bash
./attendance/auto-absen.sh
./sync/sync-sheets.sh
```

---

## 🔐 Security Notes

- **Attendance scripts** contain login credentials - keep secure!
- **Google credentials** are in `../google-credentials.json`
- **API keys** should be in environment variables
- Never commit sensitive data to git

---

## 📖 Related Documentation

- **Workspace Setup:** `../BOOTSTRAP.md`
- **Persona Configs:** `../persona/`
- **Agent Instructions:** `../AGENTS.md`
- **System Instructions:** `../SYSTEM-BOT.md`

---

**Last Updated:** January 29, 2026  
**Organization:** Categorized by function
