# Setup Webhook - Auto Save Belanja ke Google Sheet

## ✅ STATUS: MOLTBOT SUDAH RUNNING!

Moltbot sudah terinstall dan berjalan. WhatsApp gateway sudah connected ✅

**Lokasi install:** `~/moltbot` (dari source GitHub)
**Config:** `~/.clawdbot/moltbot.json`
**Command:** `cd ~/moltbot && pnpm moltbot <command>`

## 🎯 Tujuan
Otomatis menjalankan `add-belanja.py` setiap kali terima pesan belanja dari WhatsApp, tanpa perlu manual execute.

## 📋 Cara Kerja
1. User kirim: "simpan belanja ayam 2 45000"
2. Clawdbot parse pesan → extract nama, jumlah, harga
3. Clawdbot execute: `python3 add-belanja.py "ayam" 2 45000`
4. Data langsung masuk Google Sheet ✅

## ⚙️ Setup Status

### ✅ Sudah Ada:
1. Moltbot terinstall dan running dari `~/moltbot`
2. WhatsApp gateway connected
3. Bot bisa terima & reply pesan WhatsApp
4. Script `add-belanja.py` siap pakai
5. Google credentials valid

### ⏳ Yang Perlu Dilakukan:
Bot sekarang simpan ke memory file, perlu configure agar **execute script Python** untuk save ke Google Sheet.

Lihat [CONTEXT.md](CONTEXT.md) untuk instruksi bot.

---

## ⚙️ Setup (Sudah Selesai)

### 1. Enable Webhook di Moltbot Config

Edit file: `~/.clawdbot/moltbot.json`

Tambahkan:
```json
{
  "hooks": {
    "enabled": true,
    "token": "your-secret-token-here",
    "path": "/hooks"
  }
}
```

**Generate token yang aman:**
```bash
openssl rand -hex 32
```

### 2. Restart Gateway
```bash
moltbot gateway restart
```

### 3. Test Webhook
```bash
curl -X POST http://127.0.0.1:18789/hooks/agent \
  -H 'Authorization: Bearer your-secret-token-here' \
  -H 'Content-Type: application/json' \
  -d '{"message":"Test webhook", "name":"Test"}'
```

## 🤖 Cara Clawdbot Sudah Bekerja

Berdasarkan [CONTEXT.md](CONTEXT.md), bot sudah di-setup untuk:

**Trigger words:**
- "simpan belanja"
- "catat belanja" 
- "tambah belanja"
- "ia simpan"

**Format:**
```
simpan belanja [nama] [jumlah] [harga]
```

**Contoh:**
```
simpan belanja tempe 2 1000
simpan belanja ayam 2 45000
```

Bot akan otomatis:
1. Parse nama, jumlah, harga dari pesan
2. Execute: `python3 /Users/ahmadfaris/moltbot-workspace/add-belanja.py "nama" jumlah harga`
3. Reply dengan konfirmasi

## ✅ Verifikasi

Cek apakah data masuk ke Google Sheet:
```bash
# Lihat data terakhir yang masuk
python3 sync-google-auth.py
tail -5 data.csv
```

Atau buka langsung:
https://docs.google.com/spreadsheets/d/1Ibt6u5_SK4Sck9uCdLTlvkk4OYPyrjaHo92Zr33pQMc

## 🔍 Troubleshooting

### Bot tidak execute command?
- Pastikan trigger word match (simpan/catat/tambah belanja)
- Cek format: nama jumlah harga (3 parameter)

### Script error?
```bash
# Test manual
python3 add-belanja.py "Test" 1 1000

# Cek credentials
ls -la google-credentials.json
```

### Data tidak masuk sheet?
- Pastikan google-credentials.json ada & valid
- Cek permission: service account harus punya akses ke sheet
- Share sheet dengan email service account: `SERVICE_ACCOUNT_EMAIL@PROJECT_ID.iam.gserviceaccount.com`

## 📊 Lihat Total Belanja

**Trigger:** "total belanja", "berapa total", "cek belanja"

Bot akan:
1. Download data dari sheet
2. Hitung total kolom "Total"
3. Reply dengan summary

## 🔐 Security

- Hook token harus rahasia!
- Webhook endpoint hanya listen di loopback (127.0.0.1)
- Service account credentials tetap di local machine
- Tidak ada data sensitif dikirim ke luar

## 📝 Files Penting

- `add-belanja.py` - Script untuk tambah data ke sheet
- `sync-google-auth.py` - Download data dari sheet (pakai service account)
- `google-credentials.json` - Service account credentials (JANGAN SHARE!)
- `CONTEXT.md` - Instruksi untuk bot tentang command belanja
- `~/.clawdbot/moltbot.json` - Config moltbot

## 🎮 Command Lengkap

```bash
# Test tambah data manual
python3 add-belanja.py "Telur" 10 2500

# Sync & lihat data
python3 sync-google-auth.py
cat data.csv

# Check bot status
moltbot gateway status

# Restart bot
moltbot gateway restart
```

---

**✨ Tips:** Setelah setup, cukup kirim pesan di WhatsApp dengan format "simpan belanja [nama] [jumlah] [harga]" dan data langsung masuk otomatis!
