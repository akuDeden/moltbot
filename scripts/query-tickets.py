#!/usr/bin/env python3
"""
Search tickets by keywords with optional sprint filter
Usage: 
    python3 query-tickets.py "sales"
    python3 query-tickets.py "sales" --sprint "Sprint 2"
    python3 query-tickets.py --all  # akan minta konfirmasi
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

def get_sprint_id(token, sprint_database_id, sprint_name):
    """Get Sprint UUID from Sprint name"""
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json'
        }
        
        url = f'https://api.notion.com/v1/databases/{sprint_database_id}/query'
        response = httpx.post(url, headers=headers, json={}, timeout=30.0)
        
        if response.status_code != 200:
            # Debug: show error
            # print(f"Debug: Sprint DB error {response.status_code}: {response.text}")
            return None
        
        data = response.json()
        sprints = data.get('results', [])
        
        # Search for matching sprint name
        for sprint_page in sprints:
            # Extract sprint title
            for key, prop in sprint_page['properties'].items():
                if prop.get('type') == 'title':
                    tlist = prop.get('title', [])
                    if tlist:
                        title = tlist[0].get('plain_text', '')
                        # Match sprint name (case-insensitive, partial match)
                        if sprint_name.lower() in title.lower():
                            sprint_id = sprint_page['id'].replace('-', '')
                            # print(f"Debug: Found Sprint '{title}' with ID {sprint_id}")
                            return sprint_id
        
        return None
        
    except Exception as e:
        # print(f"Debug: Exception in get_sprint_id: {e}")
        # import traceback
        # traceback.print_exc()
        return None

def load_credentials():
    notion_token = os.getenv('NOTION_TOKEN')
    database_dev = os.getenv('DATABASE_DEV')
    sprint_database_id = os.getenv('SPRINT_DATABASE_ID')
    
    if notion_token and database_dev and sprint_database_id:
        return {
            'notion_token': notion_token,
            'database_dev': database_dev,
            'sprint_database_id': sprint_database_id
        }
    
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Credentials not found")
        print("Set NOTION_TOKEN, DATABASE_DEV & SPRINT_DATABASE_ID in .env")
        sys.exit(1)

def confirm_fetch_all():
    """Ask user confirmation before fetching all tickets"""
    print("\n⚠️  PERINGATAN: Ini akan mengambil SEMUA tiket dari database dev.")
    print("   Proses ini akan memakan waktu lama.")
    print()
    
    while True:
        response = input("Anda yakin mau lanjut? (ya/tidak): ").strip().lower()
        if response in ['ya', 'y', 'yes', 'iya', 'setuju', 'ia']:
            return True
        elif response in ['tidak', 'no', 'n', 'cancel', 'batal']:
            return False
        else:
            print("⚠️  Mohon jawab 'ya' atau 'tidak'")

def search_tickets(token, database_id, sprint_database_id=None, keywords=None, sprint=None, fetch_all=False):
    """Search for tickets by keywords and optional sprint"""
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json'
        }
        
        url = f'https://api.notion.com/v1/databases/{database_id}/query'
        body = {}
        
        # Add sprint filter if specified
        if sprint:
            # Get Sprint UUID first
            sprint_uuid = get_sprint_id(token, sprint_database_id, sprint)
            if not sprint_uuid:
                print(f"⚠️  Sprint '{sprint}' tidak ditemukan")
                return []
            
            body['filter'] = {
                "property": "Sprint",
                "relation": {
                    "contains": sprint_uuid
                }
            }
        
        # Fetch all pages (handle pagination)
        all_results = []
        has_more = True
        start_cursor = None
        page_count = 0
        
        print(f"🔍 Mencari tiket...")
        if keywords:
            print(f"   Kata kunci: '{keywords}'")
        if sprint:
            print(f"   Sprint: '{sprint}'")
        if fetch_all:
            print(f"   Mode: Ambil semua tiket")
        
        while has_more:
            if start_cursor:
                body['start_cursor'] = start_cursor
            
            response = httpx.post(url, headers=headers, json=body, timeout=30.0)
            
            if response.status_code != 200:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return []
            
            data = response.json()
            all_results.extend(data.get('results', []))
            
            has_more = data.get('has_more', False)
            start_cursor = data.get('next_cursor')
            page_count += 1
            
            # Show progress for large fetches
            if page_count > 1:
                print(f"   📄 Halaman {page_count}, total: {len(all_results)} tiket...")
        
        # Filter by keywords if provided (client-side search)
        if keywords and not fetch_all:
            filtered = []
            for page in all_results:
                # Extract title
                page_title = ''
                for key, prop in page['properties'].items():
                    if prop.get('type') == 'title':
                        tlist = prop.get('title', [])
                        if tlist:
                            page_title = tlist[0].get('plain_text', '')
                        break
                
                # Check if keywords match title (case-insensitive)
                if keywords.lower() in page_title.lower():
                    filtered.append(page)
            
            return filtered
        
        return all_results
        
    except Exception as e:
        print(f"❌ Error searching tickets: {e}")
        import traceback
        traceback.print_exc()
        return []

def display_tickets(tickets):
    """Display tickets in a formatted way"""
    if not tickets:
        print("\n❌ Tidak ada tiket ditemukan.")
        return
    
    print(f"\n✅ Ditemukan {len(tickets)} tiket:\n")
    
    for i, page in enumerate(tickets, 1):
        # Extract title
        page_title = 'Untitled'
        for key, prop in page['properties'].items():
            if prop.get('type') == 'title':
                tlist = prop.get('title', [])
                if tlist:
                    page_title = tlist[0].get('plain_text', 'Untitled')
                break
        
        # Extract properties
        status = page['properties'].get('Status', {}).get('status', {}).get('name', 'No Status')
        
        # Extract Sprint (relation field)
        sprint_prop = page['properties'].get('Sprint', {})
        sprint_name = 'No Sprint'
        if sprint_prop.get('relation'):
            relations = sprint_prop['relation']
            if relations:
                # For now just show "Sprint" since we'd need another API call to get the name
                # Could be improved later with caching
                sprint_name = 'Sprint (linked)'
        
        # Extract assignee if exists
        assignee_prop = page['properties'].get('Assignee', {})
        assignee = 'Unassigned'
        if assignee_prop.get('people'):
            people = assignee_prop['people']
            if people:
                assignee = people[0].get('name', 'Unassigned')
        
        # Get page ID for URL
        page_id = page['id'].replace('-', '')
        
        print(f"{i}. {page_title}")
        print(f"   Status: {status} | Sprint: {sprint_name} | Assignee: {assignee}")
        print(f"   🔗 https://notion.so/{page_id}")
        print()

def main():
    parser = argparse.ArgumentParser(
        description='Search Notion tickets by keywords',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Cari tiket dengan kata kunci "sales"
  %(prog)s "sales"
  
  # Cari tiket "sales" di Sprint 2
  %(prog)s "sales" --sprint "Sprint 2"
  
  # Ambil semua tiket (dengan konfirmasi)
  %(prog)s --all
  
  # Cari tiket di sprint tertentu (tanpa kata kunci)
  %(prog)s --sprint "Sprint 2"
        """
    )
    
    parser.add_argument('keywords', nargs='?', help='Kata kunci pencarian (opsional)')
    parser.add_argument('--sprint', help='Filter berdasarkan sprint')
    parser.add_argument('--all', action='store_true', help='Ambil semua tiket (butuh konfirmasi)')
    
    args = parser.parse_args()
    
    # Validation
    if not args.keywords and not args.sprint and not args.all:
        print("❌ Error: Minimal berikan kata kunci, --sprint, atau --all")
        parser.print_help()
        sys.exit(1)
    
    # Load credentials
    creds = load_credentials()
    token = creds['notion_token']
    database_id = creds['database_dev']
    sprint_database_id = creds.get('sprint_database_id')
    
    # Confirm if fetching all
    fetch_all = args.all
    if fetch_all:
        if not confirm_fetch_all():
            print("\n❌ Dibatalkan oleh user.")
            sys.exit(0)
        print("\n✅ Melanjutkan...\n")
    
    # Search tickets
    tickets = search_tickets(
        token, 
        database_id,
        sprint_database_id=sprint_database_id,
        keywords=args.keywords, 
        sprint=args.sprint,
        fetch_all=fetch_all
    )
    
    # Display results
    display_tickets(tickets)

if __name__ == "__main__":
    main()
