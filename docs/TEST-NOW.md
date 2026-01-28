# 🧪 Test Sekarang - WhatsApp ke Google Sheet

## ✅ Sistem Sudah Jalan!

Service auto-sync **RUNNING** (PID: check dengan `launchctl list | grep belanja`)

## 📱 Test Step-by-Step:

### 1️⃣ Kirim Pesan di WhatsApp:
```
simpan belanja teh 2 5000
```

### 2️⃣ Bot akan reply (simpan ke memory)
Cek file: `/Users/ahmadfaris/moltbot-workspace/memory/2026-01-28.md`
Pastikan ada line baru:
```
- Teh 2: Rp 10.000
```

### 3️⃣ Tunggu Max 2 Menit
Service auto-sync jalan setiap 2 menit

ATAU manual sync instant:
```bash
cd /Users/ahmadfaris/moltbot-workspace
python3 auto-sync-memory-to-sheet.py
```

### 4️⃣ Cek Google Sheet
https://docs.google.com/spreadsheets/d/1Ibt6u5_SK4Sck9uCdLTlvkk4OYPyrjaHo92Zr33pQMc/edit

Harusnya ada row baru:
```
2026-01-28 HH:MM | Teh | 2 | 5000 | 10000
```

## 🎯 Expected Result:

✅ Bot reply di WhatsApp  
✅ Data di memory file updated  
✅ Dalam 2 menit → data muncul di Google Sheet  

## 🚀 Untuk Sync Instant:

Jika ingin langsung tanpa tunggu:

```bash
python3 /Users/ahmadfaris/moltbot-workspace/auto-sync-memory-to-sheet.py
```

Akan muncul:
```
📖 Reading from: /Users/ahmadfaris/moltbot-workspace/memory/2026-01-28.md
📝 Found X items
✅ Added: Teh x2 @ Rp5,000 = Rp10,000

📊 Summary: 1 added, X skipped
```

## 💡 Tips:

- Kirim pesan WhatsApp biasa, bot akan handle
- Data akan sync otomatis setiap 2 menit
- Bisa manual sync kapan saja
- Service auto-restart kalau Mac reboot

## ✅ Success!

Sistem sudah lengkap! Tinggal pakai! 🎉
