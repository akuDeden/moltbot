# Notion Database Query Scripts

Script-script untuk membaca dan query Notion database (untuk clawbot/moltbot persona).

## 📋 Prerequisites

1. **Notion Integration Token**
   - Buat integration di: https://www.notion.so/my-integrations
   - Copy Integration Token
   - Share database dengan integration Anda

2. **Python Dependencies**
   ```bash
   pip install requests
   ```

3. **Environment Setup**
   ```bash
   # Set environment variable
   export NOTION_TOKEN="your_notion_integration_token_here"
   
   # Or create .env file di folder scripts/
   echo "NOTION_TOKEN=your_token_here" > .env
   ```

## 🚀 Usage

### 1. List All Pages/Databases

Explore semua pages dan databases yang accessible:

```bash
# List all
python list_all_pages.py

# Search specific
python list_all_pages.py --search "dev ticket"

# Show only databases
python list_all_pages.py --show-databases

# Export to JSON
python list_all_pages.py --output all_pages.json
```

### 2. Query Specific Database (Generic)

Query database dengan berbagai filter:

```bash
# Basic query
python notion_database_reader.py --database-id 482be0a206b044d99fff5798db2381e4

# Filter by status
python notion_database_reader.py \
  --database-id 482be0a206b044d99fff5798db2381e4 \
  --status "In Progress"

# Search in title
python notion_database_reader.py \
  --database-id 482be0a206b044d99fff5798db2381e4 \
  --search "bug fix"

# Filter by tag
python notion_database_reader.py \
  --database-id 482be0a206b044d99fff5798db2381e4 \
  --tag "backend"

# Show database schema
python notion_database_reader.py \
  --database-id 482be0a206b044d99fff5798db2381e4 \
  --show-schema

# Export to JSON
python notion_database_reader.py \
  --database-id 482be0a206b044d99fff5798db2381e4 \
  --output dev_tickets.json
```

### 3. List Dev Tickets (Specific)

Script khusus untuk dev tickets dengan multiple database IDs:

```bash
# List all dev tickets dari semua databases
python list_dev_tickets.py

# Filter by status
python list_dev_tickets.py --status "To Do"

# Query specific database only
python list_dev_tickets.py --database-id 482be0a206b044d99fff5798db2381e4

# Export to JSON
python list_dev_tickets.py --output dev_tickets.json
```

**Configured Dev Database IDs:**
- `482be0a206b044d99fff5798db2381e4` (Dev ticket database 1)
- `32e29af7d7dd4df69310270de8830d1a` (Dev tiket database 2)

### 4. List Bug Tickets (Specific)

Script khusus untuk bug tickets:

```bash
# Set bug database ID
export BUG_DATABASE_ID="your_bug_database_id"

# List all bugs
python list_bug_tickets.py

# Filter by status
python list_bug_tickets.py --status "Open"

# Filter by priority
python list_bug_tickets.py --priority "High"

# Combine filters
python list_bug_tickets.py --status "Open" --priority "Critical"

# Export to JSON
python list_bug_tickets.py --output bug_tickets.json
```

## 🔧 Configuration

### Database IDs

Database IDs yang sudah dikonfigurasi:

**Dev Tickets:**
- Database 1: `482be0a206b044d99fff5798db2381e4`
- Database 2: `32e29af7d7dd4df69310270de8830d1a`

**Bug Tickets:**
- Set via environment: `BUG_DATABASE_ID=your_id_here`

### Environment Variables

```bash
# Required
export NOTION_TOKEN="secret_xxxxxxxxxxxx"

# Optional (untuk bug tickets)
export BUG_DATABASE_ID="your_bug_database_id"
```

## 📦 Files Overview

| File | Description |
|------|-------------|
| `notion_database_reader.py` | Core library untuk query Notion database |
| `list_all_pages.py` | List semua pages/databases di workspace |
| `list_dev_tickets.py` | Query dev tickets dari multiple databases |
| `list_bug_tickets.py` | Query bug tickets dengan priority filter |

## 🎯 Use Cases untuk Clawbot/Moltbot

### 1. Read Tickets untuk Review
```bash
# Get all "In Progress" tickets
python list_dev_tickets.py --status "In Progress" --output current_work.json

# Process dengan clawbot
# clawbot akan membaca current_work.json dan analyze
```

