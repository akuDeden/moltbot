#!/usr/bin/env python3
"""
Update assignee of a ticket by searching with title filter
Usage: python3 update-ticket-assignee-simple.py "<ticket_title>" "<assignee_name>"
Example: python3 update-ticket-assignee-simple.py "Elasticsearch Query Builder" "Ahmad Faris"
"""
import sys
import httpx
import os

def load_credentials():
    """Load credentials from .env file"""
    env_file = os.path.expanduser('~/moltbot-workspace/.env')  # Absolute path for compatibility

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

def search_ticket_by_title(token, db_id, search_title):
    """Search for a specific ticket by title using exact match"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }

    url = f'https://api.notion.com/v1/databases/{db_id}/query'

    # Find the title property name first
    body = {
        "page_size": 1
    }

    response = httpx.post(url, headers=headers, json=body, timeout=30.0)
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

    data = response.json()
    first_result = data.get('results', [{}])[0]
    props = first_result.get('properties', {})

    title_property = None
    for key in props.keys():
        if props[key].get('type') == 'title':
            title_property = key
            break

    if not title_property:
        raise Exception("Could not find title property")

    # Now search with title filter
    body = {
        "filter": {
            "property": title_property,
            "title": {
                "equals": search_title
            }
        },
        "page_size": 5
    }

    response = httpx.post(url, headers=headers, json=body, timeout=30.0)
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

    data = response.json()
    results = data.get('results', [])

    if not results:
        return None

    return results[0]

def find_assignee_property(props):
    """Find the assignee property name - MUST be 'Assignee' not 'Tester'"""
    # CRITICAL: Target the actual 'Assignee' property (notion://tasks/assign_property)
    # NOT 'Tester' which is a different people field!
    
    # Try exact match first (Notion database uses 'Assignee' for the main assignee field)
    if 'Assignee' in props and props['Assignee'].get('type') == 'people':
        return 'Assignee'
    
    # Fallback to case variations
    assignee_keys = ['assignee', 'Owner', 'owner', 'Assigned to', 'assigned_to']
    for key in assignee_keys:
        if key in props and props[key].get('type') == 'people':
            return key
    
    # DO NOT fallback to any people property - this causes Tester to be used instead!
    # If Assignee not found, return None and fail explicitly
    return None

def update_assignee(token, ticket_id, assignee_property, assignee_user_id=None):
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

def get_users(token):
    """Get all users from workspace"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }

    url = 'https://api.notion.com/v1/users'

    response = httpx.get(url, headers=headers, timeout=30.0)

    if response.status_code == 200:
        data = response.json()
        return data.get('results', [])
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 update-ticket-assignee-simple.py '<ticket_title>' ['<assignee_name>']")
        print("Example: python3 update-ticket-assignee-simple.py 'Elasticsearch Query Builder' 'Ahmad Faris'")
        sys.exit(1)

    ticket_title = sys.argv[1]
    assignee_name = sys.argv[2] if len(sys.argv) > 2 else None

    # Load credentials
    creds = load_credentials()
    token = creds['NOTION_TOKEN']
    dev_db_id = creds['DATABASE_DEV']

    print(f"🔍 Searching for ticket: '{ticket_title}'...")

    try:
        ticket = search_ticket_by_title(token, dev_db_id, ticket_title)

        if not ticket:
            print(f"❌ No ticket found with exact title: '{ticket_title}'")
            print("\nTry using the exact title from the list.")
            sys.exit(1)

        ticket_id = ticket['id']
        props = ticket['props'] if 'props' in ticket else ticket.get('properties', {})

        print(f"✅ Found ticket")
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

        # If no assignee name provided, just unassign
        if not assignee_name:
            print(f"\n🔄 Unassigning ticket...")
            success, result = update_assignee(token, ticket_id, assignee_property, None)

            if success:
                print("✅ Ticket unassigned successfully!")
                print(f"🔗 {ticket['url']}")
            else:
                print(f"❌ Failed to unassign: {result}")
            sys.exit(0)

        # Get users to find assignee
        print(f"\n👥 Searching for users...")
        users = get_users(token)

        # Try to find user by name
        assignee_user_id = None

        for user in users:
            user_type = user.get('type', '')
            if user_type == 'person':
                person = user.get('person', {})
                user_name = user.get('name', '')
                user_email = person.get('email', '')

                # Try to match by name
                if assignee_name.lower() in user_name.lower():
                    assignee_user_id = user.get('id')
                    print(f"✅ Found user: {user_name} ({user_email})")
                    print(f"   User ID: {assignee_user_id}")
                    break

        if not assignee_user_id:
            print(f"⚠️  Could not find user with name: '{assignee_name}'")
            print("\nAvailable users:")
            for user in users:
                user_type = user.get('type', '')
                if user_type == 'person':
                    person = user.get('person', {})
                    user_name = user.get('name', '')
                    user_email = person.get('email', '')
                    print(f"  - {user_name} ({user_email})")
            sys.exit(1)

        # Update assignee
        print(f"\n🔄 Assigning ticket to {assignee_name}...")
        success, result = update_assignee(token, ticket_id, assignee_property, assignee_user_id)

        if success:
            print(f"✅ Ticket assigned to {assignee_name} successfully!")
            print(f"🔗 {ticket['url']}")
        else:
            print(f"❌ Failed to assign: {result}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
