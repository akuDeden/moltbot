"""
List All Pages from Notion Workspace
Script untuk explore semua pages yang accessible

Usage:
    python list_all_pages.py [--search QUERY] [--output FILE]
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional


def list_all_pages(notion_token: str, 
                   search_query: Optional[str] = None,
                   page_size: int = 100) -> List[Dict]:
    """
    List all pages accessible by the integration
    
    Args:
        notion_token: Notion Integration Token
        search_query: Optional search query
        page_size: Results per page
        
    Returns:
        List of pages
    """
    base_url = "https://api.notion.com/v1"
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    url = f"{base_url}/search"
    
    payload = {
        "page_size": min(page_size, 100)
    }
    
    if search_query:
        payload["query"] = search_query
    
    all_results = []
    has_more = True
    start_cursor = None
    
    try:
        while has_more:
            if start_cursor:
                payload["start_cursor"] = start_cursor
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            all_results.extend(data.get("results", []))
            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor")
            
            print(f"📥 Fetched {len(all_results)} pages so far...")
            
        return all_results
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error searching pages: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        raise


def extract_page_info(page: Dict) -> Dict:
    """Extract basic info from page"""
    page_type = page.get("object", "")
    page_id = page.get("id", "")
    url = page.get("url", "")
    
    info = {
        "id": page_id,
        "type": page_type,
        "url": url,
        "created_time": page.get("created_time", ""),
        "last_edited_time": page.get("last_edited_time", ""),
    }
    
    # Extract title
    if page_type == "page":
        properties = page.get("properties", {})
        title_prop = properties.get("title", {})
        title_texts = title_prop.get("title", [])
        info["title"] = "".join([t.get("plain_text", "") for t in title_texts])
    
    elif page_type == "database":
        title_parts = page.get("title", [])
        info["title"] = "".join([t.get("plain_text", "") for t in title_parts])
        info["properties"] = list(page.get("properties", {}).keys())
    
    return info


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="List all Notion pages accessible by integration"
    )
    
    parser.add_argument(
        "--search",
        help="Search query"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        help="Output JSON file"
    )
    
    parser.add_argument(
        "--show-databases",
        action="store_true",
        help="Show only databases"
    )
    
    parser.add_argument(
        "--show-pages",
        action="store_true",
        help="Show only pages"
    )
    
    args = parser.parse_args()
    
    # Get Notion token
    notion_token = os.getenv("NOTION_TOKEN")
    if not notion_token:
        print("❌ Error: NOTION_TOKEN environment variable not set")
        print("   Set NOTION_TOKEN in your environment or .env file")
        print("   Get token from: https://www.notion.so/my-integrations")
        sys.exit(1)
    
    # Search pages
    print("🔍 Searching Notion workspace...")
    if args.search:
        print(f"   Query: {args.search}")
    print()
    
    try:
        pages = list_all_pages(
            notion_token=notion_token,
            search_query=args.search
        )
        
        print(f"\n✅ Found {len(pages)} pages/databases")
        
        # Extract info
        pages_info = [extract_page_info(page) for page in pages]
        
        # Filter if requested
        if args.show_databases:
            pages_info = [p for p in pages_info if p["type"] == "database"]
            print(f"   Filtered to {len(pages_info)} databases")
        elif args.show_pages:
            pages_info = [p for p in pages_info if p["type"] == "page"]
            print(f"   Filtered to {len(pages_info)} pages")
        
        # Output
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(pages_info, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved to {output_path}")
        else:
            # Print to console
            print("\n" + "=" * 80)
            
            # Group by type
            databases = [p for p in pages_info if p["type"] == "database"]
            regular_pages = [p for p in pages_info if p["type"] == "page"]
            
            if databases:
                print(f"\n📊 DATABASES ({len(databases)}):")
                print("-" * 80)
                for db in databases:
                    print(f"\n  📁 {db.get('title', 'Untitled')}")
                    print(f"     ID: {db['id']}")
                    print(f"     URL: {db['url']}")
                    if db.get('properties'):
                        print(f"     Properties: {', '.join(db['properties'][:5])}...")
            
            if regular_pages:
                print(f"\n📄 PAGES ({len(regular_pages)}):")
                print("-" * 80)
                for page in regular_pages[:20]:  # Limit to first 20
                    print(f"\n  📄 {page.get('title', 'Untitled')}")
                    print(f"     ID: {page['id']}")
                    print(f"     URL: {page['url']}")
                
                if len(regular_pages) > 20:
                    print(f"\n  ... and {len(regular_pages) - 20} more pages")
            
            print("\n" + "=" * 80)
            
    except Exception as e:
        print(f"❌ Failed to search pages: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
