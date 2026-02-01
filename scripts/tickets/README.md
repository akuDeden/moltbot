# Ticket Management Scripts

Collection of scripts for querying and managing Notion tickets.

## 🚀 Quick Start

### Recommended: N8N Webhook (Dynamic & Flexible)

```bash
# Setup
export N8N_WEBHOOK_URL="https://your-n8n.com/webhook/query-tickets"

# Simple queries
./n8n-tickets.sh sprint "Sprint 2"
./n8n-tickets.sh status "In Progress"
./n8n-tickets.sh search "sales"
./n8n-tickets.sh assignee "Ahmad"

# Advanced queries
python3 n8n-query-tickets.py --sprint "Sprint 2" --status "In Progress" --output compact
```

**Prerequisites:** n8n workflow deployed (see `../../docs/N8N-DYNAMIC-TICKETS.md`)

### Alternative: Direct Notion API

```bash
# Sprint queries
./query-sprint-tickets.sh 2

# Search with filters
python3 query-tickets.py "sales" --sprint "Sprint 2"

# Get sprint tickets with status
python3 get-sprint-tickets-status.py 2
```

## 📁 Scripts Overview

### 🆕 N8N Integration (Recommended)

| Script | Purpose | Usage |
|--------|---------|-------|
| `n8n-tickets.sh` | Simple wrapper | `./n8n-tickets.sh sprint "Sprint 2"` |
| `n8n-query-tickets.py` | Full CLI client | `python3 n8n-query-tickets.py --sprint "Sprint 2"` |

**Features:**
- ✅ Dynamic filtering (sprint, status, assignee, priority, tags, keywords)
- ✅ Multiple output formats (text, compact, JSON, URLs)
- ✅ Fast (API-based, no pagination delays)
- ✅ Easy integration with chat bots

**Docs:** `../../docs/N8N-DYNAMIC-TICKETS.md`, `../../docs/N8N-QUICK-REF.md`

### 📋 Query Scripts (Direct API)

| Script | Purpose | Database | Usage |
|--------|---------|----------|-------|
| `query-sprint-tickets.sh` | Get all tickets by sprint number | Dev | `./query-sprint-tickets.sh 2` |
| `query-tickets.py` | Search tickets by keywords | Dev | `python3 query-tickets.py "sales"` |
| `get-sprint-tickets-status.py` | Sprint tickets grouped by status | Dev | `python3 get-sprint-tickets-status.py 2` |
| `get-tickets-sprint.py` | Basic sprint query | Dev | `python3 get-tickets-sprint.py 2` |

### 🔍 Search & Verify

| Script | Purpose | Usage |
|--------|---------|-------|
| `find-elasticsearch-ticket.py` | Search in multiple databases | `python3 find-elasticsearch-ticket.py "TECH-123"` |
| `verify-ticket.py` | Check ticket existence & details | `python3 verify-ticket.py "TECH-123"` |

### ✏️ Update Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `update-ticket-status.py` | Change ticket status | `python3 update-ticket-status.py "TECH-123" "Done"` |
| `update-ticket-assignee.py` | Assign ticket | `python3 update-ticket-assignee.py "TECH-123" "Ahmad"` |
| `update-ticket-assignee-simple.py` | Simple assignee update | `python3 update-ticket-assignee-simple.py "TECH-123" "Ahmad"` |
| `update-ticket-property.py` | Update any property | `python3 update-ticket-property.py "TECH-123" "Priority" "High"` |

### 🐛 Bug Management

| Script | Purpose | Usage |
|--------|---------|-------|
| `create-bug-ticket.py` | Create new bug report | `python3 create-bug-ticket.py --title "Login broken"` |

## 🔧 Configuration

### Method 1: Environment Variables (.env)

```bash
# ~/.env or project .env
export NOTION_TOKEN="secret_xxx"
export DATABASE_DEV="32e29af7d7dd4df69310270de8830d1a"
export DATABASE_BUG="482be0a206b044d99fff5798db2381e4"
export SPRINT_DATABASE_ID="e24adcac28d64eae9ce59794034dec75"
export N8N_WEBHOOK_URL="https://your-n8n.com/webhook/query-tickets"
```

### Method 2: Credentials File

```json
// /Users/ahmadfaris/moltbot-workspace/notion-credentials.json
{
  "notion_token": "secret_xxx",
  "database_dev": "32e29af7d7dd4df69310270de8830d1a",
  "database_bug": "482be0a206b044d99fff5798db2381e4",
  "sprint_database_id": "e24adcac28d64eae9ce59794034dec75"
}
```

