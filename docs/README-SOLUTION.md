# ✅ SOLUSI FINAL - Auto-Save Belanja ke Google Sheet

## 🎉 Status: BERHASIL!

Sistem auto-save belanja sudah **JALAN**! Data dari WhatsApp otomatis masuk ke Google Sheet.

## 📊 Cara Kerja:

1. **Kirim belanja di WhatsApp:**
   ```
   simpan belanja gula 1 15000
   ```

2. **Bot menyimpan ke memory file:**
   - File: `/Users/ahmadfaris/moltbot-workspace/memory/2026-01-28.md`
   - Bot update file ini secara realtime

3. **Auto-sync service (setiap 2 menit):**
   - Baca memory file
   - Parse item-item belanja
   - Sync ke Google Sheet (skip yang sudah ada)
   - ✅ Data masuk Google Sheet!

## 🔄 Service Auto-Sync

**Status:** ✅ RUNNING  
**Interval:** Setiap **1 jam** (3600 detik)  
**Service:** `com.ahmadfaris.belanja-sync`

### Change Sync Interval:

Edit file plist dan ubah `StartInterval` (dalam detik):

```bash
# Edit file
nano ~/Library/LaunchAgents/com.ahmadfaris.belanja-sync.plist
```

**Common intervals:**
- 1 menit: `60`
- 5 menit: `300`
- 15 menit: `900`
- 30 menit: `1800`
- 1 jam: `3600` ← **Current**
- 2 jam: `7200`
- 6 jam: `21600`

**Setelah edit, restart service:**
```bash
launchctl unload ~/Library/LaunchAgents/com.ahmadfaris.belanja-sync.plist
launchctl load ~/Library/LaunchAgents/com.ahmadfaris.belanja-sync.plist
```

### Check Status:
```bash
launchctl list | grep belanja
```

### View Logs:
```bash
tail -f /Users/ahmadfaris/moltbot-workspace/cron-sync.log
```

### Manual Trigger (instant sync):
```bash
bash /Users/ahmadfaris/moltbot-workspace/scripts/cron-sync.sh
```

### Restart Service:
```bash
launchctl unload ~/Library/LaunchAgents/com.ahmadfaris.belanja-sync.plist
launchctl load ~/Library/LaunchAgents/com.ahmadfaris.belanja-sync.plist
```

### Stop Service:
```bash
launchctl unload ~/Library/LaunchAgents/com.ahmadfaris.belanja-sync.plist
```

## 🧪 Test Flow:

**1. Kirim di WhatsApp:**
```
simpan belanja mie 5 3000
```

**2. Bot Reply:**
```
Sudah disimpan!

*Total belanja hari ini: Rp XXX*

Item yang dicatat:
- Tempe 2 kg: Rp 2.000
- ...
- Mie 5: Rp 15.000

Ada yang mau ditambah lagi?
```

**3. Tunggu Max 2 Menit**

**4. Cek Google Sheet:**
https://docs.google.com/spreadsheets/d/1Ibt6u5_SK4Sck9uCdLTlvkk4OYPyrjaHo92Zr33pQMc/edit

Data akan muncul ✅

## 🚀 Manual Sync (Instant):

Jika ingin langsung sync tanpa tunggu 2 menit:

```bash
cd /Users/ahmadfaris/moltbot-workspace
python3 auto-sync-memory-to-sheet.py
```

Output:
```
📖 Reading from: /Users/ahmadfaris/moltbot-workspace/memory/2026-01-28.md
📝 Found X items
⏭️  Skip (already exists): ...
✅ Added: mie x5 @ Rp3,000 = Rp15,000

📊 Summary: 1 added, X skipped
```

## 📱 Command WhatsApp:

### Simpan Belanja:
```
simpan belanja [nama] [jumlah] [harga]
catat belanja [nama] [jumlah] [harga]
tambah belanja [nama] [jumlah] [harga]
ia simpan [nama] [jumlah] [harga]
```

**Contoh:**
- `simpan belanja telur 10 2500`
- `catat belanja ayam 2 45000`
- `ia simpan beras 5 75000`

### Lihat Total:
```
total belanja
berapa total
cek belanja
```

## 🛠️ Troubleshooting:

### Data belum muncul di sheet?
1. Cek apakah service jalan: `launchctl list | grep belanja`
2. Lihat log: `tail -20 ~/moltbot-workspace/sync-stdout.log`
3. Manual sync: `python3 auto-sync-memory-to-sheet.py`

### Service tidak jalan?
```bash
# Load service
launchctl load ~/Library/LaunchAgents/com.ahmadfaris.belanja-sync.plist

# Check
launchctl list | grep belanja
```

### Bot tidak respond?
```bash
# Check moltbot gateway
cd ~/moltbot && pnpm moltbot gateway status

# Restart
cd ~/moltbot && pnpm moltbot gateway restart
```

## 📁 File-File Penting:

- `add-belanja.py` - Manual add item ke sheet (bisa jalan langsung)
- `auto-sync-memory-to-sheet.py` - Sync dari memory ke sheet
- `watch-and-sync.sh` - Watcher service (jalan otomatis)
- `memory/2026-01-28.md` - Memory log hari ini
- `CONTEXT.md` - Instruksi untuk bot
- `google-credentials.json` - Service account credentials

## ✨ Kesimpulan:

Sistem **SUDAH JALAN**! 

Workflow:
1. ✅ Kirim "simpan belanja" di WhatsApp
2. ✅ Bot simpan ke memory file
3. ✅ Auto-sync (max 2 menit) sync ke Google Sheet
4. ✅ Data muncul di sheet

**Tidak perlu action manual lagi!** Tinggal kirim pesan WhatsApp, tunggu max 2 menit, data masuk! 🎉

---

**Untuk sync instant:** Jalankan `python3 auto-sync-memory-to-sheet.py`
