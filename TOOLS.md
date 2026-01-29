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
python3 /Users/ahmadfaris/moltbot-workspace/scripts/tickets/get-tickets-sprint.py [sprint_number]
```

**Examples:**
- Sprint 2: `python3 /Users/ahmadfaris/moltbot-workspace/scripts/tickets/get-tickets-sprint.py 2`
  - Returns: 75 tickets grouped by status
- Sprint 1: `python3 /Users/ahmadfaris/moltbot-workspace/scripts/tickets/get-tickets-sprint.py 1`

**Filtering by Status:**
User may ask: "berikan list tiket sprint 2 yang status nya code review"
- Run the full command above
- Output is already grouped by status (CODE REVIEW, IN PROGRESS, NOT STARTED, etc.)
- Extract and show only the requested status section from output
- Example statuses: "Code review", "In progress", "Not started", "Ready for testing", "Deployed", "Ready for beta"

---

### 🔄 Update Ticket Properties

**WHEN USER ASKS:** "update tiket X dengan assignee Y dan status Z"

**USER LANGUAGE CONTEXT:**
- User says **"assignment"** or **"assignee"** → means **"Assignee"** property (NOT "Tester")
- User says **"status"** → means **"Status"** property (NOT "Domain")

**CRITICAL - Property Name Disambiguation:**
- **"Assignee"** = main assignee field (notion://tasks/assign_property) ✅ USE THIS
  - This is what user means by "assignment" or "assignee"
- **"Tester"** = separate QA tester field ❌ DO NOT use for general assignment
- **"Status"** = main workflow status (notion://tasks/status_property) ✅ USE THIS
  - This is what user means by "status"
- **"Domain"** = category/team field (select type) ❌ DO NOT use for workflow status

**Update Assignee:**
```bash
python3 /Users/ahmadfaris/moltbot-workspace/scripts/tickets/update-ticket-assignee-simple.py "<ticket_title>" "<assignee_name>"
```
Example: `python3 .../update-ticket-assignee-simple.py "Celery Worker Configuration" "Ahmad Faris"`

**Update Status:**
```bash
python3 /Users/ahmadfaris/moltbot-workspace/scripts/tickets/update-ticket-status.py "<ticket_title>" --status "<status_name>"
```
Example: `python3 .../update-ticket-status.py "Celery Worker Configuration" --status "In Progress"`

**Valid Status Values:**
- "Not Started" / "Not started"
- "In Progress" / "In progress"
- "Code Review" / "Code review"
- "Ready for testing (dev)" / "Ready for testing"
- "Testing (dev)" / "Testing"
- "Done"
- "Pending"
- "Deployed"

**Common User Names:**
- Ahmad Faris (faris@chronicle.rip)
- Yahya Fadhulloh Alfatih (yahya@chronicle.rip)
- Eko Santoso (eko@chronicle.rip)

**Verification:**
After update, verify with:
```bash
python3 /Users/ahmadfaris/moltbot-workspace/scripts/tickets/verify-ticket.py <ticket_id>
```

---

**Filtering by Status:**

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

