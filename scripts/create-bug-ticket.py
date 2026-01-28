#!/usr/bin/env python3
"""
Create bug ticket in Notion
Usage: python3 create-bug-ticket.py "TITLE" "DESCRIPTION" [SEVERITY]
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

CREDENTIALS_FILE = "/Users/ahmadfaris/moltbot-workspace/notion-credentials.json"

def load_credentials():
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: {CREDENTIALS_FILE} not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: {CREDENTIALS_FILE} is not valid JSON")
        sys.exit(1)

def create_bug_ticket(notion, database_id, title, description, severity="Medium"):
    """Create a new bug ticket in Notion"""
    try:
        # First, try to get database schema to see available properties
        try:
            db_info = notion.databases.retrieve(database_id=database_id)
            print(f"📋 Database: {db_info.get('title', [{}])[0].get('plain_text', 'Unknown')}")
        except:
            pass
        
        # Create page with minimal properties - just title
        # Notion will use default database schema
        properties = {
            "title": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        }
        
        # Prepare page content (description as blocks)
        children = []
        
        # Add severity callout
        children.append({
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": f"Severity: {severity}"
                        }
                    }
                ],
                "icon": {
                    "emoji": "⚠️"
                },
                "color": "red_background" if severity in ["Critical", "High"] else "yellow_background"
            }
        })
        
        # Add description as paragraph
        if description:
            children.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Description"
                            }
                        }
                    ]
                }
            })
            
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": description
                            }
                        }
                    ]
                }
            })
        
        # Add metadata section
        children.append({
            "object": "block",
            "type": "divider",
            "divider": {}
        })
        
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": f"📅 Created: {datetime.now().strftime('%d %b %Y, %H:%M')}\n🤖 Created by: WhatsApp Bot",
                            "link": None
                        }
                    }
                ]
            }
        })
        
        # Create the page
        response = notion.pages.create(
            parent={"database_id": database_id},
            properties=properties,
            children=children
        )
        
        return {
            "success": True,
            "page_id": response["id"],
            "url": response["url"]
        }
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error creating ticket: {error_msg}")
        
        # Try to provide helpful error message
        if "is not a property" in error_msg:
            print("\n💡 Tip: Database schema mismatch. The database might have custom properties.")
            print("   The ticket will be created as a simple page with title and description.")
        
        import traceback
        traceback.print_exc()
        
        return {
            "success": False,
            "error": error_msg
        }

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 create-bug-ticket.py 'TITLE' 'DESCRIPTION' [SEVERITY]")
        print("Example: python3 create-bug-ticket.py 'User cannot login' 'Users report unable to login to the app' 'High'")
        print("\nSeverity options: Critical, High, Medium, Low (default: Medium)")
        sys.exit(1)
    
    title = sys.argv[1]
    description = sys.argv[2]
    severity = sys.argv[3] if len(sys.argv) > 3 else "Medium"
    
    # Load credentials
    creds = load_credentials()
    notion_token = creds.get("notion_token")
    database_bug = creds.get("database_bug")
    
    if not notion_token:
        print("❌ Error: Notion token not configured")
        sys.exit(1)
    
    if not database_bug:
        print("❌ Error: Bug database ID not configured")
        sys.exit(1)
    
    # Initialize Notion client
    notion = Client(auth=notion_token)
    
    print(f"🐛 Creating bug ticket...")
    print(f"   Title: {title}")
    print(f"   Severity: {severity}")
    print()
    
    # Create ticket
    result = create_bug_ticket(notion, database_bug, title, description, severity)
    
    if result["success"]:
        print(f"✅ Bug ticket berhasil dibuat!")
        print(f"   Title: {title}")
        print(f"   Severity: {severity}")
        print(f"   URL: {result['url']}")
        print()
        print(f"📋 Page ID: {result['page_id']}")
    else:
        print(f"❌ Failed to create ticket")
        print(f"   Error: {result.get('error', 'Unknown error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
