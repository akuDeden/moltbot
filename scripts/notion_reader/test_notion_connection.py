#!/usr/bin/env python3
"""
Test Notion Connection
Quick script untuk test apakah NOTION_TOKEN sudah benar dan connection berhasil
"""

import os
import sys
import requests

def test_notion_connection():
    """Test Notion API connection"""
    
    print("🔍 Testing Notion API Connection...")
    print("=" * 60)
    
    # Check token
    notion_token = os.getenv("NOTION_TOKEN")
    if not notion_token:
        print("❌ NOTION_TOKEN not found!")
        print("\nTo fix:")
        print("  export NOTION_TOKEN='your_token_here'")
        print("\nGet token from: https://www.notion.so/my-integrations")
        return False
    
    print(f"✅ NOTION_TOKEN found: {notion_token[:20]}...{notion_token[-4:]}")
    
    # Test API call
    print("\n🌐 Testing API access...")
    
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    try:
        # Simple search call
        response = requests.post(
            "https://api.notion.com/v1/search",
            headers=headers,
            json={"page_size": 1}
        )
        
        if response.status_code == 200:
            data = response.json()
            results_count = len(data.get("results", []))
            
            print(f"✅ API connection successful!")
            print(f"   Found {results_count} accessible pages/databases")
            
            if results_count > 0:
                print("\n📄 Sample result:")
                sample = data["results"][0]
                obj_type = sample.get("object", "unknown")
                obj_id = sample.get("id", "unknown")
                print(f"   Type: {obj_type}")
                print(f"   ID: {obj_id}")
            
            print("\n✨ Connection test PASSED!")
            print("\nYou can now use:")
            print("  • python3 list_all_pages.py")
            print("  • python3 list_dev_tickets.py")
            print("  • python3 notion_database_reader.py --database-id <ID>")
            
            return True
            
        elif response.status_code == 401:
            print("❌ Authentication failed!")
            print("   Token is invalid or expired")
            print("\nTo fix:")
            print("  1. Go to https://www.notion.so/my-integrations")
            print("  2. Generate new Integration Token")
            print("  3. export NOTION_TOKEN='new_token'")
            return False
            
        else:
            print(f"❌ API error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {str(e)}")
        print("\nCheck:")
        print("  • Internet connection")
        print("  • Firewall settings")
        print("  • Notion API status")
        return False


def test_dev_databases():
    """Test configured dev database IDs"""
    
    print("\n" + "=" * 60)
    print("🗂️  Testing Dev Database IDs...")
    print("=" * 60)
    
    notion_token = os.getenv("NOTION_TOKEN")
    if not notion_token:
        print("⚠️  Skip: NOTION_TOKEN not set")
        return
    
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    dev_databases = [
        ("Dev Database 1", "482be0a206b044d99fff5798db2381e4"),
        ("Dev Database 2", "32e29af7d7dd4df69310270de8830d1a"),
    ]
    
    for name, db_id in dev_databases:
        try:
            response = requests.get(
                f"https://api.notion.com/v1/databases/{db_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                db_data = response.json()
                title_parts = db_data.get("title", [])
                db_title = "".join([t.get("plain_text", "") for t in title_parts])
                print(f"\n✅ {name}: {db_id}")
                print(f"   Title: {db_title or 'Untitled'}")
                print(f"   Properties: {len(db_data.get('properties', {}))} fields")
                
            elif response.status_code == 404:
                print(f"\n⚠️  {name}: {db_id}")
                print(f"   Status: Not found or not shared with integration")
                print(f"   Action: Share database with your integration")
                
            else:
                print(f"\n❌ {name}: {db_id}")
                print(f"   Status: {response.status_code}")
                
        except Exception as e:
            print(f"\n❌ {name}: Error - {str(e)}")


def main():
    print("🤖 Notion Database Reader - Connection Test")
    print("=" * 60)
    print()
    
    # Test connection
    connection_ok = test_notion_connection()
    
    if connection_ok:
        # Test databases
        test_dev_databases()
    
    print("\n" + "=" * 60)
    if connection_ok:
        print("✅ Setup Complete!")
    else:
        print("❌ Setup Issues - Please fix errors above")
    print("=" * 60)


if __name__ == "__main__":
    main()
