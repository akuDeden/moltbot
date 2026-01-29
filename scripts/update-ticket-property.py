#!/usr/bin/env python3
"""
Update ticket properties in Notion database
Usage: 
    # Update assigned user
    python3 update-ticket-property.py PAGE_URL --assigned "user@email.com"
    
    # Update sprint
    python3 update-ticket-property.py PAGE_URL --sprint "Sprint 1"
    
    # Update status
    python3 update-ticket-property.py PAGE_URL --status "In Progress"
    
    # Update multiple properties at once
    python3 update-ticket-property.py PAGE_URL --assigned "user@email.com" --sprint "Sprint 2" --status "Done"
"""
import sys
import json
import re
import os
import argparse
from pathlib import Path

try:
    from notion_client import Client
except ImportError:
    print("❌ Error: notion-client not installed")
    print("Install with: pip install notion-client")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass  # dotenv optional

CREDENTIALS_FILE = "/Users/ahmadfaris/moltbot-workspace/notion-credentials.json"

def load_credentials():
    # Try .env first
    notion_token = os.getenv('NOTION_TOKEN')
    database_dev = os.getenv('DATABASE_DEV')
    
    if notion_token:
        creds = {'notion_token': notion_token}
        if database_dev:
            creds['database_dev'] = database_dev
        return creds
    
    # Fallback to JSON
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Credentials not found")
        print("Set NOTION_TOKEN in .env or create notion-credentials.json")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: {CREDENTIALS_FILE} is not valid JSON")
        sys.exit(1)

