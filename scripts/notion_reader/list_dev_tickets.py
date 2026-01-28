"""
List Development Tickets from Notion Database
Script khusus untuk membaca dev tickets

Usage:
    python list_dev_tickets.py [--status STATUS] [--output FILE]
"""

import os
import sys
from notion_database_reader import NotionDatabaseReader, build_status_filter

# Database IDs untuk dev tickets
DEV_DATABASE_IDS = [
    "482be0a206b044d99fff5798db2381e4",  # Dev ticket database 1
    "32e29af7d7dd4df69310270de8830d1a",  # Dev tiket database 2
]


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="List Development Tickets from Notion"
    )
    
    parser.add_argument(
        "--database-id",
        help="Specific database ID (default: uses all configured dev databases)"
    )
    
    parser.add_argument(
        "--status",
        help="Filter by status (e.g., 'In Progress', 'To Do', 'Done')"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        help="Output JSON file"
    )
    
    parser.add_argument(
        "--show-all",
        action="store_true",
        help="Show all dev tickets from all databases"
    )
    
    args = parser.parse_args()
    
    # Get Notion token
    notion_token = os.getenv("NOTION_TOKEN")
    if not notion_token:
        print("❌ Error: NOTION_TOKEN environment variable not set")
        print("   Set NOTION_TOKEN in your environment or .env file")
        print("   Get token from: https://www.notion.so/my-integrations")
        sys.exit(1)
    
    # Initialize reader
    reader = NotionDatabaseReader(notion_token)
    
    # Determine which databases to query
    if args.database_id:
        databases = [args.database_id]
    else:
        databases = DEV_DATABASE_IDS
    
    # Build filter
    filter_conditions = None
    if args.status:
        filter_conditions = build_status_filter(args.status)
    
    # Query all databases
    all_tickets = []
    
    for db_id in databases:
        print(f"🔍 Querying dev database: {db_id}")
        try:
            pages = reader.query_database(
                database_id=db_id,
                filter_conditions=filter_conditions,
                page_size=100
            )
            
            tickets = [reader.extract_page_properties(page) for page in pages]
            all_tickets.extend(tickets)
            
            print(f"   ✅ Found {len(tickets)} tickets")
        except Exception as e:
            print(f"   ⚠️  Error querying database {db_id}: {str(e)}")
            continue
    
    print(f"\n📊 Total: {len(all_tickets)} dev tickets")
    
    # Output
    if args.output:
        import json
        from pathlib import Path
        
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_tickets, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved to {output_path}")
    else:
        # Print summary
        print("\n" + "=" * 80)
        for ticket in all_tickets:
            print(reader.format_ticket_summary(ticket))
            print()


if __name__ == "__main__":
    main()
