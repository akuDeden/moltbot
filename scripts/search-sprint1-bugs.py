#!/usr/bin/env python3
"""
Search for bug tickets in Sprint 1
Usage: python3 search-sprint1-bugs.py
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

def search_sprint1_bugs(notion):
    """Search for bug tickets with 'Sprint 1'"""
    try:
        # Search for pages containing both "Sprint 1" and "bug"
        response = notion.search(
            query="Sprint 1",
            filter={
                "property": "object",
                "value": "page"
            },
            page_size=100
        )

        results = response.get("results", [])

        bug_tickets = []
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

            # Check if it's a bug ticket (contains Bug or hotfix in title)
            title_lower = title.lower() if title else ""
            is_bug = "bug" in title_lower or "hotfix" in title_lower

            if not is_bug:
                continue

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

            # Get created time
            created_time = result.get("created_time", "")

            bug_tickets.append({
                "id": result["id"],
                "title": title or "Untitled",
                "status": status,
                "sprint": sprint,
                "created": created_time,
                "url": result.get("url", "")
            })

        # Sort by created time (newest first)
        bug_tickets.sort(key=lambda x: x["created"], reverse=True)

        return bug_tickets

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
    # Load credentials
    creds = load_credentials()
    notion_token = creds.get("notion_token")

    if not notion_token:
        print("❌ Error: Notion token not configured")
        sys.exit(1)

    # Initialize Notion client
    notion = Client(auth=notion_token)

    print(f"🔍 Searching for Bug tickets in Sprint 1...\n")

    # Get bug tickets
    bug_tickets = search_sprint1_bugs(notion)

    if not bug_tickets:
        print("❌ No bug tickets found in Sprint 1")
        sys.exit(0)

    print(f"🐛 SPRINT 1 BUG TICKETS ({len(bug_tickets)}):\n")

    for i, ticket in enumerate(bug_tickets, 1):
        status_emoji = "🔴" if ticket["status"] in ["Open", "In Progress", "Todo"] else "✅"
        status_str = f" [{ticket['status']}]" if ticket['status'] else ""
        sprint_str = f" Sprint: {ticket['sprint']}" if ticket['sprint'] else ""

        print(f"{i}. {status_emoji} {ticket['title']}{status_str}{sprint_str}")
        print(f"   Created: {format_date(ticket['created'])}")
        print(f"   URL: {ticket['url']}")
        print()

if __name__ == "__main__":
    main()
