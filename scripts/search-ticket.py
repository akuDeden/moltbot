#!/usr/bin/env python3
"""
Search for a specific ticket in Notion
Usage: python3 search-ticket.py "SEARCH_QUERY"
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

def search_ticket(notion, query):
    """Search for ticket by query"""
    try:
        # Search for pages containing the query
        response = notion.search(
            query=query,
            filter={
                "property": "object",
                "value": "page"
            },
            page_size=10
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

        return pages

    except Exception as e:
        print(f"❌ Error searching pages: {str(e)}")
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
    if len(sys.argv) < 2:
        print("Usage: python3 search-ticket.py 'SEARCH_QUERY'")
        print("Example: python3 search-ticket.py 'Invoice status issues'")
        sys.exit(1)

    query = sys.argv[1]

    # Load credentials
    creds = load_credentials()
    notion_token = creds.get("notion_token")

    if not notion_token:
        print("❌ Error: Notion token not configured")
        sys.exit(1)

    # Initialize Notion client
    notion = Client(auth=notion_token)

    print(f"🔍 Searching for: {query}\n")

    # Get tickets
    pages = search_ticket(notion, query)

    if not pages:
        print(f"❌ No tickets found matching: {query}")
        sys.exit(0)

    print(f"📋 FOUND ({len(pages)}):\n")

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
