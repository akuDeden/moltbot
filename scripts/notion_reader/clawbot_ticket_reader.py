#!/usr/bin/env python3
"""
Example: Clawbot/Moltbot Persona - Ticket Reader
Contoh integrasi untuk membaca tiket dan prepare context untuk AI agent

Usage:
    python clawbot_ticket_reader.py --ticket-id <notion_page_id>
    python clawbot_ticket_reader.py --database-id <db_id> --status "In Progress"
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional
from notion_database_reader import NotionDatabaseReader


class ClawbotTicketReader:
    """
    Persona reader untuk Clawbot/Moltbot
    Membaca tiket dan prepare context untuk AI agent
    """
    
    def __init__(self, notion_token: str):
        self.reader = NotionDatabaseReader(notion_token)
        self.notion_token = notion_token
    
    def read_ticket_with_content(self, page_id: str) -> Dict:
        """
        Baca ticket lengkap dengan content dari Notion page
        
        Args:
            page_id: Notion page ID
            
        Returns:
            Dictionary dengan ticket properties dan content
        """
        # Get page content
        page_data = self.reader.get_page_content(page_id)
        
        # Extract properties
        ticket_info = self.reader.extract_page_properties(page_data["page"])
        
        # Convert blocks to markdown
        content_markdown = self.reader.convert_blocks_to_markdown(page_data["blocks"])
        
        ticket_info["content"] = content_markdown
        
        return ticket_info
    
    def prepare_context_for_agent(self, ticket: Dict) -> str:
        """
        Prepare context string untuk AI agent (Clawbot/Moltbot)
        
        Args:
            ticket: Ticket data dengan properties dan content
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        # Header
        context_parts.append("=" * 80)
        context_parts.append("TICKET CONTEXT FOR AI AGENT")
        context_parts.append("=" * 80)
        context_parts.append("")
        
        # Basic info
        title = ticket.get("Name") or ticket.get("Title") or "Untitled Ticket"
        context_parts.append(f"## {title}")
        context_parts.append("")
        
        # Metadata
        ticket_id = ticket.get("ID") or ticket.get("id")
        if ticket_id:
            context_parts.append(f"**Ticket ID:** {ticket_id}")
        
        status = ticket.get("Status")
        if status:
            context_parts.append(f"**Status:** {status}")
        
        priority = ticket.get("Priority")
        if priority:
            context_parts.append(f"**Priority:** {priority}")
        
        assignee = ticket.get("Assignee")
        if assignee:
            if isinstance(assignee, list) and assignee:
                names = [p.get("name", "Unknown") for p in assignee]
                context_parts.append(f"**Assignee:** {', '.join(names)}")
            else:
                context_parts.append(f"**Assignee:** {assignee}")
        
        tags = ticket.get("Tags") or ticket.get("Labels")
        if tags and isinstance(tags, list):
            context_parts.append(f"**Tags:** {', '.join(tags)}")
        
        url = ticket.get("url")
        if url:
            context_parts.append(f"**URL:** {url}")
        
        context_parts.append("")
        context_parts.append("---")
        context_parts.append("")
        
        # Content
        content = ticket.get("content", "")
        if content:
            context_parts.append("## Ticket Content")
            context_parts.append("")
            context_parts.append(content)
        
        context_parts.append("")
        context_parts.append("=" * 80)
        context_parts.append("END OF TICKET CONTEXT")
        context_parts.append("=" * 80)
        
        return "\n".join(context_parts)
    
    def get_tickets_for_review(self, 
                              database_id: str,
                              status: Optional[str] = None,
                              limit: int = 10) -> List[Dict]:
        """
        Get tickets yang perlu di-review
        
        Args:
            database_id: Notion database ID
            status: Filter by status (optional)
            limit: Maximum tickets to fetch
            
        Returns:
            List of tickets dengan full content
        """
        # Build filter
        filter_conditions = None
        if status:
            filter_conditions = {
                "property": "Status",
                "status": {"equals": status}
            }
        
        # Query database
        pages = self.reader.query_database(
            database_id=database_id,
            filter_conditions=filter_conditions,
            page_size=limit
        )
        
        # Get full content untuk setiap ticket
        tickets_with_content = []
        for page in pages:
            page_id = page.get("id")
            try:
                ticket = self.read_ticket_with_content(page_id)
                tickets_with_content.append(ticket)
            except Exception as e:
                print(f"⚠️  Error reading ticket {page_id}: {str(e)}")
                continue
        
        return tickets_with_content
    
    def export_for_agent(self, 
                        tickets: List[Dict],
                        output_file: str,
                        format: str = "json") -> None:
        """
        Export tickets untuk AI agent processing
        
        Args:
            tickets: List of tickets
            output_file: Output file path
            format: Output format ('json' or 'markdown')
        """
        output_path = Path(output_file)
        
        if format == "json":
            # Export as JSON
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(tickets, f, indent=2, ensure_ascii=False)
            print(f"💾 Exported {len(tickets)} tickets to {output_path} (JSON)")
        
        elif format == "markdown":
            # Export as Markdown
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("# Tickets for AI Agent Review\n\n")
                f.write(f"Total Tickets: {len(tickets)}\n")
                f.write(f"Generated: {Path(__file__).name}\n\n")
                f.write("---\n\n")
                
                for i, ticket in enumerate(tickets, 1):
                    context = self.prepare_context_for_agent(ticket)
                    f.write(f"\n\n# Ticket {i}/{len(tickets)}\n\n")
                    f.write(context)
                    f.write("\n\n---\n\n")
            
            print(f"💾 Exported {len(tickets)} tickets to {output_path} (Markdown)")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Clawbot/Moltbot Ticket Reader - Prepare tickets for AI agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Read single ticket dengan full content
  python clawbot_ticket_reader.py --ticket-id abc123

  # Get tickets untuk review (from database)
  python clawbot_ticket_reader.py \\
    --database-id 482be0a206b044d99fff5798db2381e4 \\
    --status "Ready for Review"

  # Export to JSON untuk agent processing
  python clawbot_ticket_reader.py \\
    --database-id 482be0a206b044d99fff5798db2381e4 \\
    --status "In Progress" \\
    --output tickets_for_review.json

  # Export to Markdown dengan full context
  python clawbot_ticket_reader.py \\
    --database-id 482be0a206b044d99fff5798db2381e4 \\
    --output tickets_context.md \\
    --format markdown
        """
    )
    
    # Input options
    parser.add_argument(
        "--ticket-id",
        help="Single ticket/page ID to read"
    )
    
    parser.add_argument(
        "--database-id",
        help="Database ID to query tickets"
    )
    
    # Filter options
    parser.add_argument(
        "--status",
        help="Filter by status"
    )
    
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum tickets to fetch (default: 10)"
    )
    
    # Output options
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path"
    )
    
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="Output format (default: json)"
    )
    
    parser.add_argument(
        "--show-context",
        action="store_true",
        help="Print context to console"
    )
    
    args = parser.parse_args()
    
    # Validation
    if not args.ticket_id and not args.database_id:
        parser.error("Either --ticket-id or --database-id is required")
    
    # Get Notion token
    notion_token = os.getenv("NOTION_TOKEN")
    if not notion_token:
        print("❌ Error: NOTION_TOKEN environment variable not set")
        print("   Set NOTION_TOKEN in your environment")
        print("   Get token from: https://www.notion.so/my-integrations")
        sys.exit(1)
    
    # Initialize reader
    clawbot = ClawbotTicketReader(notion_token)
    
    # Process
    if args.ticket_id:
        # Single ticket mode
        print(f"🔍 Reading ticket: {args.ticket_id}")
        
        try:
            ticket = clawbot.read_ticket_with_content(args.ticket_id)
            
            if args.show_context or not args.output:
                # Print to console
                context = clawbot.prepare_context_for_agent(ticket)
                print("\n")
                print(context)
            
            if args.output:
                # Export
                clawbot.export_for_agent([ticket], args.output, args.format)
            
        except Exception as e:
            print(f"❌ Error reading ticket: {str(e)}")
            sys.exit(1)
    
    elif args.database_id:
        # Database query mode
        print(f"🔍 Querying database: {args.database_id}")
        if args.status:
            print(f"   Status filter: {args.status}")
        print(f"   Limit: {args.limit}")
        print()
        
        try:
            tickets = clawbot.get_tickets_for_review(
                database_id=args.database_id,
                status=args.status,
                limit=args.limit
            )
            
            print(f"\n✅ Found {len(tickets)} tickets")
            
            if args.show_context:
                # Print first ticket as example
                if tickets:
                    print("\n📄 Example - First Ticket Context:")
                    context = clawbot.prepare_context_for_agent(tickets[0])
                    print(context)
            
            if args.output:
                # Export all tickets
                clawbot.export_for_agent(tickets, args.output, args.format)
            elif not args.show_context:
                # Print summary
                print("\n📊 Tickets Summary:")
                for i, ticket in enumerate(tickets, 1):
                    title = ticket.get("Name") or ticket.get("Title") or "Untitled"
                    status = ticket.get("Status") or "No status"
                    print(f"  {i}. {title} [{status}]")
        
        except Exception as e:
            print(f"❌ Error querying database: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    main()
