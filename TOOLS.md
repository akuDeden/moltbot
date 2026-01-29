# TOOLS.md - Local Notes

Environment-specific configuration and local setup details.

**For commands, see:**
- Ticket management → `persona/QA.md`
- Shopping/notes → `persona/ASSISTANT.md`
- Attendance → `persona/WORKER.md`

---

## 🔐 Credentials & Paths

**Notion:**
- Credentials: `/Users/ahmadfaris/moltbot-workspace/notion-credentials.json`
- Also available in: `.env` (NOTION_TOKEN, DATABASE_DEV, DATABASE_BUG, SPRINT_DATABASE_ID)

**Google Sheets:**
- Service Account: `/Users/ahmadfaris/moltbot-workspace/google-credentials.json`
- Shopping Sheet ID: `1Ibt6u5_SK4Sck9uCdLTlvkk4OYPyrjaHo92Zr33pQMc`

---

## 🗄️ Notion Database IDs

**Development Tasks:**
- ID: `32e29af7d7dd4df69310270de8830d1a`
- Type: Sprint tickets, tech tasks, features

**Bug Tickets:**
- ID: `482be0a206b044d99fff5798db2381e4`
- Type: Bug reports, hotfixes

**Sprint Timeline:**
- ID: `e24adcac28d64eae9ce59794034dec75`
- Type: Sprint planning database

---

## 🌐 SSH & Hosts

**Primary Gateway:**
- Host: `exe.dev`
- Access: `ssh exe.dev` then `ssh vm-name`
- Use: Stable connection to VMs

**Notes:**
- SSH can be flaky - use exe.dev web terminal or Shelley as fallback
- Keep tmux sessions for long operations

---

## 🏢 HR System

**Attendance Portal:**
- Credentials stored in: `.env` (HR_URL, HR_EMAIL, HR_PASSWORD)
- State file: `~/moltbot-workspace/data/attendance-state.json`
- Scripts: `scripts/attendance/auto-absen.sh`, `dry-run-absen.sh`

---

## 📝 API Notes

**Notion API:**
- Version: `2022-06-28` (legacy endpoint required)
- Client: Uses `httpx` directly (not notion-client SDK)
- Reason: Compatibility with older database schema

---

Add any other environment-specific notes here as needed.

