"""
Notion Database Reader
Script untuk membaca dan query database Notion (Dev Tickets, Bug Tickets, etc.)
Dapat digunakan untuk clawbot/moltbot persona

Usage:
    python notion_database_reader.py --database-id <database_id> [options]
    
Example:
    # List semua dev tickets
    python notion_database_reader.py --database-id 482be0a206b044d99fff5798db2381e4
    
    # Filter berdasarkan status
    python notion_database_reader.py --database-id 482be0a206b044d99fff5798db2381e4 --status "In Progress"
    
    # Export ke JSON
    python notion_database_reader.py --database-id 482be0a206b044d99fff5798db2381e4 --output tickets.json
"""

import os
import sys
import json
import requests
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

class NotionDatabaseReader:
    """
    Class untuk membaca Notion Database dan query tickets
    """
    
    def __init__(self, notion_token: str, notion_version: str = "2022-06-28"):
        """
        Initialize Notion Database Reader
        
        Args:
            notion_token: Notion Integration Token
            notion_version: Notion API version
        """
        self.notion_token = notion_token
        self.notion_version = notion_version
        self.base_url = "https://api.notion.com/v1"
        
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Notion-Version": self.notion_version,
            "Content-Type": "application/json"
        }
    
    def query_database(self, 
                      database_id: str, 
                      filter_conditions: Optional[Dict] = None,
                      sorts: Optional[List[Dict]] = None,
                      page_size: int = 100) -> List[Dict]:
        """
        Query Notion Database dengan filter dan sorting
        
        Args:
            database_id: ID database Notion
            filter_conditions: Filter conditions (Notion API format)
            sorts: Sort conditions (Notion API format)
            page_size: Jumlah results per page (max 100)
            
        Returns:
            List of pages/tickets dari database
        """
        url = f"{self.base_url}/databases/{database_id}/query"
        
        payload = {
            "page_size": min(page_size, 100)
        }
        
        if filter_conditions:
            payload["filter"] = filter_conditions
            
        if sorts:
            payload["sorts"] = sorts
        
        all_results = []
        has_more = True
        start_cursor = None
        
        try:
            while has_more:
                if start_cursor:
                    payload["start_cursor"] = start_cursor
                
                response = requests.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                data = response.json()
                
                all_results.extend(data.get("results", []))
                has_more = data.get("has_more", False)
                start_cursor = data.get("next_cursor")
                
                print(f"📥 Fetched {len(all_results)} tickets so far...")
                
            return all_results
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error querying database: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            raise
    
    def get_page_content(self, page_id: str) -> Dict:
        """
        Get page content (metadata + blocks) dari Notion API
        
        Args:
            page_id: Notion page ID
            
        Returns:
            Dictionary dengan page metadata dan blocks
        """
        try:
            # Get page metadata
            page_url = f"{self.base_url}/pages/{page_id}"
            page_response = requests.get(page_url, headers=self.headers)
            page_response.raise_for_status()
            page_data = page_response.json()
            
            # Get page blocks (content)
            blocks_url = f"{self.base_url}/blocks/{page_id}/children"
            blocks_response = requests.get(blocks_url, headers=self.headers)
            blocks_response.raise_for_status()
            blocks_data = blocks_response.json()
            
            return {
                "page": page_data,
                "blocks": blocks_data["results"]
            }
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching page content: {str(e)}")
            raise
    
    def get_block_children(self, block_id: str) -> List[Dict]:
        """
        Get children blocks untuk nested content
        
        Args:
            block_id: Block ID
            
        Returns:
            List of child blocks
        """
        try:
            children_url = f"{self.base_url}/blocks/{block_id}/children"
            response = requests.get(children_url, headers=self.headers)
            response.raise_for_status()
            children_data = response.json()
            return children_data.get("results", [])
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Warning: Failed to fetch children for block {block_id}: {str(e)}")
            return []
    
    def get_database_info(self, database_id: str) -> Dict:
        """
        Get informasi tentang database (schema, properties, etc.)
        
        Args:
            database_id: ID database Notion
            
        Returns:
            Database metadata
        """
        url = f"{self.base_url}/databases/{database_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error getting database info: {str(e)}")
            raise
    
    def extract_page_properties(self, page: Dict) -> Dict[str, Any]:
        """
        Extract properties dari Notion page ke format yang mudah dibaca
        
        Args:
            page: Notion page object
            
        Returns:
            Dictionary dengan properties yang sudah di-extract
        """
        properties = page.get("properties", {})
        extracted = {
            "id": page.get("id", ""),
            "url": page.get("url", ""),
            "created_time": page.get("created_time", ""),
            "last_edited_time": page.get("last_edited_time", ""),
        }
        
        for prop_name, prop_value in properties.items():
            prop_type = prop_value.get("type")
            
            if prop_type == "title":
                title_texts = prop_value.get("title", [])
                extracted[prop_name] = "".join([t.get("plain_text", "") for t in title_texts])
            
            elif prop_type == "rich_text":
                rich_texts = prop_value.get("rich_text", [])
                extracted[prop_name] = "".join([t.get("plain_text", "") for t in rich_texts])
            
            elif prop_type == "number":
                extracted[prop_name] = prop_value.get("number")
            
            elif prop_type == "select":
                select_obj = prop_value.get("select")
                extracted[prop_name] = select_obj.get("name") if select_obj else None
            
            elif prop_type == "multi_select":
                multi_select_objs = prop_value.get("multi_select", [])
                extracted[prop_name] = [obj.get("name") for obj in multi_select_objs]
            
            elif prop_type == "date":
                date_obj = prop_value.get("date")
                if date_obj:
                    extracted[prop_name] = {
                        "start": date_obj.get("start"),
                        "end": date_obj.get("end")
                    }
                else:
                    extracted[prop_name] = None
            
            elif prop_type == "checkbox":
                extracted[prop_name] = prop_value.get("checkbox", False)
            
            elif prop_type == "url":
                extracted[prop_name] = prop_value.get("url")
            
            elif prop_type == "email":
                extracted[prop_name] = prop_value.get("email")
            
            elif prop_type == "phone_number":
                extracted[prop_name] = prop_value.get("phone_number")
            
            elif prop_type == "status":
                status_obj = prop_value.get("status")
                extracted[prop_name] = status_obj.get("name") if status_obj else None
            
            elif prop_type == "people":
                people_objs = prop_value.get("people", [])
                extracted[prop_name] = [
                    {
                        "id": person.get("id"),
                        "name": person.get("name"),
                        "type": person.get("type")
                    }
                    for person in people_objs
                ]
            
            elif prop_type == "relation":
                relation_objs = prop_value.get("relation", [])
                extracted[prop_name] = [rel.get("id") for rel in relation_objs]
            
            elif prop_type == "formula":
                formula_type = prop_value.get("formula", {}).get("type")
                formula_value = prop_value.get("formula", {})
                if formula_type in formula_value:
                    extracted[prop_name] = formula_value.get(formula_type)
            
            elif prop_type == "rollup":
                rollup_type = prop_value.get("rollup", {}).get("type")
                rollup_value = prop_value.get("rollup", {})
                if rollup_type in rollup_value:
                    extracted[prop_name] = rollup_value.get(rollup_type)
            
            else:
                # Fallback untuk tipe lain
                extracted[prop_name] = str(prop_value)
        
        return extracted
    
    def convert_blocks_to_markdown(self, blocks: List[Dict], indent_level: int = 0) -> str:
        """
        Convert Notion blocks ke markdown format dengan recursive children
        
        Args:
            blocks: List of Notion block objects
            indent_level: Current indentation level
            
        Returns:
            Markdown string
        """
        markdown_content = ""
        indent = "  " * indent_level
        
        for block in blocks:
            block_type = block.get("type", "")
            has_children = block.get("has_children", False)
            block_id = block.get("id", "")
            
            if block_type == "paragraph":
                text = self._extract_rich_text(block.get("paragraph", {}).get("rich_text", []))
                if text.strip():
                    markdown_content += f"{indent}{text}\n\n"
            
            elif block_type == "heading_1":
                text = self._extract_rich_text(block.get("heading_1", {}).get("rich_text", []))
                markdown_content += f"{indent}# {text}\n\n"
            
            elif block_type == "heading_2":
                text = self._extract_rich_text(block.get("heading_2", {}).get("rich_text", []))
                markdown_content += f"{indent}## {text}\n\n"
            
            elif block_type == "heading_3":
                text = self._extract_rich_text(block.get("heading_3", {}).get("rich_text", []))
                markdown_content += f"{indent}### {text}\n\n"
            
            elif block_type == "bulleted_list_item":
                text = self._extract_rich_text(block.get("bulleted_list_item", {}).get("rich_text", []))
                markdown_content += f"{indent}- {text}\n"
                
                if has_children and block_id:
                    children = self.get_block_children(block_id)
                    if children:
                        children_content = self.convert_blocks_to_markdown(children, indent_level + 1)
                        markdown_content += children_content
            
            elif block_type == "numbered_list_item":
                text = self._extract_rich_text(block.get("numbered_list_item", {}).get("rich_text", []))
                markdown_content += f"{indent}1. {text}\n"
                
                if has_children and block_id:
                    children = self.get_block_children(block_id)
                    if children:
                        children_content = self.convert_blocks_to_markdown(children, indent_level + 1)
                        markdown_content += children_content
            
            elif block_type == "to_do":
                text = self._extract_rich_text(block.get("to_do", {}).get("rich_text", []))
                checked = block.get("to_do", {}).get("checked", False)
                checkbox = "[x]" if checked else "[ ]"
                markdown_content += f"{indent}- {checkbox} {text}\n"
                
                if has_children and block_id:
                    children = self.get_block_children(block_id)
                    if children:
                        children_content = self.convert_blocks_to_markdown(children, indent_level + 1)
                        markdown_content += children_content
            
            elif block_type == "code":
                language = block.get("code", {}).get("language", "")
                text = self._extract_rich_text(block.get("code", {}).get("rich_text", []))
                markdown_content += f"{indent}```{language}\n{text}\n```\n\n"
            
            elif block_type == "quote":
                text = self._extract_rich_text(block.get("quote", {}).get("rich_text", []))
                markdown_content += f"{indent}> {text}\n\n"
            
            elif block_type == "callout":
                text = self._extract_rich_text(block.get("callout", {}).get("rich_text", []))
                icon = block.get("callout", {}).get("icon", {})
                icon_text = ""
                if icon.get("type") == "emoji":
                    icon_text = icon.get("emoji", "")
                markdown_content += f"{indent}{icon_text} **{text}**\n\n"
                
                if has_children and block_id:
                    children = self.get_block_children(block_id)
                    if children:
                        children_content = self.convert_blocks_to_markdown(children, indent_level + 1)
                        markdown_content += children_content
            
            elif block_type == "divider":
                markdown_content += f"{indent}---\n\n"
            
            elif block_type == "image":
                image_data = block.get("image", {})
                image_type = image_data.get("type")
                url = ""
                if image_type == "file":
                    url = image_data.get("file", {}).get("url", "")
                elif image_type == "external":
                    url = image_data.get("external", {}).get("url", "")
                
                caption_parts = image_data.get("caption", [])
                caption = self._extract_rich_text(caption_parts) if caption_parts else "Image"
                
                if url:
                    markdown_content += f"{indent}![{caption}]({url})\n\n"
        
        return markdown_content
    
    def _extract_rich_text(self, rich_text_array: List[Dict]) -> str:
        """
        Extract plain text dari Notion rich text format dengan formatting
        
        Args:
            rich_text_array: Array of rich text objects
            
        Returns:
            Formatted text string
        """
        text_parts = []
        
        for text_obj in rich_text_array:
            plain_text = text_obj.get("plain_text", "")
            annotations = text_obj.get("annotations", {})
            
            # Apply formatting
            if annotations.get("bold"):
                plain_text = f"**{plain_text}**"
            if annotations.get("italic"):
                plain_text = f"*{plain_text}*"
            if annotations.get("strikethrough"):
                plain_text = f"~~{plain_text}~~"
            if annotations.get("code"):
                plain_text = f"`{plain_text}`"
            
            # Handle links
            if text_obj.get("href"):
                plain_text = f"[{plain_text}]({text_obj.get('href')})"
            
            text_parts.append(plain_text)
        
        return "".join(text_parts)
    
    def format_ticket_summary(self, ticket: Dict) -> str:
        """
        Format ticket menjadi string summary yang mudah dibaca
        
        Args:
            ticket: Extracted ticket properties
            
        Returns:
            Formatted string summary
        """
        lines = []
        lines.append("=" * 80)
        
        # Title/Name
        title = ticket.get("Name") or ticket.get("Title") or ticket.get("title") or "Untitled"
        lines.append(f"📌 {title}")
        lines.append("-" * 80)
        
        # Status
        status = ticket.get("Status") or ticket.get("status")
        if status:
            lines.append(f"Status: {status}")
        
        # ID/Number
        ticket_id = ticket.get("ID") or ticket.get("Ticket ID") or ticket.get("id")
        if ticket_id:
            lines.append(f"ID: {ticket_id}")
        
        # Priority
        priority = ticket.get("Priority") or ticket.get("priority")
        if priority:
            lines.append(f"Priority: {priority}")
        
        # Assignee
        assignee = ticket.get("Assignee") or ticket.get("assignee")
        if assignee:
            if isinstance(assignee, list) and assignee:
                names = [p.get("name", "Unknown") for p in assignee]
                lines.append(f"Assignee: {', '.join(names)}")
            else:
                lines.append(f"Assignee: {assignee}")
        
        # Tags/Labels
        tags = ticket.get("Tags") or ticket.get("Labels") or ticket.get("tags")
        if tags and isinstance(tags, list):
            lines.append(f"Tags: {', '.join(tags)}")
        
        # Description
        description = ticket.get("Description") or ticket.get("description")
        if description:
            lines.append(f"Description: {description[:200]}..." if len(description) > 200 else f"Description: {description}")
        
        # URL
        url = ticket.get("url")
        if url:
            lines.append(f"🔗 {url}")
        
        # Timestamps
        created = ticket.get("created_time")
        if created:
            lines.append(f"Created: {created}")
        
        edited = ticket.get("last_edited_time")
        if edited:
            lines.append(f"Last Edited: {edited}")
        
        lines.append("=" * 80)
        return "\n".join(lines)


