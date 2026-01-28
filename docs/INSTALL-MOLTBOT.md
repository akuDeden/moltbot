# 🦞 Moltbot - Installation Guide

Panduan lengkap install aplikasi Moltbot dari awal.

## 📋 System Requirements

- **OS:** macOS, Linux, atau Windows (WSL2)
- **Node.js:** Version 22 atau lebih baru
- **Package Manager:** pnpm ≥ 10
- **Git:** For cloning repository
- **RAM:** Minimal 4GB
- **Storage:** ~2GB untuk dependencies

## 🚀 Installation Methods

### Method 1: Global Install via npm (Recommended for Users)

```bash
# Install globally
npm install -g moltbot@latest

# Verify installation
moltbot --version

# Run onboarding wizard
moltbot onboard --install-daemon
```

### Method 2: From Source (Recommended for Development)

```bash
# Clone repository
cd ~
git clone https://github.com/moltbot/moltbot.git
cd moltbot

# Install dependencies
pnpm install

# Build UI
pnpm ui:build

# Build project
pnpm build

# Run from source
pnpm moltbot onboard --install-daemon
```

## 📦 Step-by-Step Installation (From Source)

### 1. Install Node.js v22+

**Option A: Using nvm (recommended):**
```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Restart terminal, then:
nvm install 22
nvm use 22
nvm alias default 22
```

**Option B: Using Homebrew (macOS):**
```bash
brew install node@22
```

**Option C: Download from nodejs.org:**
- Visit: https://nodejs.org/
- Download LTS version (≥22)
- Install package

### 2. Install pnpm

```bash
npm install -g pnpm

# Verify
pnpm --version
```

### 3. Clone Moltbot

```bash
cd ~
git clone https://github.com/moltbot/moltbot.git
cd moltbot
```

### 4. Install Dependencies

```bash
pnpm install
```

This will:
- Install all Node.js packages
- Download required binaries
- Setup development environment

**Note:** First install may take 5-10 minutes.

### 5. Build the Project

```bash
# Build UI first
pnpm ui:build

# Then build main project
pnpm build
```

### 6. Run Onboarding Wizard

```bash
pnpm moltbot onboard
```

The wizard will guide you through:
- ✅ Creating workspace directory
- ✅ Configuring AI model provider
- ✅ Setting up messaging channels
- ✅ Installing daemon service (optional)

**Install as daemon (background service):**
```bash
pnpm moltbot onboard --install-daemon
```

## 🎯 Post-Installation Setup

### Create Workspace Directory

**Pilih nama folder sesuai kebutuhan** (contoh: `moltbot-workspace`, `my-bot`, dll):

```bash
# Contoh 1: Gunakan "clawd"
mkdir -p ~/moltbot-workspace
cd ~/moltbot-workspace

# Contoh 2: Gunakan nama sendiri
mkdir -p ~/my-bot-workspace
cd ~/my-bot-workspace

# Contoh 3: Gunakan nama project
mkdir -p ~/assistant-bot
cd ~/assistant-bot

# Initialize with basic files
echo "# My Moltbot Workspace" > README.md
```

**Tips:** Pilih nama yang mudah diingat dan relevan dengan project Anda.

### Configure Moltbot

Config file location: `~/.clawdbot/moltbot.json`

Example basic config:
```json
{
  "agents": {
    "defaults": {
      "workspace": "/Users/username/YOUR-WORKSPACE-NAME",
      "model": {
        "primary": "zai/glm-4.7"
      }
    }
  }
}
```

**Note:** Ganti `YOUR-WORKSPACE-NAME` dengan nama folder yang Anda buat (misalnya `clawd`, `my-bot-workspace`, dll).

## 🖥️ Running Moltbot

### Start Gateway

**Foreground (see logs):**
```bash
cd ~/moltbot
pnpm moltbot gateway
```

**Background (as service):**
```bash
# The daemon was installed during onboarding
# Gateway should start automatically

# Check status
launchctl list | grep molt

# Manual start/stop
launchctl load ~/Library/LaunchServices/bot.molt.gateway.plist
launchctl unload ~/Library/LaunchServices/bot.molt.gateway.plist
```

### Access Dashboard

Open in browser:
- Local: http://127.0.0.1:18789/
- Alternative: http://localhost:18789/

The dashboard provides:
- Chat interface
- Channel management
- Session monitoring
- Configuration UI
- Logs viewer

## 🔌 Connect Messaging Channels

### WhatsApp

```bash
pnpm moltbot channels login
```

Scan QR code with WhatsApp app.

### Telegram

1. Create bot via [@BotFather](https://t.me/botfather)
2. Get bot token
3. Add to config:

```json
{
  "channels": {
    "telegram": {
      "token": "YOUR_BOT_TOKEN"
    }
  }
}
```

### Discord

1. Create application at https://discord.com/developers/applications
2. Create bot and get token
3. Add to config:

```json
{
  "channels": {
    "discord": {
      "token": "YOUR_BOT_TOKEN"
    }
  }
}
```

## 🔧 Common Commands

```bash
# Version info
moltbot --version

# Gateway management
moltbot gateway                    # Start foreground
moltbot gateway status            # Check status
moltbot gateway restart           # Restart

# Channel management
moltbot channels status           # All channels
moltbot channels login            # Pair WhatsApp

# TUI (Terminal UI)
moltbot tui                       # Interactive terminal

# Configuration
moltbot doctor                    # Check setup
moltbot config                    # View config

# Logs
moltbot logs                      # View logs
```

## 📁 Directory Structure

```
~/moltbot/                    # Moltbot installation
├── dist/                     # Compiled code
├── ui/                       # Control UI source
├── src/                      # Source code
└── scripts/                  # Utility scripts

~/.clawdbot/                  # User config & data
├── moltbot.json             # Main config
├── agents/                   # Agent data
│   └── main/
├── media/                    # Downloaded media
└── sessions/                 # WhatsApp sessions

~/your-workspace/             # Your workspace (nama bisa bebas)
├── AGENTS.md                # Agent instructions
├── CONTEXT.md               # Command definitions
├── memory/                  # Memory logs
└── scripts/                 # Your scripts
```

## 🔄 Updating Moltbot

### From Source

```bash
cd ~/moltbot
git pull
pnpm install
pnpm ui:build
pnpm build
pnpm moltbot gateway restart
```

### Global Install

```bash
npm update -g moltbot
moltbot gateway restart
```

## 🛠️ Troubleshooting

### Gateway won't start

```bash
# Check if port is in use
lsof -i :18789

# Kill process if needed
kill -9 <PID>

# Restart
pnpm moltbot gateway restart
```

### WhatsApp disconnected

```bash
# Relogin
pnpm moltbot channels login

# Check status
pnpm moltbot channels status
```

### Update Moltbot

```bash
cd ~/moltbot
git pull
pnpm install
pnpm ui:build
pnpm build

# Restart gateway
pnpm moltbot gateway restart
```

## 📚 Resources

- **Docs:** https://docs.molt.bot
- **GitHub:** https://github.com/moltbot/moltbot
- **Discord:** Community support

## 🎉 Next Steps

After installation:
1. Setup your workspace folder (e.g., `~/moltbot-workspace`)
2. Configure `CONTEXT.md` for bot instructions
3. Setup skills and automations
4. Test with WhatsApp messages

---

**✅ Installation complete!** Your bot is ready to use.
