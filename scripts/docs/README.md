# 🛠️ Scripts - Belanja Tracker Utilities

Folder ini berisi semua script utilities untuk sistem belanja tracker.

## 📜 Scripts:

### **add-belanja.py**
Script utama untuk menambah item belanja ke Google Sheet.

**Usage:**
```bash
python3 scripts/notes/add-belanja.py "Nama Item" Jumlah Harga
```

**Example:**
```bash
python3 scripts/notes/add-belanja.py "Telur" 10 2500
# Output: ✅ Berhasil tambah: Telur x10 @ Rp2.500 = Rp25.000
```

---

### **auto-sync-memory-to-sheet.py**
Auto-sync items dari memory file ke Google Sheet (skip duplicates).

**Usage:**
```bash
python3 scripts/auto-sync-memory-to-sheet.py [memory_file]
```

**Example:**
```bash
python3 scripts/auto-sync-memory-to-sheet.py
# Auto-detect today's memory file
```

---

### **sync-google-auth.py**
Download data dari Google Sheet ke local CSV file.

**Usage:**
```bash
python3 scripts/sync/sync-google-auth.py
```

**Output:** `/Users/ahmadfaris/moltbot-workspace/data.csv`

---

### **sync-sheets.sh**
Download Google Sheet sebagai CSV via URL (public access needed).

**Usage:**
```bash
bash scripts/sync/sync-sheets.sh
```

---

### **watch-and-sync.sh**
Background watcher script yang auto-sync setiap 2 menit.

**Usage:**
```bash
# Run manually (foreground)
bash scripts/sync/watch-and-sync.sh

# Run as service (via launchd)
launchctl load ~/Library/LaunchAgents/com.ahmadfaris.belanja-sync.plist
```

---

## 🔄 Dependencies:

```bash
pip install gspread oauth2client
```

## 📁 Files Needed:

- `google-credentials.json` - Service account credentials (di root clawd/)
- `memory/YYYY-MM-DD.md` - Memory file untuk auto-sync

## 🚀 Quick Commands:

```bash
# Manual add item
python3 scripts/notes/add-belanja.py "Kopi" 1 15000

# Manual sync from memory
python3 scripts/auto-sync-memory-to-sheet.py

# Download sheet data
python3 scripts/sync/sync-google-auth.py

# Check auto-sync service
launchctl list | grep belanja
tail -f /Users/ahmadfaris/moltbot-workspace/sync-stdout.log
```

---

**✅ All scripts ready to use!**
