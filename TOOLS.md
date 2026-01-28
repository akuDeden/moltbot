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

## 📝 Notion Integration

**Credentials:**
- Location: `/Users/ahmadfaris/moltbot-workspace/notion-credentials.json`
- API Token: Stored in `notion-credentials.json` (key: `notion_token`)

**Database IDs:**
- Development/Sprint Tasks: `32e29af7d7dd4df69310270de8830d1a`
- Bug Tickets: `482be0a206b044d99fff5798db2381e4`

**Scripts Location:** `/Users/ahmadfaris/moltbot-workspace/scripts/notion_reader/`

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

**Key Point:** NO need for separate `search-sprint1.py`, `search-sprint2.py` scripts! Use generic `list_all_pages.py --search "Sprint N"` for any sprint number.