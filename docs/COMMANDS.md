# 📋 Bot Commands - Quick Reference

Semua command yang bisa dipakai via WhatsApp.

## 🛒 Belanja Tracker → Google Sheets

### Simpan Belanja
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

**Hasil:**
- Data langsung masuk Google Sheets
- Bot reply konfirmasi

### Lihat Total
```
total belanja
berapa total
cek belanja
```

**Hasil:**
Bot akan kasih summary total belanja.

---

## 📝 Notion Integration → Review Tiket

### Review Tiket
```
review tiket [TICKET_ID] isi [REVIEW_TYPE] [CONTENT]
```

**Contoh:**
- `review tiket Tech-n-1_files_cleaner-2880 isi UAT all test cases passed successfully`
- `review tiket TECH-123 isi QA needs improvement on error handling`
- `review tiket PROJ-456 isi UAT testing completed, ready for prod`

**Review Types:**
- `UAT` - User Acceptance Testing
- `QA` - Quality Assurance
- `Review` - General review
- Atau custom type sesuai database Notion kamu

**Hasil:**
- Bot cari tiket di Notion database
- Update field yang sesuai (UAT Status, UAT Notes, dll)
- Bot reply konfirmasi: "✅ Review berhasil ditulis ke Notion!"

---

## 🔧 Setup Required

### Belanja Tracker
✅ Sudah ready! Langsung pakai.

### Notion Review
📝 Perlu setup dulu (5 menit):
1. Buat Notion integration & get token
2. Get database ID
3. Share database dengan integration
4. Edit `notion-credentials.json`

**Guide lengkap:** [docs/NOTION-QUICKSTART.md](NOTION-QUICKSTART.md)

---

## 📱 Tips Pakai Bot

### Format Fleksibel
Bot bisa parse berbagai format:
- `simpan belanja gula 1 15000` ✅
- `catat gula 1 kg harganya 15rb` ✅
- `ia simpan gula 15000` (tanpa qty, assume 1) ✅

### Multiple Items
Kirim sekaligus:
```
simpan belanja telur 10 2500
catat juga beras 5 75000
```
Bot akan process semua!

### Natural Language
Bot understand bahasa natural:
- "review tiket TECH-123 isi UAT semua test udah passed"
- "update notion TECH-456 dengan QA masih ada bug"

---

## 🚀 Quick Test

### Test Belanja:
```
simpan belanja test-item 1 1000
```
Check: [Google Sheet](https://docs.google.com/spreadsheets/d/1Ibt6u5_SK4Sck9uCdLTlvkk4OYPyrjaHo92Zr33pQMc/edit)

### Test Notion:
```
review tiket TEST-001 isi UAT testing bot integration
```
Check: Notion database kamu

---

**Need help?** Tanya aja di WhatsApp! Bot siap bantu 😊
