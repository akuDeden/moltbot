#!/usr/bin/env python3
"""
Verify ticket properties directly from Notion API
Usage: python3 verify-ticket.py "<ticket_id>"
"""
import sys
import json
import httpx
from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 verify-ticket.py <ticket_id>")
        print("Example: python3 verify-ticket.py 2f1c6dc1a8eb80b4a962e0478fa1c945")
        sys.exit(1)
    
    ticket_id = sys.argv[1].replace('-', '')
    token = os.getenv('NOTION_TOKEN')
    
    if not token:
        print("❌ NOTION_TOKEN not found in .env")
        sys.exit(1)
    
    # Query page directly
    headers = {
        'Authorization': f'Bearer {token}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }
    
    url = f'https://api.notion.com/v1/pages/{ticket_id}'
    
    print(f"🔍 Fetching ticket: {ticket_id}")
    print(f"   URL: {url}")
    print()
    
    response = httpx.get(url, headers=headers, timeout=30.0)
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    data = response.json()
    props = data.get('properties', {})
    
    # Extract key properties
    print("=" * 70)
    print("TICKET PROPERTIES (Direct from Notion API)")
    print("=" * 70)
    print()
    
    # Title
    for key, prop in props.items():
        if prop.get('type') == 'title':
            title_list = prop.get('title', [])
            if title_list:
                title = title_list[0].get('plain_text', 'No title')
                print(f"📝 Title: {title}")
    
    # Status
    if 'Status' in props:
        status_prop = props['Status']
        if status_prop.get('type') == 'status':
            status = status_prop.get('status', {}).get('name', 'No status')
            print(f"📊 Status: {status}")
    
    # Assignee
    if 'Assignee' in props:
        assignee_prop = props['Assignee']
        if assignee_prop.get('type') == 'people':
            people = assignee_prop.get('people', [])
            if people:
                names = [p.get('name', 'Unknown') for p in people]
                print(f"👤 Assignee: {', '.join(names)}")
            else:
                print(f"👤 Assignee: (unassigned)")
    
    # Sprint
    if 'Sprint' in props:
        sprint_prop = props['Sprint']
        if sprint_prop.get('type') == 'relation':
            relations = sprint_prop.get('relation', [])
            if relations:
                print(f"🏃 Sprint: {len(relations)} relation(s)")
            else:
                print(f"🏃 Sprint: No sprint")
    
    print()
    print("=" * 70)
    print("RAW PROPERTIES (for debugging)")
    print("=" * 70)
    print(json.dumps(props, indent=2))

if __name__ == '__main__':
    main()
