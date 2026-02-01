# N8N Dynamic Ticket Query - Architecture

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Requests                           │
├─────────────────────────────────────────────────────────────────┤
│  Chat Bot  │  CLI  │  Web Dashboard  │  Cron Jobs  │  API Call │
└──────┬───────┬──────────────┬──────────────┬───────────┬────────┘
       │       │               │              │           │
       └───────┴───────────────┴──────────────┴───────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   N8N Webhook Trigger   │
                    │  POST /query-tickets    │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   Parse Request         │
                    │  - Extract parameters   │
                    │  - Build filters        │
                    │  - Set defaults         │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   Query Notion API      │
                    │  - Apply filters        │
                    │  - Pagination           │
                    │  - Sort results         │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Extract & Filter       │
                    │  - Parse properties     │
                    │  - Keyword search       │
                    │  - Structure data       │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   Format Response       │
                    │  - Group by status      │
                    │  - Generate text        │
                    │  - Build JSON           │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   Return Response       │
                    │  - HTTP 200 (success)   │
                    │  - HTTP 500 (error)     │
                    └─────────────────────────┘
```

## 📊 Data Flow

```
User Input:
{
  "sprint": "Sprint 2",
  "status": "In Progress",
  "keywords": "sales"
}
         │
         ▼
Parse & Build Filters:
{
  "filter": {
    "and": [
      {"property": "Sprint", "select": {"equals": "Sprint 2"}},
      {"property": "Status", "status": {"equals": "In Progress"}}
    ]
  }
}
         │
         ▼
Notion API Query:
→ Apply filters
→ Get results (with pagination)
→ Return pages
         │
         ▼
Extract Properties:
[
  {
    "title": "Implement Sales API",
    "status": "In Progress",
    "sprint": "Sprint 2",
    "assignee": "Ahmad",
    ...
  },
  ...
]
         │
         ▼
Filter by Keywords:
→ Check if "sales" in title
→ Keep matching tickets
         │
         ▼
Format Output:
{
  "success": true,
  "count": 3,
  "message": "📊 *Hasil Query Ticket*\n...",
  "data": {...},
  "formatted": {...}
}
         │
         ▼
Return to User
```

## 🔄 Integration Patterns

### Pattern 1: Chat Bot Command

```
User: "cari tiket sprint 2"
  │
  ▼
Chat Bot (Moltbot/Telegram/Discord)
  │
  ▼
Parse Command:
  - Action: query tickets
  - Param: sprint = "Sprint 2"
  │
  ▼
Execute Script:
  ./scripts/tickets/n8n-tickets.sh sprint "Sprint 2"
  │
  ▼
Script → HTTP POST → N8N Webhook
  │
  ▼
N8N → Notion API → Process → Format
  │
  ▼
Return formatted text
  │
  ▼
Bot → Send reply to user
```

### Pattern 2: Automated Report

```
Cron Job (Daily 9 AM)
  │
  ▼
Execute:
  python3 n8n-query-tickets.py --sprint "Sprint 2"
  │
  ▼
N8N Workflow → Query → Format
  │
  ▼
Save to file OR Send email/Slack
```

### Pattern 3: Dashboard Widget

```
Frontend (React/Vue)
  │
  ▼
API Call:
  fetch('/webhook/query-tickets', {
    body: JSON.stringify({sprint: 'Sprint 2'})
  })
  │
  ▼
N8N → Process → Return JSON
  │
  ▼
