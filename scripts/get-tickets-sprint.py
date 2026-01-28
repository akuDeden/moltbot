#!/usr/bin/env python3
"""
Get tickets from database_dev filtered by sprint using raw HTTP
Usage: python3 get-tickets-sprint.py [sprint_number]
Example: python3 get-tickets-sprint.py 2
"""
import sys
import json
import httpx
import os

CREDENTIALS_FILE = os.environ.get(
    'NOTION_CREDENTIALS_FILE',
    os.path.expanduser('~/moltbot-workspace/notion-credentials.json')
)

def load_credentials():
    with open(CREDENTIALS_FILE, 'r') as f:
        return json.load(f)

def query_database_with_filter(token, db_id, filter_obj=None, api_version='2022-06-28'):
    """Query Notion database with filter using raw HTTP with pagination"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Notion-Version': api_version,
        'Content-Type': 'application/json'
    }
    
    url = f'https://api.notion.com/v1/databases/{db_id}/query'
    
    all_results = []
    has_more = True
    start_cursor = None
    
    while has_more:
        body = {}
        if filter_obj:
            body['filter'] = filter_obj
        if start_cursor:
            body['start_cursor'] = start_cursor
        
        response = httpx.post(url, headers=headers, json=body, timeout=30.0)
        
        if response.status_code == 200:
            data = response.json()
            all_results.extend(data.get('results', []))
            has_more = data.get('has_more', False)
            start_cursor = data.get('next_cursor')
        else:
            raise Exception(f"API Error: {response.status_code} - {response.text}")
    
    return {'results': all_results}

def main():
    # Load credentials
    creds = load_credentials()
    token = creds['notion_token']
    dev_db_id = creds['database_dev']
    sprint_db_id = creds['sprint_database_id']
    
    # Get sprint filter
    sprint_filter = sys.argv[1] if len(sys.argv) > 1 else None
    
    # If filtering by sprint, get Sprint UUID first
    sprint_uuid = None
    sprint_name = None
    if sprint_filter:
        print(f"🔍 Looking for Sprint {sprint_filter}...")
        sprint_data = query_database_with_filter(token, sprint_db_id)
        
        for sprint in sprint_data.get('results', []):
            props = sprint.get('properties', {})
            for key in props.keys():
                if props[key].get('type') == 'title':
                    tlist = props[key].get('title', [])
                    if tlist:
                        name = tlist[0].get('plain_text', '')
                        name_lower = name.lower().strip()
                        # Match "Sprint 2 –" or "Sprint 2 " at start
                        if name_lower.startswith(f'sprint {sprint_filter} ') or name_lower.startswith(f'sprint {sprint_filter}–'):
                            sprint_uuid = sprint.get('id')
                            sprint_name = name
                            print(f"✅ Found: {name}")
                            print(f"   UUID: {sprint_uuid}")
                            break
            if sprint_uuid:
                break
        
        if not sprint_uuid:
            print(f"❌ Sprint {sprint_filter} not found")
            sys.exit(1)
    
    # Query tickets with filter if sprint specified
    filter_obj = None
    if sprint_uuid:
        # IMPORTANT: Remove dashes from UUID for relation filter
        clean_id = sprint_uuid.replace('-', '')
        filter_obj = {
            "property": "Sprint",
            "relation": {
                "contains": clean_id
            }
        }
        print(f"\n📊 Querying with Sprint filter (ID: {clean_id})...")
    else:
        print(f"\n📊 Querying all tickets...")
    
    tickets_data = query_database_with_filter(token, dev_db_id, filter_obj)
    
    tickets = []
    for ticket in tickets_data.get('results', []):
        props = ticket.get('properties', {})
        
        # Get title
        title = "Untitled"
        for key in props.keys():
            if props[key].get('type') == 'title':
                tlist = props[key].get('title', [])
                if tlist:
                    title = tlist[0].get('plain_text', 'Untitled')
                break
        
        tickets.append({
            'title': title,
            'url': ticket.get('url')
        })
    
    # Display results
    if not tickets:
        if sprint_filter:
            print(f"\n❌ No tickets found in Sprint {sprint_filter}")
        else:
            print("\n❌ No tickets found")
        sys.exit(1)
    
    print(f"\n{'='*70}")
    if sprint_filter and sprint_name:
        print(f"Tickets in {sprint_name}:")
    else:
        print("All tickets:")
    print('='*70)
    
    for i, ticket in enumerate(tickets, 1):
        print(f"\n{i}. {ticket['title']}")
        print(f"   🔗 {ticket['url']}")
    
    print(f"\n✅ Total: {len(tickets)} tickets")

if __name__ == "__main__":
    main()
