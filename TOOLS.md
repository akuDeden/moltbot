# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
---

## ⚠️ CRITICAL: Sprint Ticket Queries

**WHEN USER ASKS:** "review tiket sprint X" OR "list sprint tickets" OR "berikan list tiket sprint X"

**YOU MUST RUN THIS COMMAND:**
```bash
python3 /Users/ahmadfaris/moltbot-workspace/scripts/get-tickets-sprint.py [sprint_number]
```

**Examples:**
- Sprint 2: `python3 /Users/ahmadfaris/moltbot-workspace/scripts/get-tickets-sprint.py 2`
  - Returns: 71 tickets
- Sprint 1: `python3 /Users/ahmadfaris/moltbot-workspace/scripts/get-tickets-sprint.py 1`

**DO NOT:**
- ❌ Use any other script for sprint queries
- ❌ Use old cached data
- ❌ Call Notion API directly
- ❌ Use notion-client SDK (incompatible with old databases)

**Script details:**
- Uses Notion API v2022-06-28 (legacy endpoint)
- Handles UUID format automatically (removes dashes)
- Implements pagination for 2000+ tickets
- Credentials: `/Users/ahmadfaris/moltbot-workspace/notion-credentials.json`

---

## 📝 Notion Integration

**Credentials:**
- Location: `/Users/ahmadfaris/moltbot-workspace/notion-credentials.json`
- API Token: Stored in `notion-credentials.json` (key: `notion_token`)

**Database IDs:**
- Development/Sprint Tasks: `32e29af7d7dd4df69310270de8830d1a`
- Bug Tickets: `482be0a206b044d99fff5798db2381e4`
- Sprint Timeline: `e24adcac28d64eae9ce59794034dec75`

**Note:** Script uses Notion API v2022-06-28 with httpx (not notion-client SDK) because of API version compatibility issues.

**Quick Commands:**
```bash
# Setup
export NOTION_TOKEN=$(cat /Users/ahmadfaris/moltbot-workspace/notion-credentials.json | jq -r .notion_token)

# List dev tickets
python3 scripts/notion_reader/list_dev_tickets.py

# Search any sprint (scalable!)
python3 scripts/notion_reader/list_all_pages.py --search "Sprint 2"
python3 scripts/notion_reader/list_all_pages.py --search "Sprint 83"

# List bugs
python3 scripts/notion_reader/list_bug_tickets.py --priority "High"

# Read full ticket with content
python3 scripts/notion_reader/clawbot_ticket_reader.py --ticket-id <page_id>
```

