#!/usr/bin/env python3
"""
List all tickets with their exact titles to find the right one
"""
import httpx
import os

def load_credentials():
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

    return creds

creds = load_credentials()
token = creds['NOTION_TOKEN']
dev_db_id = creds['DATABASE_DEV']

headers = {
    'Authorization': f'Bearer {token}',
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json'
}

url = f'https://api.notion.com/v1/databases/{dev_db_id}/query'

all_results = []
has_more = True
start_cursor = None

print("Fetching all tickets...")

while has_more:
    body = {}
    if start_cursor:
        body['start_cursor'] = start_cursor

    response = httpx.post(url, headers=headers, json=body, timeout=30.0)

    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        all_results.extend(results)
        has_more = data.get('has_more', False)
        start_cursor = data.get('next_cursor')
        print(f"Fetched {len(results)} tickets (total: {len(all_results)})")
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

print(f"\nTotal tickets: {len(all_results)}")
print("\nSearching for Elasticsearch tickets...")

for ticket in all_results:
    props = ticket.get('properties', {})

    # Extract title
    title = ""
    for key in props.keys():
        if props[key].get('type') == 'title':
            tlist = props[key].get('title', [])
            if tlist:
                title = tlist[0].get('plain_text', '')
            break

    if 'elasticsearch' in title.lower():
        print(f"\n✅ Found: {title}")
        print(f"   ID: {ticket['id']}")
        print(f"   🔗 {ticket['url']}")
