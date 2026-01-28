#!/usr/bin/env python3
"""
Review ticket and write result to Notion
Auto-detects database based on ticket type:
- Development/Task tickets → database_dev
- Bug tickets → database_bug

Usage: python3 review-ticket-notion.py "TICKET_ID" "REVIEW_TYPE" "REVIEW_CONTENT"
"""
import sys
import json
from datetime import datetime

try:
    from notion_client import Client
except ImportError:
    print("❌ Error: notion-client not installed")
    print("Install with: pip install notion-client")
    sys.exit(1)

# Load Notion credentials
CREDENTIALS_FILE = "/Users/ahmadfaris/moltbot-workspace/notion-credentials.json"

def load_credentials():
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: {CREDENTIALS_FILE} not found")
        print("Create it with your Notion token and database IDs")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: {CREDENTIALS_FILE} is not valid JSON")
        sys.exit(1)

def detect_ticket_type(ticket_id):
    """Detect if ticket is bug or dev/task based on ID pattern"""
    ticket_lower = ticket_id.lower()
    
    # Bug indicators
    bug_keywords = ['bug', 'hotfix', 'issue', 'defect']
    if any(keyword in ticket_lower for keyword in bug_keywords):
        return 'bug'
    
    # Default to dev/task
    return 'dev'

def find_ticket_page(notion, database_id, ticket_id):
    """Find Notion page by ticket ID using Search API"""
    try:
        # Use search API to find the ticket
        response = notion.search(
            query=ticket_id,
            filter={
                "property": "object",
                "value": "page"
            }
        )
        
        results = response.get("results", [])
        
        # Filter results to match database_id if provided
        for result in results:
            # Check if page is in the target database
            if result.get("parent", {}).get("type") == "database_id":
                parent_db = result.get("parent", {}).get("database_id", "").replace("-", "")
                target_db = database_id.replace("-", "")
                
                if parent_db == target_db:
                    return result["id"]
        
        # If not found in specific database, return first match
        if results:
            return results[0]["id"]
            
        return None
        
    except Exception as e:
        print(f"❌ Error searching for ticket: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def update_notion_page(notion, page_id, review_type, review_content):
    """Update Notion page with review - adds comment instead of modifying properties"""
    try:
        # Instead of updating properties, add a comment/block to the page
        # This is more flexible and works regardless of database schema
        
        notion.comments.create(
            parent={"page_id": page_id},
            rich_text=[
                {
                    "type": "text",
                    "text": {
                        "content": f"[{review_type}] {review_content}\n\nReviewed by Bot on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                    }
                }
            ]
        )
        
        return True
        
    except Exception as e:
        # If comments fail, try adding a block to the page content
        try:
            notion.blocks.children.append(
                block_id=page_id,
                children=[
                    {
                        "object": "block",
                        "type": "callout",
                        "callout": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": f"✅ {review_type}: {review_content}"
                                    }
                                }
                            ],
                            "icon": {
                                "emoji": "✅"
                            },
                            "color": "green_background"
                        }
                    }
                ]
            )
            return True
        except Exception as e2:
            print(f"❌ Error updating page: {str(e2)}")
            return False

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 review-ticket-notion.py 'TICKET_ID' 'REVIEW_TYPE' 'REVIEW_CONTENT'")
        print("Example: python3 review-ticket-notion.py 'TECH-123' 'UAT' 'Passed all test cases'")
        print("\nDatabase routing:")
        print("  - Dev/Task tickets → database_dev")
        print("  - Bug tickets → database_bug")
        sys.exit(1)
    
    ticket_id = sys.argv[1]
    review_type = sys.argv[2]
    review_content = sys.argv[3]
    
    # Load credentials
    creds = load_credentials()
    notion_token = creds.get("notion_token")
    
    if not notion_token or notion_token == "YOUR_NOTION_INTEGRATION_TOKEN_HERE":
        print("❌ Error: Notion token not configured")
        print(f"Edit {CREDENTIALS_FILE} and add your Notion integration token")
        sys.exit(1)
    
    # Detect ticket type and select database
    ticket_type = detect_ticket_type(ticket_id)
    
    if ticket_type == 'bug':
        database_id = creds.get("database_bug")
        db_name = "Bug Database"
    else:
        database_id = creds.get("database_dev")
        db_name = "Dev/Task Database"
    
    if not database_id:
        print(f"❌ Error: Database ID not configured for {ticket_type} tickets")
        print(f"Edit {CREDENTIALS_FILE} and add database_{ticket_type}")
        sys.exit(1)
    
    # Initialize Notion client
    notion = Client(auth=notion_token)
    
    print(f"🔍 Searching for ticket: {ticket_id}")
    print(f"📂 Database: {db_name} ({ticket_type})")
    
    # Find the ticket page
    page_id = find_ticket_page(notion, database_id, ticket_id)
    
    if not page_id:
        print(f"❌ Ticket not found: {ticket_id}")
        print(f"Make sure the ticket exists in {db_name}")
        sys.exit(1)
    
    print(f"✅ Found ticket page")
    print(f"📝 Updating review: {review_type}")
    
    # Update the page
    success = update_notion_page(notion, page_id, review_type, review_content)
    
    if success:
        print(f"✅ Review berhasil ditulis ke Notion!")
        print(f"   Ticket: {ticket_id}")
        print(f"   Database: {db_name}")
        print(f"   Type: {review_type}")
        print(f"   Content: {review_content[:50]}...")
    else:
        print("❌ Failed to update Notion page")
        sys.exit(1)

if __name__ == "__main__":
    main()
