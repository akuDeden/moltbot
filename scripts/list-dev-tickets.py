#!/usr/bin/env python3
"""
List dev/sprint tickets from Notion
Usage: python3 list-dev-tickets.py [limit]
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

def list_dev_tickets(notion, database_id, limit=20):
    """List dev tickets from Notion database"""
    try:
        # Search for pages in the dev database
        response = notion.search(
            filter={
                "property": "object",
                "value": "page"
            },
            page_size=100
        )

        results = response.get("results", [])

        # Filter to only pages in dev database
        dev_tickets = []
        target_db = database_id.replace("-", "")

        for result in results:
            if result.get("parent", {}).get("type") == "database_id":
                parent_db = result.get("parent", {}).get("database_id", "").replace("-", "")

                if parent_db == target_db:
                    # Extract ticket info
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

                    # Get created time
                    created_time = result.get("created_time", "")

                    dev_tickets.append({
                        "id": result["id"],
                        "title": title or "Untitled",
                        "status": status,
                        "sprint": sprint,
                        "created": created_time,
                        "url": result.get("url", "")
                    })

        # Sort by created time (newest first)
        dev_tickets.sort(key=lambda x: x["created"], reverse=True)

        return dev_tickets[:limit]

    except Exception as e:
        print(f"❌ Error fetching tickets: {str(e)}")
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
            print("Usage: python3 list-dev-tickets.py [limit]")
            sys.exit(1)

    # Load credentials
    creds = load_credentials()
    notion_token = creds.get("notion_token")
    database_dev = creds.get("database_dev")

    if not notion_token:
        print("❌ Error: Notion token not configured")
        sys.exit(1)

    if not database_dev:
        print("❌ Error: Dev database ID not configured")
        sys.exit(1)

    # Initialize Notion client
    notion = Client(auth=notion_token)

    print(f"🔍 Fetching dev tickets...\n")

    # Get dev tickets
    tickets = list_dev_tickets(notion, database_dev, limit)

    if not tickets:
        print("❌ No dev tickets found")
        sys.exit(0)

    print(f"📋 DEV/SPRINT TICKETS ({len(tickets)}):\n")

    # Group by sprint if possible
    sprints = {}
    for ticket in tickets:
        sprint_name = ticket['sprint'] or "No Sprint"
        if sprint_name not in sprints:
            sprints[sprint_name] = []
        sprints[sprint_name].append(ticket)

    # Print tickets grouped by sprint
    for sprint_name, sprint_tickets in sprints.items():
        print(f"🏃 {sprint_name}:")
        for i, ticket in enumerate(sprint_tickets, 1):
            status_emoji = "🔴" if ticket["status"] in ["Open", "In Progress", "Todo"] else "✅"
            status_str = f" [{ticket['status']}]" if ticket['status'] else ""

            print(f"   {i}. {status_emoji} {ticket['title']}{status_str}")
            print(f"      Created: {format_date(ticket['created'])}")
            print(f"      URL: {ticket['url']}")
        print()

if __name__ == "__main__":
    main()
