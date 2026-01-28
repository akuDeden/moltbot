"""
List Bug Tickets from Notion Database
Script khusus untuk membaca bug tickets

Usage:
    python list_bug_tickets.py [--status STATUS] [--priority PRIORITY] [--output FILE]
"""

import os
import sys
from notion_database_reader import NotionDatabaseReader, build_status_filter


# Database ID untuk bug tickets (customize sesuai kebutuhan)
BUG_DATABASE_ID = os.getenv("BUG_DATABASE_ID", "YOUR_BUG_DATABASE_ID_HERE")


def build_priority_filter(priority: str):
    """Build filter untuk priority"""
    return {
        "property": "Priority",
        "select": {
            "equals": priority
        }
    }


def main():
    import argparse
    import json
    from pathlib import Path
    
    parser = argparse.ArgumentParser(
        description="List Bug Tickets from Notion"
    )
    
    parser.add_argument(
        "--database-id",
        default=BUG_DATABASE_ID,
        help=f"Bug database ID (default: {BUG_DATABASE_ID})"
    )
    
    parser.add_argument(
        "--status",
        help="Filter by status (e.g., 'Open', 'In Progress', 'Resolved')"
    )
    
    parser.add_argument(
        "--priority",
        help="Filter by priority (e.g., 'High', 'Medium', 'Low', 'Critical')"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        help="Output JSON file"
    )
    
    args = parser.parse_args()
    
    # Get Notion token
    notion_token = os.getenv("NOTION_TOKEN")
    if not notion_token:
        print("❌ Error: NOTION_TOKEN environment variable not set")
        print("   Set NOTION_TOKEN in your environment or .env file")
        print("   Get token from: https://www.notion.so/my-integrations")
        sys.exit(1)
    
    if args.database_id == "YOUR_BUG_DATABASE_ID_HERE":
        print("⚠️  Warning: Using placeholder BUG_DATABASE_ID")
        print("   Set BUG_DATABASE_ID environment variable or use --database-id")
    
    # Initialize reader
    reader = NotionDatabaseReader(notion_token)
    
    # Build filters
    filters = []
    if args.status:
        filters.append(build_status_filter(args.status))
    if args.priority:
        filters.append(build_priority_filter(args.priority))
    
    # Combine filters
    filter_conditions = None
    if filters:
        if len(filters) == 1:
            filter_conditions = filters[0]
        else:
            filter_conditions = {"and": filters}
    
    # Query database
    print(f"🔍 Querying bug database: {args.database_id}")
    if filter_conditions:
        print(f"   Filters: {json.dumps(filter_conditions, indent=2)}")
    
    try:
        pages = reader.query_database(
            database_id=args.database_id,
            filter_conditions=filter_conditions,
            page_size=100
        )
        
        tickets = [reader.extract_page_properties(page) for page in pages]
        
        print(f"\n✅ Found {len(tickets)} bug tickets")
        
        # Output
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(tickets, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved to {output_path}")
        else:
            # Print summary
            print("\n" + "=" * 80)
            for ticket in tickets:
                print(reader.format_ticket_summary(ticket))
                print()
                
    except Exception as e:
        print(f"❌ Failed to query database: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
