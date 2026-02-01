# Summary: N8N Dynamic Ticket Query System

## 📦 What Was Created

Sistem query ticket Notion yang dinamis menggunakan n8n workflow, bisa dipicu dari berbagai sumber (webhook, chat bot, CLI, API).

## 🎯 Key Improvements from Original Workflow

### Before (Manual Workflow)
- ❌ Manual trigger only
- ❌ Fixed database ID (hardcoded)
- ❌ No filtering capability
- ❌ Fixed limit (10 items)
- ❌ Basic output format

### After (Dynamic Workflow)
- ✅ Webhook trigger (HTTP POST/GET)
- ✅ Dynamic database ID
- ✅ Multiple filters (sprint, status, assignee, priority, tags, keywords)
- ✅ Configurable limit (up to 100)
- ✅ Multiple output formats (text, JSON, grouped)
- ✅ Error handling with proper HTTP status codes
- ✅ Easy integration with chat bots, scripts, cron jobs

## 📁 Files Created

### 1. N8N Workflow
**File:** `n8n-workflow-dynamic-tickets.json`
- Complete n8n workflow configuration
- Webhook trigger + 7 processing nodes
- Ready to import

### 2. Documentation
**File:** `docs/N8N-DYNAMIC-TICKETS.md`
- Complete API documentation
- Request/response examples
- Integration examples (Python, JavaScript, Bash)
- Use cases and troubleshooting

**File:** `docs/N8N-QUICK-REF.md`
- Quick reference guide
- Common commands
- Troubleshooting tips
- Real-world examples

### 3. Scripts

**File:** `scripts/tickets/n8n-query-tickets.py` (executable)
- Python CLI client
- Full parameter support
- Multiple output formats
- Error handling

**File:** `scripts/tickets/n8n-tickets.sh` (executable)
- Bash wrapper for quick commands
- Simple interface (sprint, status, search, assignee, all)
- Perfect for chat bot integration

### 4. Integration
**File:** `persona/QA.md` (updated)
- Added COMMAND 2 section for n8n integration
- Examples and usage patterns
- Fallback to legacy scripts when n8n not available

## 🚀 How to Use

### Step 1: Deploy N8N Workflow
```bash
# 1. Import workflow to n8n
#    - Open n8n
#    - Import from file: n8n-workflow-dynamic-tickets.json
#    - Update credential reference
#    - Activate workflow

# 2. Get webhook URL
#    Example: https://n8n.yourdomain.com/webhook/query-tickets

# 3. Set environment variable
echo 'export N8N_WEBHOOK_URL="https://n8n.yourdomain.com/webhook/query-tickets"' >> ~/.env
source ~/.env
```

### Step 2: Test
```bash
# Quick test
curl -X POST $N8N_WEBHOOK_URL -H "Content-Type: application/json" -d '{}'

# Or using scripts
./scripts/tickets/n8n-tickets.sh all
```

### Step 3: Use from Chat Bot
```bash
# Example commands user can send to bot:
# "cari tiket sprint 2"
# "tiket in progress"
# "cari tiket sales"

# Bot executes:
/Users/ahmadfaris/moltbot-workspace/scripts/tickets/n8n-tickets.sh sprint "Sprint 2"
```

## 🎯 Use Cases

1. **Daily Standup**
   ```bash
   python3 scripts/tickets/n8n-query-tickets.py --assignee "Ahmad" --status "In Progress"
   ```

2. **Sprint Planning**
   ```bash
   ./scripts/tickets/n8n-tickets.sh sprint "Sprint 2"
   ```

3. **Bug Triage**
   ```bash
   python3 scripts/tickets/n8n-query-tickets.py \
     --database-id "482be0a206b044d99fff5798db2381e4" \
     --priority "High"
   ```

4. **Quick Search**
   ```bash
   ./scripts/tickets/n8n-tickets.sh search "authentication"
   ```

