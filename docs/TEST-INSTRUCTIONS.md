# 🧪 Test Bot After Fix

## ✅ Yang Sudah Dilakukan:
1. Update `CONTEXT.md` dengan instruksi lebih explicit
2. Buat `SYSTEM-BOT.md` dengan system-level instructions
3. Update `AGENTS.md` untuk baca CONTEXT.md & SYSTEM-BOT.md di setiap session
4. Restart moltbot gateway

## 📱 Test Sekarang:

### Test 1: Simpan Belanja Baru
Kirim di WhatsApp:
```
simpan belanja beras 5 75000
```

**Expected:**
- Bot akan execute: `python3 add-belanja.py "beras" 5 75000`
- Bot reply: "✅ Berhasil tambah: beras x5 @ Rp75.000 = Rp375.000"
- Data masuk ke Google Sheet

### Test 2: Cek Google Sheet
Buka sheet dan lihat apakah ada data baru:
https://docs.google.com/spreadsheets/d/1Ibt6u5_SK4Sck9uCdLTlvkk4OYPyrjaHo92Zr33pQMc/edit

**Expected:**
- Ada row baru dengan data yang kamu kirim
- Formula kolom E (Total) hitung otomatis

### Test 3: Multiple Items
Kirim di WhatsApp:
```
simpan belanja gula 1 15000
catat belanja minyak 2 30000
```

**Expected:**
- Bot execute 2 script calls
- Bot reply summary dari kedua item

---

## ❌ Jika Masih Gagal:

### Cek 1: Apakah bot baca CONTEXT.md?
Di WhatsApp, tanya:
```
apa instruksi kamu untuk simpan belanja?
```

Bot harus reply dengan menyebutkan bahwa dia harus execute Python script.

### Cek 2: Lihat log gateway
```bash
cd ~/moltbot && pnpm moltbot gateway
```

Lihat apakah ada error saat bot terima command.

### Cek 3: Test manual script
```bash
cd /Users/ahmadfaris/moltbot-workspace
python3 add-belanja.py "TestManual" 1 9999
```

Cek apakah data masuk ke Google Sheet.

---

## 🎯 Success Criteria:

✅ Bot execute `python3 add-belanja.py` saat terima "simpan belanja"  
✅ Bot reply dengan output dari script (bukan dari memory)  
✅ Data muncul di Google Sheet  
✅ Formula di kolom Total bekerja  

---

## 🔧 Alternative: Hook Script

Jika bot masih tidak execute script, kita bisa buat webhook yang otomatis trigger Python script saat terima message tertentu. Tapi coba test dulu approach ini.

**Good luck! Test sekarang dan kasih tau hasilnya!** 🚀
