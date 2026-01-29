#!/usr/bin/env python3
"""
Update ticket status by searching for title and sprint
Usage: 
    python3 update-ticket-status.py "[Tech] n+1_documents #2878" "Sprint 2" "Not Started"
    python3 update-ticket-status.py "ticket title" --status "In Progress"
"""
import sys
import json
import os
import argparse
import httpx
from pathlib import Path

try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass

CREDENTIALS_FILE = "/Users/ahmadfaris/moltbot-workspace/notion-credentials.json"

def load_credentials():
    notion_token = os.getenv('NOTION_TOKEN')
    database_dev = os.getenv('DATABASE_DEV')
    
    if notion_token and database_dev:
        return {
            'notion_token': notion_token,
            'database_dev': database_dev
        }
    
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Credentials not found")
        print("Set NOTION_TOKEN & DATABASE_DEV in .env")
        sys.exit(1)

def search_ticket(token, database_id, title, sprint=None):
    """Search for ticket by title and optional sprint"""
    try:
        # Query database via HTTP (no filter initially, search client-side)
        headers = {
            'Authorization': f'Bearer {token}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json'
        }
        
        url = f'https://api.notion.com/v1/databases/{database_id}/query'
        body = {}
        
        # Add sprint filter if specified
        if sprint:
            body['filter'] = {
                "property": "Sprint",
                "select": {
                    "equals": sprint
                }
            }
        
        response = httpx.post(url, headers=headers, json=body, timeout=30.0)
        
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return None
        
        data = response.json()
        all_pages = data.get('results', [])
        
        # Filter client-side by title
        pages = []
        for page in all_pages:
            # Find title property
            page_title = ''
            for key, prop in page['properties'].items():
                if prop.get('type') == 'title':
                    tlist = prop.get('title', [])
                    if tlist:
                        page_title = tlist[0].get('plain_text', '')
                    break
            
            # Check if title contains search string (case-insensitive)
            if title.lower() in page_title.lower():
                pages.append(page)
        
        if not pages:
            print(f"❌ No tickets found matching: '{title}'")
            if sprint:
                print(f"   in sprint: '{sprint}'")
            return None
        
        if len(pages) > 1:
            print(f"⚠️  Found {len(pages)} tickets matching '{title}':")
            for i, page in enumerate(pages, 1):
                # Extract title
                page_title = 'Untitled'
                for key, prop in page['properties'].items():
                    if prop.get('type') == 'title':
                        tlist = prop.get('title', [])
                        if tlist:
                            page_title = tlist[0].get('plain_text', 'Untitled')
                        break
                
                page_sprint = page['properties'].get('Sprint', {}).get('select', {}).get('name', 'No Sprint')
                page_status = page['properties'].get('Status', {}).get('status', {}).get('name', 'No Status')
                print(f"  {i}. {page_title}")
                print(f"     Sprint: {page_sprint} | Status: {page_status}")
            
            if sprint:
                print("\n💡 Try being more specific with the title or check the sprint name")
            else:
                print("\n💡 Add sprint filter to narrow down: python3 update-ticket-status.py \"title\" \"Sprint X\" \"status\"")
            return None
        
        # Found exactly one ticket
        return pages[0]
        
    except Exception as e:
        print(f"❌ Error searching tickets: {e}")
        import traceback
        traceback.print_exc()
        return None

def update_ticket_status(token, page_id, new_status):
    """Update ticket status"""
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json'
        }
        
        url = f'https://api.notion.com/v1/pages/{page_id}'
        body = {
            "properties": {
                "Status": {
                    "status": {
                        "name": new_status
                    }
                }
            }
        }
        
        response = httpx.patch(url, headers=headers, json=body, timeout=30.0)
        
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error updating status: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Update Notion ticket status by searching title',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update status (will search by title)
  %(prog)s "[Tech] n+1_documents #2878" --status "Not Started"
  
  # Update status with sprint filter
  %(prog)s "[Tech] n+1_documents #2878" --sprint "Sprint 2" --status "Not Started"
  
  # Shorthand (positional args: title, sprint, status)
  %(prog)s "[Tech] n+1_documents #2878" "Sprint 2" "Not Started"
        """
    )
    
    parser.add_argument('title', help='Ticket title (or part of it)')
    parser.add_argument('sprint', nargs='?', help='Sprint name (optional)')
    parser.add_argument('status_arg', nargs='?', help='New status (optional if using --status)')
    parser.add_argument('--sprint', dest='sprint_flag', help='Sprint name')
    parser.add_argument('--status', dest='status_flag', help='New status')
    
    args = parser.parse_args()
    
    # Parse arguments (support both positional and flag style)
    title = args.title
    sprint = args.sprint_flag or args.sprint
    status = args.status_flag or args.status_arg
    
    if not status:
        print("❌ Error: Status is required")
        parser.print_help()
        sys.exit(1)
    
    # Load credentials
    creds = load_credentials()
    token = creds['notion_token']
    database_id = creds['database_dev']
    
    print(f"🔍 Searching for ticket: '{title}'")
    if sprint:
        print(f"   in sprint: '{sprint}'")
    
    # Search for ticket
    ticket = search_ticket(token, database_id, title, sprint)
    
    if not ticket:
        sys.exit(1)
    
    # Display found ticket
    ticket_id = ticket['id']
    
    # Extract title
    ticket_title = 'Untitled'
    for key, prop in ticket['properties'].items():
        if prop.get('type') == 'title':
            tlist = prop.get('title', [])
            if tlist:
                ticket_title = tlist[0].get('plain_text', 'Untitled')
            break
    
    current_status = ticket['properties'].get('Status', {}).get('status', {}).get('name', 'No Status')
    ticket_sprint = ticket['properties'].get('Sprint', {}).get('select', {}).get('name', 'No Sprint')
    
    print(f"\n✓ Found ticket:")
    print(f"  Title: {ticket_title}")
    print(f"  Sprint: {ticket_sprint}")
    print(f"  Current Status: {current_status}")
    print(f"  → New Status: {status}")
    
    # Update status
    print(f"\n🔄 Updating status...")
    success = update_ticket_status(token, ticket_id, status)
    
    if success:
        print(f"✅ Status updated to '{status}'!")
        print(f"🔗 https://notion.so/{ticket_id.replace('-', '')}")
    else:
        print("❌ Failed to update status")
        sys.exit(1)

if __name__ == "__main__":
    main()