### 2. Monitor Bug Status
```bash
# Get high priority open bugs
python list_bug_tickets.py --status "Open" --priority "High" --output critical_bugs.json

# Alert atau notify team
```

### 3. Daily Standup Report
```bash
# Get yesterday's tickets
python notion_database_reader.py \
  --database-id 482be0a206b044d99fff5798db2381e4 \
  --output daily_report.json

# Generate summary dengan AI
```

## 🔍 Advanced Filtering

### Custom Filters (dalam Python code)

```python
from notion_database_reader import NotionDatabaseReader

reader = NotionDatabaseReader(notion_token)

# Complex AND filter
filter_conditions = {
    "and": [
        {
            "property": "Status",
            "status": {"equals": "In Progress"}
        },
        {
            "property": "Priority",
            "select": {"equals": "High"}
        },
        {
            "property": "Assignee",
            "people": {"is_not_empty": True}
        }
    ]
}

tickets = reader.query_database(
    database_id="your_db_id",
    filter_conditions=filter_conditions
)
```

### Sort Results

```python
# Sort by created time (newest first)
sorts = [
    {
        "timestamp": "created_time",
        "direction": "descending"
    }
]

tickets = reader.query_database(
    database_id="your_db_id",
    sorts=sorts
)
```

## 🛠️ Integration dengan Clawbot

### Example: Auto-Review Pipeline

```python
#!/usr/bin/env python3
"""
Clawbot Auto-Review Pipeline
"""

from notion_database_reader import NotionDatabaseReader
import os

def main():
    # Init reader
    reader = NotionDatabaseReader(os.getenv("NOTION_TOKEN"))
    
    # Get tickets yang perlu review
    filter_conditions = {
        "property": "Status",
        "status": {"equals": "Ready for Review"}
    }
    
    tickets = reader.query_database(
        database_id="482be0a206b044d99fff5798db2381e4",
        filter_conditions=filter_conditions
    )
    
    # Process each ticket
    for page in tickets:
        ticket = reader.extract_page_properties(page)
        
        print(f"🤖 Reviewing: {ticket.get('Name')}")
        print(f"   URL: {ticket.get('url')}")
        
        # Trigger clawbot review
        # review_result = clawbot.review_ticket(ticket)
        
        # Update Notion with review results
        # ...

if __name__ == "__main__":
    main()
```

## 📚 API Reference

### NotionDatabaseReader Class

```python
reader = NotionDatabaseReader(
    notion_token="your_token",
    notion_version="2022-06-28"  # optional
)
```

**Methods:**

- `query_database(database_id, filter_conditions, sorts, page_size)` - Query database
- `get_database_info(database_id)` - Get database schema
- `extract_page_properties(page)` - Extract properties ke format readable
- `format_ticket_summary(ticket)` - Format ticket untuk display

### Filter Examples

**Status Filter:**
```python
{
    "property": "Status",
    "status": {"equals": "In Progress"}
}
```

**Priority Filter:**
```python
{
    "property": "Priority",
    "select": {"equals": "High"}
}
```

**Tag Filter:**
```python
{
    "property": "Tags",
    "multi_select": {"contains": "backend"}
}
```

**Title Search:**
```python
{
    "property": "Name",
    "title": {"contains": "bug fix"}
}
```

**Date Filter:**
```python
{
    "property": "Due Date",
    "date": {"on_or_after": "2026-01-01"}
}
```

## 🐛 Troubleshooting

### Error: "NOTION_TOKEN not set"
```bash
export NOTION_TOKEN="secret_your_token_here"
```

### Error: "object not found"
- Pastikan database sudah di-share dengan integration
- Check database ID sudah benar

### Error: "unauthorized"
- Token mungkin salah atau expired
- Generate token baru di https://www.notion.so/my-integrations

### No results returned
- Check filter conditions
- Pastikan database ada isinya
- Coba tanpa filter dulu

## 📝 Notes

- Maximum 100 results per query (bisa paging jika lebih)
- Notion API rate limit: ~3 requests/second
- Token harus punya access ke database yang di-query
- Database harus di-share dengan integration terlebih dahulu

## 🔗 Links

- [Notion API Documentation](https://developers.notion.com/)
- [Notion Integration Guide](https://developers.notion.com/docs/getting-started)
- [Database Query API](https://developers.notion.com/reference/post-database-query)

---

**Created for:** Clawbot/Moltbot Persona  
**Last Updated:** January 28, 2026
