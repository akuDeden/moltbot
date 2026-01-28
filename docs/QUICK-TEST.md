# Quick Test - Moltbot Belanja Tracker

## ✅ Status Sekarang
- Moltbot: **RUNNING** ✅
- WhatsApp: **CONNECTED** ✅  
- Bot bisa terima pesan WhatsApp ✅

## 🧪 Test Simpan Belanja

### Via WhatsApp:
Kirim pesan ke nomor WhatsApp yang di-pair dengan moltbot:

```
simpan belanja telur 10 2500
```

Bot akan:
1. Parse: nama=telur, jumlah=10, harga=2500
2. Execute: `python3 add-belanja.py "telur" 10 2500`
3. Reply konfirmasi dari script

### Manual Test Script:
```bash
# Test script langsung
cd /Users/ahmadfaris/moltbot-workspace
python3 add-belanja.py "Test Item" 1 5000

# Lihat memory log bot
cat memory/2026-01-28.md
```

## 📱 Command yang Bisa Dipakai

### 1. Simpan Belanja
```
simpan belanja [nama] [jumlah] [harga]
catat belanja [nama] [jumlah] [harga]
tambah belanja [nama] [jumlah] [harga]
ia simpan [nama] [jumlah] [harga]
```

**Contoh:**
- `simpan belanja tempe 2 1000`
- `catat belanja ayam 1 25000`
- `ia simpan beras 5 75000`

### 2. Lihat Total
```
total belanja
berapa total
cek belanja
```

Bot akan baca memory file dan kasih summary.

## 🔧 Troubleshooting

### Bot tidak respond?
```bash
# Cek status gateway
cd ~/moltbot && pnpm moltbot gateway status

# Restart gateway
cd ~/moltbot && pnpm moltbot gateway restart
```

### Bot tidak execute Python script?
1. Pastikan trigger word ada ("simpan belanja", dll)
2. Cek [CONTEXT.md](CONTEXT.md) untuk instruksi bot
3. Test manual script untuk pastikan Python works

### Lihat log bot:
```bash
# Run gateway in foreground untuk lihat log
cd ~/moltbot && pnpm moltbot gateway
```

## 🚀 Next Steps

Kalau test berhasil dan script execute dengan benar:
1. Data akan otomatis masuk ke Google Sheet
2. Bisa lihat di: https://docs.google.com/spreadsheets/d/1Ibt6u5_SK4Sck9uCdLTlvkk4OYPyrjaHo92Zr33pQMc

Selamat! Bot auto-save belanja sudah jalan! 🎉
