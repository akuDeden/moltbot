# N8N Ticket Query - Quick Reference

## 🚀 Setup

1. **Import workflow:** 
   - Import `n8n-workflow-dynamic-tickets.json` to n8n
   - Update Notion credential reference
   - Activate workflow

2. **Get webhook URL:**
   - Copy webhook URL from n8n (e.g., `https://n8n.yourdomain.com/webhook/query-tickets`)

3. **Configure:**
   ```bash
   # Add to ~/.env or .bashrc
   export N8N_WEBHOOK_URL="https://n8n.yourdomain.com/webhook/query-tickets"
   ```

4. **Test:**
   ```bash
   curl -X POST $N8N_WEBHOOK_URL -H "Content-Type: application/json" -d '{}'
   ```

## 📝 Quick Commands

### Bash Wrapper (Simplest)

```bash
# Sprint queries
./scripts/tickets/n8n-tickets.sh sprint "Sprint 2"

# Status
./scripts/tickets/n8n-tickets.sh status "In Progress"

# Search
./scripts/tickets/n8n-tickets.sh search "sales"

# Assignee
./scripts/tickets/n8n-tickets.sh assignee "Ahmad"

# All tickets
./scripts/tickets/n8n-tickets.sh all
```

### Python CLI (More Control)

```bash
# Basic filters
python3 scripts/tickets/n8n-query-tickets.py --sprint "Sprint 2"
python3 scripts/tickets/n8n-query-tickets.py --status "In Progress"
python3 scripts/tickets/n8n-query-tickets.py --keywords "sales"
python3 scripts/tickets/n8n-query-tickets.py --assignee "Ahmad"

# Combined filters
python3 scripts/tickets/n8n-query-tickets.py \
  --sprint "Sprint 2" \
  --status "In Progress" \
  --priority "High"

# Output formats
python3 scripts/tickets/n8n-query-tickets.py --sprint "Sprint 2" --output text
python3 scripts/tickets/n8n-query-tickets.py --sprint "Sprint 2" --output compact
python3 scripts/tickets/n8n-query-tickets.py --sprint "Sprint 2" --output json
python3 scripts/tickets/n8n-query-tickets.py --sprint "Sprint 2" --output urls

# Limit results
python3 scripts/tickets/n8n-query-tickets.py --sprint "Sprint 2" --limit 10

# All tickets (no filter)
python3 scripts/tickets/n8n-query-tickets.py --all
```

### Direct curl (API Testing)

```bash
# Basic query
curl -X POST $N8N_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{}'

# Sprint filter
curl -X POST $N8N_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{"sprint": "Sprint 2"}'

# Multiple filters
curl -X POST $N8N_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{
    "sprint": "Sprint 2",
    "status": "In Progress",
    "assignee": "Ahmad"
  }'

# Keyword search
curl -X POST $N8N_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{"keywords": "sales", "limit": 20}'

# Priority filter
curl -X POST $N8N_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{
    "sprint": "Sprint 2",
    "priority": "High"
  }'
```

## 🎯 Common Use Cases

### 1. Daily Standup
```bash
# My tickets in progress
python3 scripts/tickets/n8n-query-tickets.py \
  --assignee "Ahmad" \
  --status "In Progress" \
  --output compact
```

### 2. Sprint Planning
```bash
# All sprint tickets grouped by status
python3 scripts/tickets/n8n-query-tickets.py \
  --sprint "Sprint 2" \
  --output text
```

### 3. Bug Triage
```bash
# High priority open bugs
python3 scripts/tickets/n8n-query-tickets.py \
  --database-id "482be0a206b044d99fff5798db2381e4" \
  --priority "High" \
  --status "Open"
```

### 4. Quick Search
```bash
# Find tickets about specific feature
./scripts/tickets/n8n-tickets.sh search "authentication"
```

### 5. Team Status
```bash
# Check team member's tickets
./scripts/tickets/n8n-tickets.sh assignee "Deden"
```

### 6. Open URLs
```bash
# Open all "In Review" tickets in browser
python3 scripts/tickets/n8n-query-tickets.py \
  --status "In Review" \
  --output urls | xargs open
```

## 📊 Filter Options

| Filter | Type | Example | Description |
|--------|------|---------|-------------|
| `--sprint` | String | "Sprint 2" | Filter by sprint name |
| `--status` | String | "In Progress" | Filter by status/workflow |
| `--assignee` | String | "Ahmad" | Filter by assignee |
| `--priority` | String | "High" | Filter by priority |
| `--keywords` | String | "sales" | Search in title |
| `--tags` | Array | backend api | Filter by tags |
| `--limit` | Number | 20 | Max results |
| `--database-id` | String | 32e29af7... | Different database |

## 🔍 Output Formats

### Text (Default)
```
📊 *Hasil Query Ticket*

Total: 5 ticket
Sprint: Sprint 2

---

*In Progress* (3):

1. *Implement Sales API*
   Sprint: Sprint 2
   Assignee: Ahmad
   ...
```

### Compact
```
📊 Found 5 ticket(s)

1. Implement Sales API
   Status: In Progress | Sprint: Sprint 2 | Assignee: Ahmad
   🔗 https://notion.so/...
```

### JSON
```json
{
  "success": true,
  "count": 5,
  "tickets": [...],
  "formatted": {...}
}
```

### URLs
```
https://notion.so/ticket-1
https://notion.so/ticket-2
https://notion.so/ticket-3
```

## 🔧 Troubleshooting

### Webhook not configured
```bash
echo $N8N_WEBHOOK_URL
# Should show: https://your-n8n.com/webhook/query-tickets
```

### Connection error
```bash
# Test webhook directly
curl -v $N8N_WEBHOOK_URL
```

### No results
- Check filter values (case-sensitive for some fields)
- Try removing filters one by one
- Verify database has data

### Timeout
- Reduce `--limit` parameter
- Add more specific filters
- Check n8n instance status

## 📚 Resources

- Full docs: `docs/N8N-DYNAMIC-TICKETS.md`
- Workflow: `n8n-workflow-dynamic-tickets.json`
- Python client: `scripts/tickets/n8n-query-tickets.py`
- Bash wrapper: `scripts/tickets/n8n-tickets.sh`
- Integration examples: See docs file

## 💡 Tips

1. **Start simple:** Use bash wrapper for quick queries
2. **Combine filters:** Python CLI for complex queries
3. **Pipe output:** Use `--output urls` with `xargs`
4. **Save queries:** Create shell aliases for frequent queries
5. **Automate:** Use with cron for periodic reports

## 🎓 Examples

```bash
# Alias examples (add to ~/.bashrc or ~/.zshrc)
alias sprint2="python3 ~/moltbot-workspace/scripts/tickets/n8n-query-tickets.py --sprint 'Sprint 2' --output compact"
alias my-tickets="python3 ~/moltbot-workspace/scripts/tickets/n8n-query-tickets.py --assignee 'Ahmad' --output compact"
alias urgent="python3 ~/moltbot-workspace/scripts/tickets/n8n-query-tickets.py --priority 'High' --status 'Open'"

# Then just run:
sprint2
my-tickets
urgent
```

---

**Quick start:** Import workflow → Set webhook URL → Run `n8n-tickets.sh sprint "Sprint 2"` ✨