def extract_page_id_from_url(url):
    """Extract page ID from Notion URL or use raw ID"""
    # If already a 32-char hex ID, return as is
    if re.match(r'^[a-f0-9]{32}$', url):
        return url
    
    # Pattern: https://www.notion.so/Page-Title-XXXXXXXXX
    match = re.search(r'([a-f0-9]{32})', url)
    if match:
        return match.group(1)
    
    # Try with dashes (format: 8-4-4-4-12)
    match = re.search(r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', url)
    if match:
        return match.group(1).replace('-', '')
    
    return None

def get_database_schema(notion, database_id):
    """Get database schema to find available properties and their types"""
    try:
        db = notion.databases.retrieve(database_id=database_id)
        return db.get('properties', {})
    except Exception as e:
        print(f"⚠️  Warning: Could not retrieve database schema: {e}")
        return {}

def find_user_by_email(notion, email):
    """Find Notion user by email"""
    try:
        users = notion.users.list()
        for user in users.get('results', []):
            user_email = user.get('person', {}).get('email', '')
            if user_email.lower() == email.lower():
                return user.get('id')
        
        print(f"⚠️  User with email '{email}' not found")
        print("Available users:")
        for user in users.get('results', []):
            user_email = user.get('person', {}).get('email', 'N/A')
            user_name = user.get('name', 'Unknown')
            print(f"  - {user_name} ({user_email})")
        return None
    except Exception as e:
        print(f"❌ Error finding user: {e}")
        return None

def get_page_database_id(notion, page_id):
    """Get the database ID that this page belongs to"""
    try:
        page = notion.pages.retrieve(page_id=page_id)
        parent = page.get('parent', {})
        if parent.get('type') == 'database_id':
            return parent.get('database_id')
        return None
    except Exception as e:
        print(f"❌ Error getting page info: {e}")
        return None

def update_page_properties(notion, page_id, updates):
    """Update page properties"""
    try:
        # Get database ID from page
        database_id = get_page_database_id(notion, page_id)
        if not database_id:
            print("❌ Error: Could not determine database for this page")
            return False
        
        # Get database schema
        schema = get_database_schema(notion, database_id)
        if not schema:
            print("⚠️  Warning: Could not get database schema, attempting update anyway...")
        
        # Build properties update object
        properties = {}
        
        for key, value in updates.items():
            if value is None:
                continue
            
            # Find the property in schema (case-insensitive)
            prop_name = None
            prop_type = None
            
            for schema_key, schema_value in schema.items():
                if schema_key.lower() == key.lower():
                    prop_name = schema_key
                    prop_type = schema_value.get('type')
                    break
            
            if not prop_name:
                print(f"⚠️  Property '{key}' not found in database schema")
                # Try using the key as-is
                prop_name = key
            
            # Build property value based on type
            if key == 'assigned':
                # People/User property
                if isinstance(value, list):
                    properties[prop_name] = {
                        "people": [{"id": uid} for uid in value]
                    }
                else:
                    properties[prop_name] = {
                        "people": [{"id": value}]
                    }
            
            elif key == 'sprint':
                # Assume it's a select or multi-select
                if prop_type == 'multi_select':
                    if isinstance(value, list):
                        properties[prop_name] = {
                            "multi_select": [{"name": v} for v in value]
                        }
                    else:
                        properties[prop_name] = {
                            "multi_select": [{"name": value}]
                        }
                else:  # Default to select
                    properties[prop_name] = {
                        "select": {"name": value}
                    }
            
            elif key == 'status':
                # Status property (or select)
                if prop_type == 'status':
                    properties[prop_name] = {
                        "status": {"name": value}
                    }
                else:  # Fallback to select
                    properties[prop_name] = {
                        "select": {"name": value}
                    }
            
            else:
                # Generic handling for other types
                if prop_type == 'select':
                    properties[prop_name] = {"select": {"name": value}}
                elif prop_type == 'multi_select':
                    properties[prop_name] = {"multi_select": [{"name": value}]}
                elif prop_type == 'rich_text':
                    properties[prop_name] = {
                        "rich_text": [{"text": {"content": value}}]
                    }
        
        if not properties:
            print("❌ No properties to update")
            return False
        
        # Update the page
        notion.pages.update(
            page_id=page_id,
            properties=properties
        )
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating page: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Update Notion ticket properties',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s PAGE_URL --assigned "user@email.com"
  %(prog)s PAGE_URL --sprint "Sprint 1" --status "In Progress"
  %(prog)s 32e29af7d7dd4df69310270de8830d1a --assigned "user@email.com"
        """
    )
    
    parser.add_argument('page_url', help='Notion page URL or ID')
    parser.add_argument('--assigned', help='Assign to user (email address)')
    parser.add_argument('--sprint', help='Set sprint name')
    parser.add_argument('--status', help='Set status')
    parser.add_argument('--list-users', action='store_true', help='List all available users')
    
    args = parser.parse_args()
    
    # Load credentials
    creds = load_credentials()
    notion = Client(auth=creds['notion_token'])
    
    # List users if requested
    if args.list_users:
        print("📋 Available users:")
        try:
            users = notion.users.list()
            for user in users.get('results', []):
                user_email = user.get('person', {}).get('email', 'N/A')
                user_name = user.get('name', 'Unknown')
                user_id = user.get('id', 'N/A')
                print(f"  - {user_name} ({user_email}) [ID: {user_id}]")
        except Exception as e:
            print(f"❌ Error listing users: {e}")
        return
    
    # Extract page ID
    page_id = extract_page_id_from_url(args.page_url)
    if not page_id:
        print(f"❌ Error: Invalid Notion URL or ID")
        sys.exit(1)
    
    print(f"📄 Page ID: {page_id}")
    
    # Build updates dict
    updates = {}
    
    if args.assigned:
        # Find user by email
        user_id = find_user_by_email(notion, args.assigned)
        if not user_id:
            print("❌ Error: User not found")
            sys.exit(1)
        updates['assigned'] = user_id
        print(f"✓ Will assign to: {args.assigned}")
    
    if args.sprint:
        updates['sprint'] = args.sprint
        print(f"✓ Will set sprint to: {args.sprint}")
    
    if args.status:
        updates['status'] = args.status
        print(f"✓ Will set status to: {args.status}")
    
    if not updates:
        print("❌ Error: No properties to update. Use --assigned, --sprint, or --status")
        parser.print_help()
        sys.exit(1)
    
    # Perform update
    print("\n🔄 Updating properties...")
    success = update_page_properties(notion, page_id, updates)
    
    if success:
        print("✅ Properties updated successfully!")
    else:
        print("❌ Failed to update properties")
        sys.exit(1)

if __name__ == "__main__":
    main()
