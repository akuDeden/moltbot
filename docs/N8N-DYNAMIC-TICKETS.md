# Dynamic Notion Tickets Query - n8n Workflow

## 📋 Overview

Workflow n8n yang dinamis untuk query tickets dari Notion database. Bisa dipicu dari berbagai sumber (webhook, chat bot, API call) dengan parameter yang fleksibel.

## 🚀 Fitur Utama

1. **Webhook Trigger** - Bisa dipanggil dari mana saja (HTTP POST)
2. **Dynamic Filtering** - Filter berdasarkan sprint, status, assignee, priority, tags, keywords
3. **Flexible Parameters** - Semua parameter optional dengan defaults yang sensible
4. **Formatted Response** - Output terstruktur dan user-friendly (text, JSON, grouped by status)
5. **Error Handling** - Proper error responses dengan HTTP status codes
6. **Pagination Support** - Limit hasil untuk performa optimal

## 📥 API Endpoint

Setelah workflow aktif, webhook URL:
```
POST https://your-n8n-instance.com/webhook/query-tickets
```

## 🔧 Request Parameters

Semua parameter **optional**. Kirim via POST body (JSON) atau query string.

### Core Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `database_id` | string | `32e29af7d7dd4df69310270de8830d1a` | Notion database ID |
| `keywords` | string | - | Search dalam title (partial match) |
| `sprint` | string | - | Filter by sprint name |
| `status` | string | - | Filter by status/workflow |
| `assignee` | string | - | Filter by assignee name |
| `priority` | string | - | Filter by priority level |
| `tags` | array/string | - | Filter by tags |
| `limit` | number | 100 | Max results (max: 100) |
| `sort_by` | string | `last_edited_time` | Sort field |
| `sort_direction` | string | `descending` | Sort direction |

### Example Requests

#### 1. Basic Query (All tickets)
```bash
curl -X POST https://your-n8n.com/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{}'
```

#### 2. Filter by Sprint
```bash
curl -X POST https://your-n8n.com/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{
    "sprint": "Sprint 2"
  }'
```

#### 3. Filter by Status and Sprint
```bash
curl -X POST https://your-n8n.com/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{
    "sprint": "Sprint 2",
    "status": "In Progress"
  }'
```

#### 4. Search with Keywords
```bash
curl -X POST https://your-n8n.com/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "sales",
    "sprint": "Sprint 2"
  }'
```

#### 5. Filter by Assignee
```bash
curl -X POST https://your-n8n.com/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{
    "assignee": "Ahmad",
    "status": "Done"
  }'
```

#### 6. Complex Query
```bash
curl -X POST https://your-n8n.com/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d '{
    "sprint": "Sprint 2",
    "status": "In Progress",
    "priority": "High",
    "tags": ["backend", "api"],
    "limit": 20
  }'
```

#### 7. Query String (via GET)
```bash
curl "https://your-n8n.com/webhook/query-tickets?sprint=Sprint%202&status=Done&limit=10"
```

## 📤 Response Format

### Success Response

```json
{
  "success": true,
  "message": "📊 *Hasil Query Ticket*\n\nTotal: 5 ticket\nSprint: Sprint 2\n\n---\n\n*In Progress* (3):\n\n1. *Implement Sales API*\n   Sprint: Sprint 2\n   Assignee: Ahmad\n   Priority: High\n   Tags: backend, api\n   🔗 https://notion.so/...\n\n...",
  "data": {
    "success": true,
    "count": 5,
    "params": {
      "databaseId": "32e29af7...",
      "sprint": "Sprint 2",
      "keywords": "",
      "limit": 100
    },
    "tickets": [
      {
        "id": "...",
        "title": "Implement Sales API",
        "status": "In Progress",
        "sprint": "Sprint 2",
        "assignee": "Ahmad",
        "priority": "High",
        "tags": ["backend", "api"],
        "url": "https://notion.so/...",
        "created_time": "2026-01-15T10:00:00.000Z",
        "last_edited_time": "2026-01-28T15:30:00.000Z"
      }
    ],
    "timestamp": "2026-01-30T12:00:00.000Z"
  },
  "formatted": {
    "text": "...",
    "markdown": "...",
    "count": 5,
    "grouped_by_status": {
      "In Progress": [...],
      "Done": [...]
    }
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": "Database not found",
  "timestamp": "2026-01-30T12:00:00.000Z"
}
```

## 🔗 Integration Examples

### 1. From Moltbot Chat Command

Add to `persona/QA.md` or similar:

```bash
# Query tickets via n8n webhook
curl -X POST https://your-n8n.com/webhook/query-tickets \
  -H "Content-Type: application/json" \
  -d "{
    \"sprint\": \"Sprint 2\",
    \"status\": \"In Progress\"
  }" | jq -r '.message'
```

### 2. From Python Script

```python
import httpx
import json

def query_tickets(sprint=None, status=None, keywords=None):
    url = "https://your-n8n.com/webhook/query-tickets"
    
    payload = {}
    if sprint:
        payload['sprint'] = sprint
    if status:
        payload['status'] = status
    if keywords:
        payload['keywords'] = keywords
    
    response = httpx.post(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(data['message'])
        return data['data']['tickets']
    else:
        print(f"Error: {response.status_code}")
        return None

# Usage
tickets = query_tickets(sprint="Sprint 2", status="In Progress")
```

