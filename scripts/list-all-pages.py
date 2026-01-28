#!/usr/bin/env python3
"""
List all pages from Notion (no database filter)
Usage: python3 list-all-pages.py [limit]
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

def list_all_pages(notion, limit=20):
    """List all pages from Notion"""
    try:
        # Search for all pages
        response = notion.search(
            filter={
                "property": "object",
                "value": "page"
            },
            page_size=100
        )

        results = response.get("results", [])

        pages = []
        for result in results:
            # Extract page info
            title = ""
            properties = result.get("properties", {})

            # Try to get title from various property names
            for prop_name in ["Name", "Title", "Ticket", "Task", "Item"]:
                if prop_name in properties:
                    prop_data = properties[prop_name]
                    if prop_data.get("type") == "title":
                        title_data = prop_data.get("title", [])
                        if title_data:
                            title = title_data[0].get("plain_text", "")
                            break

            # Get status if exists
            status = ""
            for prop_name in ["Status", "State"]:
                if prop_name in properties:
                    prop_data = properties[prop_name]
                    if prop_data.get("type") == "status":
                        status_data = prop_data.get("status", {})
                        if status_data:
                            status = status_data.get("name", "")
                            break

            # Get Sprint if exists
            sprint = ""
            for prop_name in ["Sprint"]:
                if prop_name in properties:
                    prop_data = properties[prop_name]
                    if prop_data.get("type") == "select":
                        select_data = prop_data.get("select", {})
                        if select_data:
                            sprint = select_data.get("name", "")
                            break

            # Get parent info
            parent_info = ""
            parent = result.get("parent", {})
            if parent.get("type") == "database_id":
                parent_db = parent.get("database_id", "")
                parent_info = f"DB: {parent_db[:8]}..."

            # Get created time
            created_time = result.get("created_time", "")

            pages.append({
                "id": result["id"],
                "title": title or "Untitled",
                "status": status,
                "sprint": sprint,
                "parent": parent_info,
                "created": created_time,
                "url": result.get("url", "")
            })

        # Sort by created time (newest first)
        pages.sort(key=lambda x: x["created"], reverse=True)

        return pages[:limit]

    except Exception as e:
        print(f"❌ Error fetching pages: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

def format_date(date_str):
    """Format ISO date to readable format"""
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y, %H:%M")
    except:
        return date_str

def main():
    limit = 20
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            print("Usage: python3 list-all-pages.py [limit]")
            sys.exit(1)

    # Load credentials
    creds = load_credentials()
    notion_token = creds.get("notion_token")

    if not notion_token:
        print("❌ Error: Notion token not configured")
        sys.exit(1)

    # Initialize Notion client
    notion = Client(auth=notion_token)

    print(f"🔍 Fetching all pages...\n")

    # Get all pages
    pages = list_all_pages(notion, limit)

    if not pages:
        print("❌ No pages found")
        sys.exit(0)

    print(f"📋 ALL PAGES ({len(pages)}):\n")

    for i, page in enumerate(pages, 1):
        status_emoji = "🔴" if page["status"] in ["Open", "In Progress", "Todo"] else "✅"
        status_str = f" [{page['status']}]" if page['status'] else ""
        sprint_str = f" Sprint: {page['sprint']}" if page['sprint'] else ""

        print(f"{i}. {status_emoji} {page['title']}{status_str}{sprint_str}")
        print(f"   Parent: {page['parent']}")
        print(f"   Created: {format_date(page['created'])}")
        print(f"   URL: {page['url']}")
        print()

if __name__ == "__main__":
    main()
