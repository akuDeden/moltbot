# 🤖 Notion Database Reader untuk Clawbot/Moltbot

Script collection untuk membaca dan query Notion database yang dirancang khusus untuk AI agent (clawbot/moltbot) dalam membaca dan memproses tiket.

## 📁 File Structure

```
scripts/
├── notion_database_reader.py       # Core library untuk query Notion
├── list_all_pages.py               # List semua pages/databases
├── list_dev_tickets.py             # Query dev tickets
├── list_bug_tickets.py             # Query bug tickets  
├── clawbot_ticket_reader.py        # AI agent integration (full content)
├── NOTION_DATABASE_GUIDE.md        # Dokumentasi lengkap
├── setup_notion_scripts.sh         # Setup script
└── copy_to_clawd.sh                # Copy ke /Users/ahmadfaris/moltbot-workspace/scripts
```

## 🚀 Quick Start

### 1. Setup

```bash
# Set environment variable
export NOTION_TOKEN="secret_your_integration_token"

# Or copy ke folder target
chmod +x copy_to_clawd.sh
./copy_to_clawd.sh

cd /Users/ahmadfaris/moltbot-workspace/scripts
```

### 2. Basic Usage

```bash
# List semua databases
python3 list_all_pages.py --show-databases

# Query dev tickets
python3 list_dev_tickets.py

# Query specific database
python3 notion_database_reader.py \
  --database-id 482be0a206b044d99fff5798db2381e4

# Read ticket dengan full content (untuk AI agent)
python3 clawbot_ticket_reader.py \
  --database-id 482be0a206b044d99fff5798db2381e4 \
  --status "Ready for Review" \
  --output tickets_for_ai.json
```

## 🎯 Use Cases untuk Persona AI

### 1. **Auto Ticket Review**
Persona membaca tiket dan melakukan review otomatis:

```bash
# Get tickets ready for review
python3 clawbot_ticket_reader.py \
  --database-id 482be0a206b044d99fff5798db2381e4 \
  --status "Ready for Review" \
  --output review_queue.json

# AI agent process
# clawbot akan membaca review_queue.json
# Analyze ticket content
# Generate review report
```

### 2. **Daily Standup Report**
Generate daily summary dari tickets:

```bash
# Get all in-progress tickets
python3 list_dev_tickets.py \
  --status "In Progress" \
  --output daily_work.json

# AI generate summary
```

### 3. **Bug Monitoring**
Monitor critical bugs:

```bash
# Get high priority bugs
python3 list_bug_tickets.py \
  --status "Open" \
  --priority "Critical" \
  --output critical_bugs.json

# AI alert team
```

## 🗂️ Database Configuration

### Dev Tickets
- Database 1: `482be0a206b044d99fff5798db2381e4`
- Database 2: `32e29af7d7dd4df69310270de8830d1a`

### Bug Tickets
Set environment variable:
```bash
export BUG_DATABASE_ID="your_bug_database_id"
```

## 🔧 Advanced: AI Agent Integration

### Example: Clawbot Persona

```python
#!/usr/bin/env python3
"""
Clawbot Persona - Automated Ticket Review
"""

from clawbot_ticket_reader import ClawbotTicketReader
import os

def main():
    # Initialize
    token = os.getenv("NOTION_TOKEN")
    clawbot = ClawbotTicketReader(token)
    
    # Get tickets for review
    tickets = clawbot.get_tickets_for_review(
        database_id="482be0a206b044d99fff5798db2381e4",
        status="Ready for Review",
        limit=5
    )
    
    # Process each ticket
    for ticket in tickets:
        # Get full context
        context = clawbot.prepare_context_for_agent(ticket)
        
        # AI review here
        print(f"🤖 Reviewing: {ticket.get('Name')}")
        
        # Your AI model processes context
        # review = your_ai_model.analyze(context)
        
        # Post results back to Notion
        # ...

if __name__ == "__main__":
    main()
```

### Output Format Options

#### JSON Output (for programmatic processing)
```bash
python3 clawbot_ticket_reader.py \
  --database-id 482be0a206b044d99fff5798db2381e4 \
  --output tickets.json \
  --format json
```

