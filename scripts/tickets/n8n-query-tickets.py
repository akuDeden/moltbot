#!/usr/bin/env python3
"""
N8N Dynamic Tickets Query Client
Wrapper script untuk query tickets via n8n webhook dengan CLI interface

Usage:
    python3 n8n-query-tickets.py --sprint "Sprint 2"
    python3 n8n-query-tickets.py --status "In Progress" --assignee "Ahmad"
    python3 n8n-query-tickets.py --keywords "sales" --limit 20
"""

import argparse
import httpx
import json
import os
import sys
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass

# N8N webhook URL - configure this
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL', 'https://your-n8n-instance.com/webhook/query-tickets')

def query_tickets(
    database_id=None,
    keywords=None,
    sprint=None,
    status=None,
    assignee=None,
    priority=None,
    tags=None,
    limit=100,
    sort_by='last_edited_time',
    sort_direction='descending',
    output_format='text'
):
    """Query tickets via n8n webhook"""
    
    # Build request payload
    payload = {}
    
    if database_id:
        payload['database_id'] = database_id
    if keywords:
        payload['keywords'] = keywords
    if sprint:
        payload['sprint'] = sprint
    if status:
        payload['status'] = status
    if assignee:
        payload['assignee'] = assignee
    if priority:
        payload['priority'] = priority
    if tags:
        payload['tags'] = tags if isinstance(tags, list) else [tags]
    if limit:
        payload['limit'] = limit
    if sort_by:
        payload['sort_by'] = sort_by
    if sort_direction:
        payload['sort_direction'] = sort_direction
    
    try:
        # Make request to n8n webhook
        response = httpx.post(
            N8N_WEBHOOK_URL,
            json=payload,
            timeout=30.0
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if output_format == 'text':
                # Print formatted text message
                print(data['message'])
                return data['data']['tickets']
            
            elif output_format == 'json':
                # Print full JSON response
                print(json.dumps(data, indent=2, ensure_ascii=False))
                return data['data']['tickets']
            
            elif output_format == 'compact':
                # Print compact ticket list
                tickets = data['data']['tickets']
                print(f"\n📊 Found {len(tickets)} ticket(s)\n")
                for idx, ticket in enumerate(tickets, 1):
                    print(f"{idx}. {ticket['title']}")
                    print(f"   Status: {ticket['status']} | Sprint: {ticket['sprint']} | Assignee: {ticket['assignee']}")
                    print(f"   🔗 {ticket['url']}\n")
                return tickets
            
            elif output_format == 'urls':
                # Print only URLs (useful for piping)
                tickets = data['data']['tickets']
                for ticket in tickets:
                    print(ticket['url'])
                return tickets
        
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(response.text)
            return None
    
    except httpx.TimeoutException:
        print("❌ Error: Request timeout")
        return None
    except httpx.RequestError as e:
        print(f"❌ Error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description='Query Notion tickets via n8n webhook',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --sprint "Sprint 2"
  %(prog)s --status "In Progress" --assignee "Ahmad"
  %(prog)s --keywords "sales" --limit 20
  %(prog)s --sprint "Sprint 2" --status "Done" --output json
  %(prog)s --all --output urls | xargs open  # Open all ticket URLs
        """
    )
    
    # Filter parameters
    parser.add_argument('--database-id', help='Notion database ID')
    parser.add_argument('--keywords', '-k', help='Search keywords in title')
    parser.add_argument('--sprint', '-s', help='Filter by sprint name')
    parser.add_argument('--status', help='Filter by status')
    parser.add_argument('--assignee', '-a', help='Filter by assignee name')
    parser.add_argument('--priority', '-p', help='Filter by priority')
    parser.add_argument('--tags', '-t', nargs='+', help='Filter by tags')
    
    # Query options
    parser.add_argument('--limit', '-l', type=int, default=100, help='Maximum number of results (default: 100)')
    parser.add_argument('--sort-by', default='last_edited_time', choices=['created_time', 'last_edited_time'], 
                       help='Sort field (default: last_edited_time)')
    parser.add_argument('--sort-direction', default='descending', choices=['ascending', 'descending'],
                       help='Sort direction (default: descending)')
    
    # Output format
    parser.add_argument('--output', '-o', default='text', choices=['text', 'json', 'compact', 'urls'],
                       help='Output format (default: text)')
    
    # Shortcuts
    parser.add_argument('--all', action='store_true', help='Get all tickets (no filters)')
    
    args = parser.parse_args()
    
    # Validate webhook URL
    if 'your-n8n-instance.com' in N8N_WEBHOOK_URL:
        print("❌ Error: N8N_WEBHOOK_URL not configured")
        print("Set N8N_WEBHOOK_URL environment variable or edit this script")
        sys.exit(1)
    
    # Execute query
    tickets = query_tickets(
        database_id=args.database_id,
        keywords=args.keywords,
        sprint=args.sprint,
        status=args.status,
        assignee=args.assignee,
        priority=args.priority,
        tags=args.tags,
        limit=args.limit,
        sort_by=args.sort_by,
        sort_direction=args.sort_direction,
        output_format=args.output
    )
    
    if tickets is None:
        sys.exit(1)

if __name__ == '__main__':
    main()
