#!/usr/bin/env python3
"""
Update assignee of a ticket
Usage: python3 update-ticket-assignee.py "<ticket_title>" "<assignee_name>"
Example: python3 update-ticket-assignee.py "Elasticsearch Query Builder" "Ahmad Faris"
"""
import sys
import json
import httpx
import os

def load_credentials():
    """Load credentials from .env file"""
    env_file = os.path.expanduser('~/moltbot-workspace/.env')

    if not os.path.exists(env_file):
        raise Exception(f"Credentials file not found: {env_file}")

    creds = {}
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                creds[key] = value

    if not all(k in creds for k in ['NOTION_TOKEN', 'DATABASE_DEV']):
        raise Exception("Missing required credentials in .env file")

    return creds

def search_tickets(token, db_id, search_title):
    """Search for tickets by title"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }

    url = f'https://api.notion.com/v1/databases/{db_id}/query'

    # Get all tickets first
    all_results = []
    has_more = True
    start_cursor = None

    while has_more:
        body = {}
        if start_cursor:
            body['start_cursor'] = start_cursor

        response = httpx.post(url, headers=headers, json=body, timeout=30.0)

        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])

            # Search in results
            for result in results:
                props = result.get('properties', {})
                title = ""

                # Extract title
                for key in props.keys():
                    if props[key].get('type') == 'title':
                        tlist = props[key].get('title', [])
                        if tlist:
                            title = tlist[0].get('plain_text', '')
                        break

                if search_title.lower() in title.lower():
                    all_results.append({
                        'id': result.get('id'),
                        'title': title,
                        'url': result.get('url'),
                        'props': props
                    })

            has_more = data.get('has_more', False)
            start_cursor = data.get('next_cursor')
        else:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

    return all_results

def find_assignee_property(props):
    """Find the assignee property name"""
    assignee_keys = ['Assignee', 'assignee', 'Owner', 'owner', 'Assigned to', 'assigned_to']

    for key in assignee_keys:
        if key in props:
            prop = props[key]
            if prop.get('type') == 'people':
                return key

    # Look for any people type property
    for key, prop in props.items():
        if prop.get('type') == 'people':
            return key

    return None

def update_assignee(token, ticket_id, assignee_property, assignee_user_id=None, assignee_email=None):
    """Update the assignee of a ticket"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }

    url = f'https://api.notion.com/v1/pages/{ticket_id}'

    body = {
        'properties': {
            assignee_property: {
                'people': []
            }
        }
    }

    if assignee_user_id:
        body['properties'][assignee_property]['people'].append({
            'object': 'user',
            'id': assignee_user_id
        })

    response = httpx.patch(url, headers=headers, json=body, timeout=30.0)

    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.text

def search_user_by_email(token, email):
    """Search for a user by email"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }

    url = 'https://api.notion.com/v1/users'

    response = httpx.get(url, headers=headers, timeout=30.0)

    if response.status_code == 200:
        data = response.json()
        users = data.get('results', [])

        for user in users:
            user_type = user.get('type', '')
            if user_type == 'person':
                person = user.get('person', {})
                if person.get('email', '').lower() == email.lower():
                    return user.get('id'), user

    return None, None

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 update-ticket-assignee.py '<ticket_title>' '<assignee_name>'")
        print("Example: python3 update-ticket-assignee.py 'Elasticsearch Query Builder' 'Ahmad Faris'")
        sys.exit(1)

    ticket_title = sys.argv[1]
    assignee_name = sys.argv[2]

    # Load credentials
    creds = load_credentials()
    token = creds['NOTION_TOKEN']
    dev_db_id = creds['DATABASE_DEV']

    print(f"🔍 Searching for ticket: '{ticket_title}'...")
    tickets = search_tickets(token, dev_db_id, ticket_title)

    if not tickets:
        print(f"❌ No tickets found matching: '{ticket_title}'")
        sys.exit(1)

    if len(tickets) > 1:
        print(f"⚠️  Found {len(tickets)} tickets matching. Showing all:")
        for i, ticket in enumerate(tickets, 1):
            print(f"{i}. {ticket['title']}")
            print(f"   ID: {ticket['id']}")
            print(f"   🔗 {ticket['url']}")
        print("\nUsing the first match.")

    ticket = tickets[0]
    ticket_id = ticket['id']
    props = ticket['props']

    print(f"✅ Found ticket: {ticket['title']}")
    print(f"   ID: {ticket_id}")
    print(f"   🔗 {ticket['url']}")

    # Find assignee property
    assignee_property = find_assignee_property(props)
    if not assignee_property:
        print("❌ No 'Assignee' property found in ticket")
        print("Available properties:")
        for key in props.keys():
            prop_type = props[key].get('type', '')
            print(f"  - {key} ({prop_type})")
        sys.exit(1)

    print(f"📝 Assignee property: {assignee_property}")

    # Try to find user by common email patterns
    possible_emails = [
        f"{assignee_name.replace(' ', '.').lower()}@gmail.com",
        f"{assignee_name.replace(' ', '.').lower()}@yahoo.com",
    ]

    assignee_user_id = None

    for email in possible_emails:
        print(f"🔍 Searching for user with email: {email}")
        user_id, user = search_user_by_email(token, email)
        if user_id:
            assignee_user_id = user_id
            print(f"✅ Found user: {user.get('name', 'Unknown')} ({email})")
            break

    if not assignee_user_id:
        print("⚠️  Could not find user by email. Please provide the User ID.")
        print("You can find User IDs by:")
        print("1. Going to Notion database page")
        print("2. Opening browser DevTools (F12)")
        print("3. Looking at Network tab for user data")
        print("\nFor now, setting assignee to empty (unassigning).")
        assignee_user_id = None

    # Update assignee
    print(f"\n🔄 Updating assignee...")
    success, result = update_assignee(token, ticket_id, assignee_property, assignee_user_id)

    if success:
        print("✅ Assignee updated successfully!")
        print(f"🔗 {ticket['url']}")
    else:
        print(f"❌ Failed to update assignee: {result}")

if __name__ == "__main__":
    main()