#### Markdown Output (for AI context)
```bash
python3 clawbot_ticket_reader.py \
  --database-id 482be0a206b044d99fff5798db2381e4 \
  --output tickets_context.md \
  --format markdown
```

Markdown output includes:
- Ticket metadata (status, priority, assignee)
- Full ticket content in markdown
- Formatted untuk easy reading by AI

## 📊 Features

### Core Features
- ✅ Query Notion databases dengan filters
- ✅ Extract ticket properties (status, priority, tags, etc.)
- ✅ Read full ticket content (blocks to markdown)
- ✅ Support nested/children blocks
- ✅ Multiple database support
- ✅ Export to JSON/Markdown

### Filter Options
- Status filter
- Priority filter
- Tag/Label filter
- Title search
- Custom property filters
- Combine filters (AND/OR)

### AI Agent Features
- Full content extraction (properties + blocks)
- Formatted context untuk AI processing
- Batch processing support
- JSON/Markdown export
- Ready-to-use context strings

## 🔍 Examples

### 1. Show Database Schema
```bash
python3 notion_database_reader.py \
  --database-id 482be0a206b044d99fff5798db2381e4 \
  --show-schema
```

### 2. Filter by Multiple Conditions
```bash
# In Progress AND High Priority
python3 notion_database_reader.py \
  --database-id 482be0a206b044d99fff5798db2381e4 \
  --status "In Progress" \
  --tag "backend"
```

### 3. Get Single Ticket with Full Content
```bash
python3 clawbot_ticket_reader.py \
  --ticket-id abc123def456 \
  --show-context
```

### 4. Batch Export untuk AI
```bash
# Export all tickets yang perlu review
python3 clawbot_ticket_reader.py \
  --database-id 482be0a206b044d99fff5798db2381e4 \
  --status "Ready for Review" \
  --output ai_review_batch.md \
  --format markdown
```

## 🔐 Security

### Environment Variables
```bash
# Required
export NOTION_TOKEN="secret_xxxx"

# Optional
export BUG_DATABASE_ID="your_bug_db_id"
```

### Best Practices
- ❌ Jangan commit `.env` files
- ✅ Use environment variables
- ✅ Rotate tokens regularly
- ✅ Use least-privilege integration permissions

## 🛠️ Installation ke Target Directory

```bash
# Make copy script executable
chmod +x copy_to_clawd.sh

# Copy all files ke /Users/ahmadfaris/moltbot-workspace/scripts
./copy_to_clawd.sh

# Verify
ls -la /Users/ahmadfaris/moltbot-workspace/scripts/
```

Files yang akan di-copy:
- `notion_database_reader.py` - Core library
- `list_all_pages.py` - List pages
- `list_dev_tickets.py` - Dev tickets
- `list_bug_tickets.py` - Bug tickets
- `clawbot_ticket_reader.py` - AI integration
- `NOTION_DATABASE_GUIDE.md` - Full docs
- `setup_notion_scripts.sh` - Setup helper

## 📚 Documentation

Full documentation: `NOTION_DATABASE_GUIDE.md`

Topics covered:
- Detailed API reference
- Filter syntax and examples
- Integration patterns
- Troubleshooting guide
- Advanced use cases

## 🐛 Troubleshooting

### "NOTION_TOKEN not set"
```bash
export NOTION_TOKEN="your_token_here"
```

### "object not found"
- Database belum di-share dengan integration
- Check database ID

### "unauthorized"
- Token invalid atau expired
- Generate new token: https://www.notion.so/my-integrations

### No results
- Check filters
- Try without filters first
- Verify database has data

## 📞 Support

- Notion API Docs: https://developers.notion.com/
- Integration Setup: https://developers.notion.com/docs/getting-started
- Database Query API: https://developers.notion.com/reference/post-database-query

---

**Created for:** Clawbot/Moltbot AI Agent Persona  
**Version:** 1.0.0  
**Date:** January 28, 2026  
**Author:** Ahmad Faris

## 🎯 Next Steps

1. ✅ Copy scripts ke target directory
2. ✅ Set NOTION_TOKEN environment variable
3. ✅ Test connection: `python3 list_all_pages.py`
4. ✅ Query your databases
5. ✅ Integrate dengan AI agent/persona
6. ✅ Automate ticket reviews!

Happy automating! 🚀