### 3. From Discord Bot / Telegram

```javascript
// Example: Discord.js integration
async function queryNotionTickets(sprint, status) {
  const response = await fetch('https://your-n8n.com/webhook/query-tickets', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sprint, status })
  });
  
  const data = await response.json();
  
  if (data.success) {
    return data.message; // Send formatted message to Discord
  } else {
    return `❌ Error: ${data.error}`;
  }
}

// Discord command
client.on('messageCreate', async (message) => {
  if (message.content.startsWith('!tickets')) {
    const [, sprint, status] = message.content.split(' ');
    const result = await queryNotionTickets(sprint, status);
    message.reply(result);
  }
});
```

### 4. Scheduled Monitoring (n8n Schedule Trigger)

Tambahkan Schedule Trigger node di awal workflow untuk monitoring otomatis:

```json
{
  "parameters": {
    "rule": {
      "interval": [
        {
          "field": "hours",
          "hoursInterval": 2
        }
      ]
    }
  },
  "name": "Schedule Trigger",
  "type": "n8n-nodes-base.scheduleTrigger"
}
```

Lalu kirim hasil ke Slack/Discord/Email jika ada ticket urgent.

## 🎯 Use Cases

1. **Daily Standup Reports** - Query tickets per assignee untuk laporan harian
2. **Sprint Progress Tracking** - Monitor status tickets dalam sprint aktif
3. **Urgent Ticket Alerts** - Notifikasi otomatis untuk high-priority tickets
4. **Custom Dashboards** - Feed data ke dashboard/monitoring tools
5. **Chat Bot Integration** - Query tickets via chat commands
6. **Automated Reports** - Generate periodic reports (end of sprint, weekly, etc)

## 🔄 Workflow Nodes Explained

1. **Webhook Trigger** - Entry point untuk menerima HTTP requests
2. **Parse Request** - Extract & validate parameters dari request
3. **Get Notion Tickets** - Query Notion API dengan dynamic filters
4. **Extract & Filter Tickets** - Parse properties & apply keyword filtering
5. **Format Response** - Generate user-friendly output (text + JSON)
6. **Respond to Webhook** - Return success response
7. **Error Handler** - Catch errors dan format error responses
8. **Respond Error** - Return error response dengan HTTP 500

## ⚡ Performance Tips

1. **Use Limits** - Default 100 sudah optimal. Jangan set terlalu tinggi.
2. **Specific Filters** - Gunakan sprint/status filter untuk reduce data
3. **Cache Results** - Jika data tidak realtime, consider caching
4. **Pagination** - Untuk large datasets, implement pagination logic
5. **Async Processing** - Untuk report generation, use async workflow

## 🔐 Security

1. **API Key** - Add authentication header jika diperlukan:
   ```json
   {
     "headers": {
       "Authorization": "Bearer YOUR_API_KEY"
     }
   }
   ```

2. **Rate Limiting** - Enable rate limiting di n8n settings

3. **Allowed IPs** - Restrict webhook access ke IP tertentu

## 📊 Monitoring

Track usage via n8n execution logs:
- Total executions
- Success/error rate
- Average response time
- Most used filters

## 🛠️ Customization

### Add New Filters

Edit "Parse Request" node, tambahkan parameter baru:

```javascript
// Add Due Date filter
dueDate: body.due_date || query.due_date || '',

// In filter building
if (params.dueDate) {
  filters.push({
    property: 'Due Date',
    date: {
      equals: params.dueDate
    }
  });
}
```

### Change Output Format

Edit "Format Response" node untuk customize output format (CSV, HTML, Slack blocks, etc).

### Multiple Databases

Clone workflow dan ganti database_id, atau tambahkan routing logic:

```javascript
// Route based on database type
const dbType = body.type || 'dev';
const dbMap = {
  'dev': '32e29af7d7dd4df69310270de8830d1a',
  'bug': '482be0a206b044d99fff5798db2381e4'
};
params.databaseId = dbMap[dbType] || dbMap['dev'];
```

## 🐛 Troubleshooting

### Common Issues

1. **"Database not found"**
   - Check database_id is correct
   - Verify Notion integration has access to database

2. **"No results"**
   - Check filter values are exact matches
   - Try removing filters one by one
   - Check if database has data

3. **"Timeout"**
   - Reduce limit parameter
   - Add more specific filters
   - Check Notion API status

4. **"Invalid filter"**
   - Verify property names match Notion schema
   - Check property types (status vs select, etc)

## 📚 Related Files

- Python scripts: `/Users/ahmadfaris/moltbot-workspace/scripts/tickets/*.py`
- Credentials: `/Users/ahmadfaris/moltbot-workspace/notion-credentials.json`
- Environment: `/Users/ahmadfaris/moltbot-workspace/.env`

## 🎓 Next Steps

1. Import workflow ke n8n instance
2. Update credential reference (notion_creds_main)
3. Activate workflow
4. Copy webhook URL
5. Test dengan curl atau Postman
6. Integrate dengan chat bot / monitoring tools

---

**Created:** 2026-01-30  
**Version:** 1.0  
**Author:** Dynamic workflow based on existing scripts
