#!/usr/bin/env python3
"""
List recent bug tickets from Notion
Usage: python3 list-bug-tickets.py [limit]
"""
import sys
import json
import requests
from datetime import datetime

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

def query_database(notion_token, database_id, page_size=100):
    """Query Notion Database menggunakan REST API"""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    payload = {
        "page_size": page_size,
        "sorts": [
            {
                "timestamp": "created_time",
                "direction": "descending"
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"❌ Error querying database: {str(e)}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return []

def extract_title(properties):
    """Extract title dari page properties"""
    # Try common property names for title
    for prop_name in ["Bug name", "Name", "Title", "Ticket", "Task", "title"]:
        if prop_name in properties:
            prop_data = properties[prop_name]
            if prop_data.get("type") == "title" and prop_data.get("title"):
                titles = prop_data["title"]
                if titles and len(titles) > 0:
                    return titles[0].get("plain_text", "Untitled")
    return "Untitled"

def extract_status(properties):
    """Extract status dari page properties"""
    # Try common property names for status
    for prop_name in ["Dev Status", "Bug Status", "Status", "State", "status"]:
        if prop_name in properties:
            prop_data = properties[prop_name]
            if prop_data.get("type") == "status" and prop_data.get("status"):
                return prop_data["status"].get("name", "")
            elif prop_data.get("type") == "select" and prop_data.get("select"):
                return prop_data["select"].get("name", "")
            elif prop_data.get("type") == "rollup" and prop_data.get("rollup"):
                # Handle rollup properties
                rollup_data = prop_data["rollup"]
                if rollup_data.get("type") == "array" and rollup_data.get("array"):
                    arr = rollup_data["array"]
                    if arr and len(arr) > 0 and arr[0].get("status"):
                        return arr[0]["status"].get("name", "")
    return ""

def extract_severity(properties):
    """Extract severity dari page properties"""
    if "Severity" in properties:
        prop_data = properties["Severity"]
        if prop_data.get("type") == "select" and prop_data.get("select"):
            return prop_data["select"].get("name", "")
    return ""

def list_bug_tickets(notion_token, database_id, limit=5):
    """List recent bug tickets from Notion database"""
    results = query_database(notion_token, database_id, page_size=limit)
    
    bug_tickets = []
    for result in results:
        properties = result.get("properties", {})
        
        title = extract_title(properties)
        status = extract_status(properties)
        severity = extract_severity(properties)
        created_time = result.get("created_time", "")
        url = result.get("url", "")
        
        bug_tickets.append({
            "id": result["id"],
            "title": title,
            "status": status,
            "severity": severity,
            "created": created_time,
            "url": url
        })
    
    return bug_tickets

def format_date(date_str):
    """Format ISO date to readable format"""
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y, %H:%M")
    except:
        return date_str

def main():
    limit = 5
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            print("Usage: python3 list-bug-tickets.py [limit]")
            sys.exit(1)
    
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
    
    print(f"🔍 Fetching {limit} recent bug tickets...\n")
    
    # Get bug tickets
    tickets = list_bug_tickets(notion_token, database_bug, limit)
    
    if not tickets:
        print("❌ No bug tickets found")
        sys.exit(0)
    
    print(f"🐛 RECENT BUG TICKETS ({len(tickets)}):\n")
    
    for i, ticket in enumerate(tickets, 1):
        # Status emoji based on status
        status_emoji = "🔴" if ticket["status"] in ["Open", "In Progress", "Todo", "To Do", "Backlog"] else "✅"
        
        # Severity emoji
        severity_map = {
            "Critical": "🔥",
            "High": "⚠️",
            "Medium": "⚡",
            "Low": "💡"
        }
        severity_emoji = severity_map.get(ticket.get("severity", ""), "")
        
        # Build display string
        status_str = f" [{ticket['status']}]" if ticket['status'] else ""
        severity_str = f" {severity_emoji}{ticket['severity']}" if ticket.get('severity') else ""
        
        print(f"{i}. {status_emoji} {ticket['title']}{status_str}{severity_str}")
        print(f"   Created: {format_date(ticket['created'])}")
        print(f"   URL: {ticket['url']}")
        print()

if __name__ == "__main__":
    main()