Frontend renders tickets
```

## 🧩 Component Breakdown

### 1. Webhook Trigger Node
- **Purpose:** Entry point for HTTP requests
- **Config:** POST endpoint, returns response
- **Output:** Raw request data (body, query, headers)

### 2. Parse Request Node (Code)
- **Purpose:** Extract & validate parameters
- **Input:** HTTP request data
- **Processing:**
  - Extract from body or query string
  - Apply defaults
  - Build Notion API filter object
- **Output:** Parsed params + filter object

### 3. Get Notion Tickets Node
- **Purpose:** Query Notion database
- **Input:** Database ID, filter, sort, limit
- **Processing:** Notion API call with pagination
- **Output:** Array of Notion pages

### 4. Extract & Filter Node (Code)
- **Purpose:** Parse Notion properties
- **Input:** Raw Notion pages
- **Processing:**
  - Extract title, status, sprint, assignee, etc
  - Apply keyword search filter
  - Structure data
- **Output:** Clean ticket objects

### 5. Format Response Node (Code)
- **Purpose:** Generate user-friendly output
- **Input:** Ticket array
- **Processing:**
  - Group by status
  - Generate formatted text
  - Build complete response
- **Output:** Formatted message + JSON data

### 6. Respond Node
- **Purpose:** Return HTTP response
- **Input:** Formatted data
- **Output:** HTTP 200 with JSON

### 7. Error Handler Node (Code)
- **Purpose:** Catch and format errors
- **Input:** Error from any node
- **Processing:** Format error message
- **Output:** Error object

### 8. Respond Error Node
- **Purpose:** Return error response
- **Input:** Error object
- **Output:** HTTP 500 with error JSON

## 🎨 Output Formats

### Format 1: Text (Default)
```
📊 *Hasil Query Ticket*

Total: 5 ticket
Sprint: Sprint 2

---

*In Progress* (3):

1. *Implement Sales API*
   Sprint: Sprint 2
   Assignee: Ahmad
   Priority: High
   🔗 https://notion.so/...
```

### Format 2: Compact
```
📊 Found 5 ticket(s)

1. Implement Sales API
   Status: In Progress | Sprint: Sprint 2 | Assignee: Ahmad
   🔗 https://notion.so/...
```

### Format 3: JSON
```json
{
  "success": true,
  "count": 5,
  "params": {...},
  "tickets": [
    {
      "id": "...",
      "title": "Implement Sales API",
      "status": "In Progress",
      ...
    }
  ],
  "formatted": {...}
}
```

### Format 4: URLs
```
https://notion.so/ticket-1
https://notion.so/ticket-2
https://notion.so/ticket-3
```

## 🔐 Security Layers

```
┌─────────────────────────────────┐
│   Rate Limiting (n8n)           │ ← Prevent abuse
├─────────────────────────────────┤
│   API Key Auth (optional)       │ ← Authenticate requests
├─────────────────────────────────┤
│   Input Validation              │ ← Sanitize params
├─────────────────────────────────┤
│   Notion API Token              │ ← Secure credentials
├─────────────────────────────────┤
│   Database Access Control       │ ← Notion permissions
└─────────────────────────────────┘
```

## 📈 Performance Considerations

### Optimization Points

1. **Limit Results**
   - Default: 100
   - Max: 100
   - Use specific filters to reduce dataset

2. **Filter Early**
   - Apply Notion API filters (fast)
   - Keyword search after (post-processing)

3. **Caching** (Optional)
   - Cache results for X minutes
   - Invalidate on updates
   - Reduces API calls

4. **Pagination**
   - Notion API handles automatically
   - N8N node supports pagination
   - No manual cursor management

## 🚀 Scaling Strategy

### Small Scale (Current)
- Direct webhook calls
- Single n8n instance
- ~10-100 requests/day

### Medium Scale
- Load balancer
- Multiple n8n instances
- Redis caching
- ~100-1000 requests/day

### Large Scale
- API Gateway
- Queue system (RabbitMQ/Redis)
- Distributed caching
- CDN for static responses
- ~1000+ requests/day

## 🔧 Maintenance

### Regular Tasks
1. Monitor n8n execution logs
2. Check Notion API rate limits
3. Update filters as schema changes
4. Review and optimize slow queries
5. Clean up old cached data

### Updates
1. Test in dev environment
2. Backup workflow config
3. Deploy to production
4. Monitor for errors
5. Rollback if needed

---

**Visual Guides:** See diagrams for system architecture and data flow patterns.
