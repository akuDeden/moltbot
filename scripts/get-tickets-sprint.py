#!/usr/bin/env python3
"""
Get tickets from database_dev filtered by sprint with STATUS/WORKFLOW
Usage: python3 get-tickets-sprint.py [sprint_number]
Example: python3 get-tickets-sprint.py 2
"""
import sys
import json
import httpx
import os
from collections import defaultdict
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Fallback to JSON file if .env not found
CREDENTIALS_FILE = os.environ.get(
    'NOTION_CREDENTIALS_FILE',
    os.path.expanduser('~/moltbot-workspace/notion-credentials.json')
)

def load_credentials():
    """Load credentials from environment variables or JSON file"""
    # Try .env first
    notion_token = os.getenv('NOTION_TOKEN')
    database_dev = os.getenv('DATABASE_DEV')
    sprint_database_id = os.getenv('SPRINT_DATABASE_ID')
    
    if notion_token and database_dev and sprint_database_id:
        return {
            'notion_token': notion_token,
            'database_dev': database_dev,
            'sprint_database_id': sprint_database_id
        }
    
    # Fallback to JSON file
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    
    raise Exception(
        "Credentials not found! Either:\n"
        "1. Create .env file with NOTION_TOKEN, DATABASE_DEV, SPRINT_DATABASE_ID\n"
        f"2. Or create {CREDENTIALS_FILE} with JSON credentials"
    )

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

def extract_status(props):
    """Extract status from properties - try multiple common names"""
    # Common status property names
    status_keys = ['Status', 'status', 'Workflow', 'workflow', 'State', 'state']
    
    for key in status_keys:
        if key in props:
            prop = props[key]
            prop_type = prop.get('type', '')
            
            if prop_type == 'status':
                name = prop.get('status', {}).get('name', 'Unknown')
                return name
            elif prop_type == 'select':
                name = prop.get('select', {}).get('name', 'Unknown')
                return name
    
    # If no status found, look for any select/status type property
    for key, prop in props.items():
        prop_type = prop.get('type', '')
        if prop_type == 'status':
            name = prop.get('status', {}).get('name', 'Unknown')
            return name
        elif prop_type == 'select':
            name = prop.get('select', {}).get('name', 'Unknown')
            return name
    
    return 'Unknown'

def extract_title(props):
    """Extract title from properties"""
    for key in props.keys():
        if props[key].get('type') == 'title':
            tlist = props[key].get('title', [])
            if tlist:
                return tlist[0].get('plain_text', 'Untitled')
    return 'Untitled'

def extract_labels(props):
    """Extract tags/labels from properties"""
    labels = []
    for key, prop in props.items():
        prop_type = prop.get('type', '')
        if prop_type == 'multi_select':
            for item in prop.get('multi_select', []):
                labels.append(item.get('name', ''))
    return labels

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
    
    # Extract ticket data with status
    tickets = []
    for ticket in tickets_data.get('results', []):
        props = ticket.get('properties', {})
        title = extract_title(props)
        status = extract_status(props)
        labels = extract_labels(props)
        url = ticket.get('url')
        
        tickets.append({
            'title': title,
            'status': status,
            'labels': labels,
            'url': url
        })
    
    # Group by status
    tickets_by_status = defaultdict(list)
    for ticket in tickets:
        tickets_by_status[ticket['status']].append(ticket)
    
    # Display results
    if not tickets:
        if sprint_filter:
            print(f"\n❌ No tickets found in Sprint {sprint_filter}")
        else:
            print("\n❌ No tickets found")
        sys.exit(1)
    
    print(f"\n{'='*70}")
    if sprint_filter and sprint_name:
        print(f"{sprint_name} - Tickets by Status")
    else:
        print("Tickets by Status")
    print('='*70)
    
    # Status order (common workflow)
    status_order = ['To Do', 'In Progress', 'Done', 'In Review', 'Unknown']
    
    for status in status_order:
        if status in tickets_by_status:
            print(f"\n{'─'*70}")
            print(f"📌 {status.upper()} ({len(tickets_by_status[status])} tickets)")
            print('─'*70)
            
            for i, ticket in enumerate(tickets_by_status[status], 1):
                print(f"\n{i}. {ticket['title']}")
                if ticket['labels']:
                    labels_str = ', '.join(ticket['labels'][:3])  # Show max 3 labels
                    if len(ticket['labels']) > 3:
                        labels_str += f' +{len(ticket["labels"]) - 3} more'
                    print(f"   🏷️  {labels_str}")
                print(f"   🔗 {ticket['url']}")
    
    # Show any statuses not in predefined order
    for status, status_tickets in tickets_by_status.items():
        if status not in status_order:
            print(f"\n{'─'*70}")
            print(f"📌 {status.upper()} ({len(status_tickets)} tickets)")
            print('─'*70)
            
            for i, ticket in enumerate(status_tickets, 1):
                print(f"\n{i}. {ticket['title']}")
                if ticket['labels']:
                    labels_str = ', '.join(ticket['labels'][:3])
                    if len(ticket['labels']) > 3:
                        labels_str += f' +{len(ticket["labels"]) - 3} more'
                    print(f"   🏷️  {labels_str}")
                print(f"   🔗 {ticket['url']}")
    
    # Summary
    print(f"\n{'='*70}")
    print("📊 SUMMARY")
    print('='*70)
    for status in sorted(tickets_by_status.keys()):
        count = len(tickets_by_status[status])
        percentage = (count / len(tickets)) * 100
        bar = '█' * int(percentage / 5)
        print(f"{status:20s} [{count:2d}] {bar:<20} {percentage:.1f}%")
    
    print(f"\n✅ Total: {len(tickets)} tickets")

if __name__ == "__main__":
    main()
