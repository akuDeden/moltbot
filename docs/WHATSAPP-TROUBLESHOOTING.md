# WhatsApp Connection Troubleshooting

Panduan troubleshooting untuk masalah koneksi WhatsApp pada Moltbot.

## 🔍 Cek Status WhatsApp

```bash
cd /Users/ahmadfaris/moltbot
pnpm moltbot channels status
```

Status yang sehat:
```
- WhatsApp default: enabled, configured, linked, running, connected
```

## ❌ Masalah Umum

### 1. Channel Status: `stopped, disconnected, error:disabled`

**Gejala:**
```
- WhatsApp: enabled, configured, linked, stopped, disconnected, error:disabled
```

**Penyebab:**
- `web.enabled` di-set `false` di config
- Web provider (Baileys) dinonaktifkan

**Solusi:**
```bash
# Cek status web provider
pnpm moltbot config get web

# Jika hasilnya: { "enabled": false }
# Aktifkan web provider:
pnpm moltbot config set web.enabled true

# Restart gateway
pkill -f "moltbot-gateway"

# Tunggu beberapa detik, gateway akan auto-restart via launchd
# Lalu cek status lagi
pnpm moltbot channels status
```

### 2. Error 401 Unauthorized (Multi-Account)

**Gejala:**
```
- WhatsApp custom-1: enabled, configured, linked, stopped, error:{"error":{...401..."Connection Failure"}}
```

**Penyebab:**
- Credentials account expired/invalid
- Session Baileys rusak

**Solusi A: Disable Account Bermasalah**
```bash
# Jika punya multiple accounts dan salah satunya error
pnpm moltbot config set channels.whatsapp.accounts.custom-1.enabled false

# Restart gateway
pkill -f "moltbot-gateway"
```

**Solusi B: Re-login Account**
```bash
# Logout account bermasalah
pnpm moltbot channels logout --account custom-1

# Login ulang dengan scan QR
pnpm moltbot channels login --account custom-1

# Restart gateway
pkill -f "moltbot-gateway"
```

### 3. WhatsApp Tidak Linked

**Gejala:**
```
- WhatsApp: enabled, configured, not linked
```

**Solusi:**
```bash
# Logout credentials lama
pnpm moltbot channels logout

# Login dengan QR code baru
pnpm moltbot channels login

# Scan QR code di WhatsApp → Settings → Linked Devices

# Restart gateway
pkill -f "moltbot-gateway"
```

### 4. Gateway Tidak Berjalan

**Cek proses gateway:**
```bash
pgrep -fl moltbot
```

**Jika tidak ada output:**
```bash
# Buka Moltbot Mac app untuk start gateway
# Atau cek launchd:
launchctl print gui/$UID | grep -i moltbot
```

### 5. Action `sendMessage` Disabled

**Gejala:**
Bot tidak bisa kirim pesan meskipun sudah connected.

**Cek:**
```bash
pnpm moltbot config get channels.whatsapp.actions
```

**Jika hasilnya:**
```json
{ "sendMessage": false }
```

**Solusi:**
```bash
pnpm moltbot config set channels.whatsapp.actions.sendMessage true
pkill -f "moltbot-gateway"
```

## 📋 Checklist Debugging

Ikuti langkah ini secara berurutan:

1. ✅ **Gateway running?**
   ```bash
   pgrep -fl moltbot
   ```

2. ✅ **Web provider enabled?**
   ```bash
   pnpm moltbot config get web
   # Harus: { "enabled": true }
   ```

3. ✅ **WhatsApp linked?**
   ```bash
   pnpm moltbot doctor
   # Cek bagian: "WhatsApp: linked"
   ```

4. ✅ **Channel status OK?**
   ```bash
   pnpm moltbot channels status
   # Harus: "running, connected"
   ```

5. ✅ **Config allowlist benar?**
   ```bash
   pnpm moltbot config get channels.whatsapp.allowFrom
   # Pastikan nomor Anda ada di list
   ```

## 🔧 Config Reference

**Minimal working config** (`~/.clawdbot/moltbot.json`):

```json
{
  "web": {
    "enabled": true
  },
  "channels": {
    "whatsapp": {
      "dmPolicy": "pairing",
      "allowFrom": [
        "+6287826577336",
        "+6285778222524"
      ]
    }
  }
}
```

**Multi-account config:**

```json
{
  "web": {
    "enabled": true
  },
  "channels": {
    "whatsapp": {
      "accounts": {
        "default": {
          "enabled": true,
          "dmPolicy": "pairing"
        },
        "custom-1": {
          "enabled": false
        }
      },
      "allowFrom": ["+6287826577336"]
    }
  }
}
```

## 📝 Logs

**Lokasi log:**
```bash
/tmp/moltbot/moltbot-2026-01-29.log
```

**Lihat log WhatsApp:**
```bash
tail -f /tmp/moltbot/moltbot-*.log | grep -i whatsapp
```

**Lihat log gateway:**
```bash
tail -f /tmp/moltbot/moltbot-*.log
```

## 🆘 Doctor Command

```bash
pnpm moltbot doctor
```

Output akan menunjukkan:
- WhatsApp linked status
- Web channel info
- Agent config
- Session store

## 📚 Dokumentasi Resmi

Untuk informasi lebih lengkap:
- https://docs.molt.bot/channels/whatsapp
- https://docs.molt.bot/gateway/troubleshooting

## ⚠️ Catatan Penting

1. **Jangan gunakan Bun** untuk menjalankan gateway - gunakan Node.js
2. **Gateway harus running** sebelum kirim/terima pesan WhatsApp
3. **Restart gateway** setelah perubahan config penting (`web.enabled`, accounts, dll)
4. **Credentials location:** `~/.clawdbot/credentials/whatsapp/<accountId>/creds.json`
5. **Backup credentials** sebelum re-login atau testing
