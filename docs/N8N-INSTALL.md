# 🚀 N8N Ticket Query - Installation & Setup Guide

Quick guide untuk deploy dan setup n8n dynamic ticket query system.

## 📋 Prerequisites

- ✅ n8n instance (self-hosted atau cloud)
- ✅ Notion account dengan API access
- ✅ Python 3.7+ (untuk CLI scripts)
- ✅ bash/zsh shell
- ✅ curl (untuk testing)

## 🛠️ Installation Steps

### 1. Deploy N8N Workflow

#### Option A: Import from File
1. Login ke n8n dashboard
2. Click **Workflows** → **Import from File**
3. Select: `n8n-workflow-dynamic-tickets.json`
4. Click **Import**

#### Option B: Import from URL
```bash
# Copy workflow JSON
cat n8n-workflow-dynamic-tickets.json | pbcopy

# Or upload to gist/pastebin and import via URL
```

### 2. Configure Notion Credentials

1. Di n8n workflow editor, click node **"Get Notion Tickets"**
2. Click **Credentials** dropdown
3. Choose existing `notion_creds_main` atau create new:
   - Credential Type: **Notion API**
   - API Key: `secret_xxx` (dari [notion.so/my-integrations](https://www.notion.so/my-integrations))
   - Internal Integration: **Yes**
4. Test connection
5. Save credentials

### 3. Activate Workflow

1. Click toggle switch **Inactive → Active**
2. Workflow status should show **Active** (green)
3. Copy **Webhook URL** from the webhook trigger node
   - Example: `https://your-n8n.com/webhook/query-tickets`

### 4. Configure Environment

#### On your local machine:

```bash
# Add to ~/.env or ~/.zshrc or ~/.bashrc
export N8N_WEBHOOK_URL="https://your-n8n.com/webhook/query-tickets"

# Reload shell
source ~/.env  # or source ~/.zshrc
```

#### Verify:
```bash
echo $N8N_WEBHOOK_URL
# Should output: https://your-n8n.com/webhook/query-tickets
```

### 5. Install Python Dependencies

```bash
# Install httpx for Python client
pip3 install httpx

# Optional: python-dotenv for .env file support
pip3 install python-dotenv
```

### 6. Test Installation

```bash
cd /Users/ahmadfaris/moltbot-workspace/scripts/tickets

# Run test suite
./test-n8n-setup.sh
```

Expected output:
```
🧪 N8N Ticket Query System - Test Suite
========================================

1. Checking environment...
✅ N8N_WEBHOOK_URL configured

2. Checking scripts...
✅ n8n-tickets.sh found
✅ n8n-query-tickets.py found

3. Testing webhook connectivity...
✅ Webhook responds with HTTP 200

4. Testing basic query...
✅ Query successful

5. Testing bash wrapper...
✅ Bash wrapper works

6. Testing Python client...
✅ Python client works

7. Testing filtered query...
✅ Filtered query works (returned 10 tickets)
```

### 7. Verify with Manual Test

```bash
# Test 1: Basic query
curl -X POST $N8N_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{"limit": 5}' | jq

# Test 2: With filters
./scripts/tickets/n8n-tickets.sh all

# Test 3: Python client
python3 scripts/tickets/n8n-query-tickets.py --limit 5 --output compact
```

## 🎯 Quick Start Examples

### Bash Wrapper (Simplest)
```bash
cd /Users/ahmadfaris/moltbot-workspace/scripts/tickets

# Query by sprint
./n8n-tickets.sh sprint "Sprint 2"

# Query by status
./n8n-tickets.sh status "In Progress"

# Search keywords
./n8n-tickets.sh search "sales"

# Query by assignee
./n8n-tickets.sh assignee "Ahmad"

# Get all tickets
./n8n-tickets.sh all
```

### Python CLI (Advanced)
```bash
# Multiple filters
python3 scripts/tickets/n8n-query-tickets.py \
  --sprint "Sprint 2" \
  --status "In Progress" \
  --output compact

# Search with limit
python3 scripts/tickets/n8n-query-tickets.py \
  --keywords "api" \
  --limit 20

# Different output formats
python3 scripts/tickets/n8n-query-tickets.py \
  --sprint "Sprint 2" \
  --output text      # Full formatted (default)

python3 scripts/tickets/n8n-query-tickets.py \
  --sprint "Sprint 2" \
  --output compact   # Brief list

python3 scripts/tickets/n8n-query-tickets.py \
  --sprint "Sprint 2" \
  --output json      # Full JSON

python3 scripts/tickets/n8n-query-tickets.py \
  --sprint "Sprint 2" \
  --output urls      # Just URLs
```

### Direct API Call
```bash
# Using curl
curl -X POST $N8N_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{
    "sprint": "Sprint 2",
    "status": "In Progress",
    "limit": 10
  }' | jq -r '.message'
```

## 🔧 Integration with Chat Bot

### Add to persona/QA.md (already done)

User commands:
```
"cari tiket sprint 2"
"tiket in progress"
"cari tiket sales"
```

Bot executes:
```bash
/Users/ahmadfaris/moltbot-workspace/scripts/tickets/n8n-tickets.sh sprint "Sprint 2"
```

### Add Alias for Quick Access

```bash
# Add to ~/.bashrc or ~/.zshrc
alias n8n-tickets="cd /Users/ahmadfaris/moltbot-workspace/scripts/tickets && ./n8n-tickets.sh"
alias sprint2="python3 /Users/ahmadfaris/moltbot-workspace/scripts/tickets/n8n-query-tickets.py --sprint 'Sprint 2' --output compact"
alias my-tickets="python3 /Users/ahmadfaris/moltbot-workspace/scripts/tickets/n8n-query-tickets.py --assignee 'Ahmad' --output compact"

# Then use:
n8n-tickets sprint "Sprint 2"
sprint2
my-tickets
```

## 📊 Files Created

```
moltbot-workspace/
├── n8n-workflow-dynamic-tickets.json     # N8N workflow config
├── .env.example-n8n                      # Environment template
├── docs/
│   ├── N8N-DYNAMIC-TICKETS.md           # Full documentation
│   ├── N8N-QUICK-REF.md                 # Quick reference
│   ├── N8N-SUMMARY.md                   # Project summary
│   └── N8N-ARCHITECTURE.md              # System architecture
├── scripts/tickets/
│   ├── n8n-query-tickets.py            # Python CLI client
│   ├── n8n-tickets.sh                  # Bash wrapper
│   ├── test-n8n-setup.sh               # Test suite
│   └── README.md                        # Scripts documentation
└── persona/
    └── QA.md                            # Updated with n8n commands
```

## 🐛 Troubleshooting

### Issue: "N8N_WEBHOOK_URL not configured"

**Solution:**
```bash
export N8N_WEBHOOK_URL="https://your-n8n.com/webhook/query-tickets"
# Add to ~/.env for persistence
```

### Issue: "Connection error" or "Timeout"

**Solutions:**
1. Check n8n instance is running:
   ```bash
   curl -v $N8N_WEBHOOK_URL
   ```
2. Verify URL is correct (no typos)
3. Check firewall/network allows outbound HTTPS
4. Test from n8n UI directly

### Issue: "Notion API error"

**Solutions:**
1. Verify Notion credentials in n8n:
   - Open workflow → Get Notion Tickets node → Credentials
   - Test connection
2. Check Notion integration has access to database:
   - Open Notion database → Share → Add integration
3. Verify database ID is correct

### Issue: "No results" but database has data

**Solutions:**
1. Test without filters first:
   ```bash
   ./n8n-tickets.sh all
   ```
2. Check filter values match exactly (case-sensitive)
3. Verify property names in Notion (Status, Sprint, etc)
4. Test directly in n8n UI with manual execution

### Issue: "httpx module not found"

**Solution:**
```bash
pip3 install httpx
# or
pip3 install httpx python-dotenv
```

## 🎓 Next Steps

1. ✅ Verify installation with test suite
2. ✅ Try example queries
3. ✅ Add aliases to shell config
4. ⏳ Integrate with chat bot
5. ⏳ Set up automated reports (cron)
6. ⏳ Create custom workflows

## 📚 Documentation

- **Full Docs:** `docs/N8N-DYNAMIC-TICKETS.md`
- **Quick Ref:** `docs/N8N-QUICK-REF.md`
- **Architecture:** `docs/N8N-ARCHITECTURE.md`
- **Summary:** `docs/N8N-SUMMARY.md`
- **Scripts README:** `scripts/tickets/README.md`

## 💬 Support

Issues or questions:
1. Check troubleshooting section above
2. Review documentation files
3. Test with `./test-n8n-setup.sh`
4. Check n8n execution logs

## ✨ Success Checklist

- [ ] N8N workflow imported and active
- [ ] Notion credentials configured
- [ ] Webhook URL copied and saved to `$N8N_WEBHOOK_URL`
- [ ] Python dependencies installed (`httpx`)
- [ ] Test suite passes (`./test-n8n-setup.sh`)
- [ ] Manual queries work
- [ ] Aliases added to shell config
- [ ] Integrated with chat bot (optional)

---

**You're all set!** 🎉

Start querying tickets with:
```bash
./scripts/tickets/n8n-tickets.sh sprint "Sprint 2"
```