def build_status_filter(status: str) -> Dict:
    """
    Build filter untuk status property
    
    Args:
        status: Status value to filter
        
    Returns:
        Filter object untuk Notion API
    """
    return {
        "property": "Status",
        "status": {
            "equals": status
        }
    }


def build_multi_select_filter(property_name: str, value: str) -> Dict:
    """
    Build filter untuk multi-select property
    
    Args:
        property_name: Property name (e.g., "Tags", "Labels")
        value: Value to filter
        
    Returns:
        Filter object untuk Notion API
    """
    return {
        "property": property_name,
        "multi_select": {
            "contains": value
        }
    }


def build_title_search_filter(search_text: str) -> Dict:
    """
    Build filter untuk mencari di title/name
    
    Args:
        search_text: Text to search in title
        
    Returns:
        Filter object untuk Notion API
    """
    return {
        "property": "Name",
        "title": {
            "contains": search_text
        }
    }


def main():
    """
    Main function untuk CLI
    """
    parser = argparse.ArgumentParser(
        description="Notion Database Reader - Query Notion databases for tickets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all tickets dari database
  python notion_database_reader.py --database-id 482be0a206b044d99fff5798db2381e4
  
  # Filter by status
  python notion_database_reader.py --database-id 482be0a206b044d99fff5798db2381e4 --status "In Progress"
  
  # Search by title
  python notion_database_reader.py --database-id 482be0a206b044d99fff5798db2381e4 --search "bug"
  
  # Export to JSON file
  python notion_database_reader.py --database-id 482be0a206b044d99fff5798db2381e4 --output tickets.json
  
  # Show database schema
  python notion_database_reader.py --database-id 482be0a206b044d99fff5798db2381e4 --show-schema
        """
    )
    
    parser.add_argument(
        "--database-id",
        required=True,
        help="Notion Database ID (e.g., 482be0a206b044d99fff5798db2381e4)"
    )
    
    parser.add_argument(
        "--notion-token",
        help="Notion Integration Token (or set NOTION_TOKEN env var)"
    )
    
    parser.add_argument(
        "--status",
        help="Filter by status (e.g., 'In Progress', 'Done')"
    )
    
    parser.add_argument(
        "--search",
        help="Search text in title/name"
    )
    
    parser.add_argument(
        "--tag",
        help="Filter by tag/label"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (JSON format)"
    )
    
    parser.add_argument(
        "--show-schema",
        action="store_true",
        help="Show database schema/properties"
    )
    
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of tickets to fetch (default: 100)"
    )
    
    args = parser.parse_args()
    
    # Get Notion token
    notion_token = args.notion_token or os.getenv("NOTION_TOKEN")
    if not notion_token:
        print("❌ Error: NOTION_TOKEN not provided")
        print("   Set NOTION_TOKEN environment variable or use --notion-token")
        print("   Get token from: https://www.notion.so/my-integrations")
        sys.exit(1)
    
    # Initialize reader
    reader = NotionDatabaseReader(notion_token)
    
    # Show schema if requested
    if args.show_schema:
        print(f"📊 Fetching database schema for {args.database_id}...\n")
        try:
            db_info = reader.get_database_info(args.database_id)
            print("=" * 80)
            print(f"Database: {db_info.get('title', [{}])[0].get('plain_text', 'Untitled')}")
            print("=" * 80)
            print("\nProperties:")
            for prop_name, prop_data in db_info.get("properties", {}).items():
                prop_type = prop_data.get("type")
                print(f"  • {prop_name}: {prop_type}")
            print("\n")
        except Exception as e:
            print(f"❌ Failed to get database schema: {str(e)}")
            sys.exit(1)
    
    # Build filters
    filters = []
    if args.status:
        filters.append(build_status_filter(args.status))
    if args.search:
        filters.append(build_title_search_filter(args.search))
    if args.tag:
        filters.append(build_multi_select_filter("Tags", args.tag))
    
    # Combine filters dengan AND
    filter_conditions = None
    if filters:
        if len(filters) == 1:
            filter_conditions = filters[0]
        else:
            filter_conditions = {
                "and": filters
            }
    
    # Query database
    print(f"🔍 Querying database {args.database_id}...")
    if filter_conditions:
        print(f"   Filters: {json.dumps(filter_conditions, indent=2)}")
    print()
    
    try:
        pages = reader.query_database(
            database_id=args.database_id,
            filter_conditions=filter_conditions,
            page_size=args.limit
        )
        
        print(f"\n✅ Found {len(pages)} tickets\n")
        
        # Extract properties
        tickets = [reader.extract_page_properties(page) for page in pages]
        
        # Output
        if args.output:
            # Save to JSON file
            output_path = Path(args.output)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(tickets, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved to {output_path}")
        else:
            # Print to console
            for ticket in tickets:
                print(reader.format_ticket_summary(ticket))
                print()
        
    except Exception as e:
        print(f"❌ Failed to query database: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
