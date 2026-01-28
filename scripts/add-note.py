#!/usr/bin/env python3
"""
Add a note/block to a Notion page
Usage: python3 add-note.py "PAGE_URL" "NOTE_CONTENT"
"""
import sys
import json
import re

try:
    from notion_client import Client
except ImportError:
    print("❌ Error: notion-client not installed")
    print("Install with: pip install notion-client")
    sys.exit(1)

CREDENTIALS_FILE = "/Users/ahmadfaris/moltbot-workspace/notion-credentials.json"

def load_credentials():
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: {CREDENTIALS_FILE} not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: {CREDENTIALS_FILE} is not valid JSON")
        sys.exit(1)

def extract_page_id_from_url(url):
    """Extract page ID from Notion URL"""
    # Pattern: https://www.notion.so/Page-Title-XXXXXXXXX
    # Page ID is 32-character hex at the end of the URL
    match = re.search(r'([a-f0-9]{32})$', url)
    if match:
        return match.group(1)
    return None

def add_note_to_page(notion, page_id, note_content):
    """Add note as block to the bottom of the page"""
    try:
        # Add a heading for the note
        notion.blocks.children.append(
            block_id=page_id,
            children=[
                {
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": "📝 QA Test Requirements"
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": note_content
                                }
                            }
                        ],
                        "icon": {
                            "emoji": "🧪"
                        },
                        "color": "blue_background"
                    }
                }
            ]
        )

        return True

    except Exception as e:
        print(f"❌ Error adding note to page: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 add-note.py 'PAGE_URL' 'NOTE_CONTENT'")
        print("Example: python3 add-note.py 'https://www.notion.so/Page-Title-XXXXXXXXX' 'Test this feature'")
        sys.exit(1)

    page_url = sys.argv[1]
    note_content = sys.argv[2]

    # Extract page ID from URL
    page_id = extract_page_id_from_url(page_url)
    if not page_id:
        print(f"❌ Error: Could not extract page ID from URL: {page_url}")
        sys.exit(1)

    # Load credentials
    creds = load_credentials()
    notion_token = creds.get("notion_token")

    if not notion_token:
        print("❌ Error: Notion token not configured")
        sys.exit(1)

    # Initialize Notion client
    notion = Client(auth=notion_token)

    print(f"📝 Adding note to page...")
    print(f"   Page ID: {page_id}")
    print()

    # Add note
    success = add_note_to_page(notion, page_id, note_content)

    if success:
        print(f"✅ Note berhasil ditambahkan ke Notion!")
        print(f"   URL: {page_url}")
        print(f"\n📋 Note: {note_content[:100]}...")
    else:
        print("❌ Failed to add note to Notion page")
        sys.exit(1)

if __name__ == "__main__":
    main()