5. **Automated Reports** (cron)
   ```bash
   # Add to crontab
   0 9 * * 1-5 python3 ~/moltbot-workspace/scripts/tickets/n8n-query-tickets.py \
     --sprint "Sprint 2" --output compact | mail -s "Daily Sprint Status" team@company.com
   ```

## 📊 Supported Filters

- ✅ Sprint name
- ✅ Status/Workflow
- ✅ Assignee
- ✅ Priority
- ✅ Tags (multiple)
- ✅ Keywords (search in title)
- ✅ Limit results
- ✅ Sort by created/edited time
- ✅ Sort direction

## 🔗 Integration Points

### Chat Bots (Telegram, Discord, WhatsApp)
```python
# Example: Handle user message
if "tiket sprint" in message:
    sprint = extract_sprint_number(message)
    result = query_tickets(sprint=sprint)
    send_reply(result)
```

### Web Dashboards
```javascript
// Fetch and display tickets
fetch('https://n8n.com/webhook/query-tickets', {
  method: 'POST',
  body: JSON.stringify({ sprint: 'Sprint 2', status: 'In Progress' })
})
.then(r => r.json())
.then(data => renderTickets(data.data.tickets))
```

### Slack/Discord Webhooks
```bash
# Send sprint status to Slack daily
STATUS=$(python3 scripts/tickets/n8n-query-tickets.py --sprint "Sprint 2" --output compact)
curl -X POST $SLACK_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"$STATUS\"}"
```

### Alfred/Raycast Workflows
```bash
# Quick search from macOS launcher
alfred-search-tickets() {
  python3 ~/moltbot-workspace/scripts/tickets/n8n-query-tickets.py \
    --keywords "$1" --output compact
}
```

## 🎨 Output Formats

1. **Text** - Formatted with emojis, grouped by status
2. **Compact** - Brief list with key info
3. **JSON** - Full structured data
4. **URLs** - Just ticket URLs (for piping)

## 🔐 Security

1. **Authentication:** Add API key header in webhook if needed
2. **Rate Limiting:** Enable in n8n settings
3. **IP Whitelist:** Restrict webhook access
4. **HTTPS Only:** Always use secure connection

## 📈 Next Steps

1. ✅ Import workflow to n8n
2. ✅ Test basic functionality
3. ✅ Integrate with chat bot commands
4. ⏳ Add to daily standup routine
5. ⏳ Set up automated reports
6. ⏳ Create custom Alfred/Raycast workflows

## 🐛 Troubleshooting

### "N8N_WEBHOOK_URL not configured"
```bash
# Set in .env
export N8N_WEBHOOK_URL="https://your-n8n.com/webhook/query-tickets"
```

### "Connection error"
```bash
# Verify n8n is accessible
curl -v $N8N_WEBHOOK_URL
```

### "No results"
- Check filter values (case-sensitive)
- Verify database has data
- Try removing filters

### "Timeout"
- Reduce limit parameter
- Add more specific filters
- Check n8n instance performance

## 📚 Documentation

- Full docs: `docs/N8N-DYNAMIC-TICKETS.md`
- Quick ref: `docs/N8N-QUICK-REF.md`
- Integration: `persona/QA.md` (COMMAND 2)

## 💡 Key Features

1. **Flexible Filtering** - Combine multiple filters
2. **Multiple Outputs** - Choose format based on need
3. **Easy Integration** - Works with any system
4. **Error Handling** - Proper HTTP status codes
5. **Scalable** - Handle large datasets with pagination
6. **User-Friendly** - Formatted text output for humans
7. **Machine-Readable** - JSON for automation

## 🎓 Example Workflow

```
User message: "cari tiket sprint 2 yang in progress"
      ↓
Chat bot parses request
      ↓
Executes: n8n-tickets.sh sprint "Sprint 2"
      ↓
Script calls n8n webhook with filters
      ↓
N8N queries Notion database
      ↓
Returns formatted results
      ↓
Bot sends reply to user
```

---

**Created:** 2026-01-30  
**Status:** Ready to deploy  
**Next:** Import workflow and configure webhook URL
