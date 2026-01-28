#!/usr/bin/env python3
"""List all databases accessible via Notion API"""
import json
from notion_client import Client
from collections import Counter

# Load credentials
with open('/Users/ahmadfaris/moltbot-workspace/notion-credentials.json', 'r') as f:
    creds = json.load(f)

notion = Client(auth=creds['notion_token'])

# Search all pages
response = notion.search(page_size=100)
results = response.get('results', [])

# Count by database
db_counts = Counter()
db_samples = {}

for r in results:
    parent = r.get('parent', {})
    if parent.get('type') == 'database_id':
        db_id = parent.get('database_id', '')
        db_counts[db_id] += 1
        
        if db_id not in db_samples:
            title = r.get('properties', {}).get('Name', {}).get('title', [])
            title_text = title[0].get('plain_text', '') if title else ''
            db_samples[db_id] = title_text

print('📊 Database yang ditemukan:\n')
for db_id, count in db_counts.most_common():
    sample = db_samples.get(db_id, '')
    print(f"  {db_id} → {count} pages")
    if sample:
        print(f"    Sample: {sample[:50]}")
    print()

print(f"\n✅ Database dev dari config: {creds.get('database_dev')}")
print(f"✅ Database bug dari config: {creds.get('database_bug')}")
