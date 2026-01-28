#!/bin/bash
# Quick setup script untuk Notion database query

echo "🚀 Setting up Notion Database Query Scripts"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.7+"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install requests

# Check for NOTION_TOKEN
echo ""
if [ -z "$NOTION_TOKEN" ]; then
    echo "⚠️  NOTION_TOKEN not set"
    echo ""
    echo "To set it:"
    echo "  1. Get token from: https://www.notion.so/my-integrations"
    echo "  2. Run: export NOTION_TOKEN=\"your_token_here\""
    echo "  3. Or create .env file with NOTION_TOKEN=your_token"
    echo ""
else
    echo "✅ NOTION_TOKEN is set"
fi

# Test connection
echo ""
echo "🔍 Testing Notion API connection..."

if [ ! -z "$NOTION_TOKEN" ]; then
    python3 list_all_pages.py --show-databases 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Setup complete! Ready to use."
        echo ""
        echo "Try these commands:"
        echo "  python3 list_all_pages.py"
        echo "  python3 list_dev_tickets.py"
        echo "  python3 notion_database_reader.py --database-id 482be0a206b044d99fff5798db2381e4"
    else
        echo ""
        echo "⚠️  Connection test failed. Please check your NOTION_TOKEN"
    fi
else
    echo "⚠️  Skipping connection test (NOTION_TOKEN not set)"
    echo ""
    echo "After setting NOTION_TOKEN, run:"
    echo "  ./setup_notion_scripts.sh"
fi

echo ""
echo "📚 See NOTION_DATABASE_GUIDE.md for full documentation"