## 🎯 Common Use Cases

### Daily Standup

```bash
# My in-progress tickets
python3 n8n-query-tickets.py --assignee "Ahmad" --status "In Progress" --output compact

# Or using legacy script
python3 query-tickets.py "" --assignee "Ahmad" --status "In Progress"
```

### Sprint Planning

```bash
# All sprint tickets (n8n)
./n8n-tickets.sh sprint "Sprint 2"

# Or direct API
./query-sprint-tickets.sh 2

# With status breakdown
python3 get-sprint-tickets-status.py 2
```

### Bug Triage

```bash
# High priority bugs (n8n with bug database)
python3 n8n-query-tickets.py \
  --database-id "482be0a206b044d99fff5798db2381e4" \
  --priority "High" \
  --status "Open"
```

### Quick Search

```bash
# Search in title (n8n)
./n8n-tickets.sh search "authentication"

# Or direct API
python3 query-tickets.py "authentication"
```

### Ticket Updates

```bash
# Change status
python3 update-ticket-status.py "TECH-123" "Done"

# Reassign
python3 update-ticket-assignee.py "TECH-123" "Ahmad"

# Update property
python3 update-ticket-property.py "TECH-123" "Priority" "High"
```

## 📊 Output Formats

### N8N Scripts

```bash
# Formatted text (default)
./n8n-tickets.sh sprint "Sprint 2"

# Compact list
python3 n8n-query-tickets.py --sprint "Sprint 2" --output compact

# Full JSON
python3 n8n-query-tickets.py --sprint "Sprint 2" --output json

# Just URLs (for piping)
python3 n8n-query-tickets.py --sprint "Sprint 2" --output urls
```

### Legacy Scripts

- Standard output with emoji status indicators
- Grouped by status (where applicable)
- Includes: title, status, sprint, assignee, URL

## 🔄 Migration Guide

### From Legacy to N8N

**Before:**
```bash
python3 query-tickets.py "sales" --sprint "Sprint 2"
```

**After:**
```bash
python3 n8n-query-tickets.py --keywords "sales" --sprint "Sprint 2"
# or
./n8n-tickets.sh search "sales"
```

**Benefits:**
- Faster (API webhook vs pagination)
- More filters available
- Multiple output formats
- Better error handling
- Easier integration

## 🐛 Troubleshooting

### "Credentials not found"

```bash
# Check .env
cat ~/.env | grep NOTION_TOKEN

# Or check credentials file
cat /Users/ahmadfaris/moltbot-workspace/notion-credentials.json
```

### "N8N webhook error"

```bash
# Verify URL is set
echo $N8N_WEBHOOK_URL

# Test connection
curl -v $N8N_WEBHOOK_URL
```

### "No results"

- Check filter values (case-sensitive for some fields)
- Verify database has data
- Try without filters first
- Check database ID is correct

### "Script not executable"

```bash
chmod +x n8n-tickets.sh
chmod +x query-sprint-tickets.sh
chmod +x n8n-query-tickets.py
```

## 📚 Documentation

- **N8N System:** `../../docs/N8N-DYNAMIC-TICKETS.md` (full docs)
- **Quick Ref:** `../../docs/N8N-QUICK-REF.md`
- **Summary:** `../../docs/N8N-SUMMARY.md`
- **Integration:** `../../persona/QA.md` (COMMAND 2)

## 💡 Tips

1. **Start with n8n scripts** for most queries (faster, more features)
2. **Use legacy scripts** when n8n is not available
3. **Pipe URLs** to open tickets: `python3 n8n-query-tickets.py ... --output urls | xargs open`
4. **Create aliases** for frequent queries in `~/.bashrc` or `~/.zshrc`
5. **Automate reports** with cron using n8n scripts

## 🎓 Examples

```bash
# Daily standup
alias my-tickets="python3 ~/moltbot-workspace/scripts/tickets/n8n-query-tickets.py --assignee 'Ahmad' --status 'In Progress' --output compact"

# Sprint overview
alias sprint2="./n8n-tickets.sh sprint 'Sprint 2'"

# Urgent bugs
alias urgent-bugs="python3 ~/moltbot-workspace/scripts/tickets/n8n-query-tickets.py --database-id '482be0a206b044d99fff5798db2381e4' --priority 'High' --status 'Open'"
```

---

**Recommended:** Start with n8n integration for best experience. See `../../docs/N8N-QUICK-REF.md` for quick start guide.
