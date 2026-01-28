#!/bin/bash
# Script untuk copy Notion database query files ke /Users/ahmadfaris/moltbot-workspace/scripts
# Run from: scripts/moltbot_notion_reader/

SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TARGET_DIR="/Users/ahmadfaris/moltbot-workspace/scripts"

echo "🤖 Moltbot/Clawbot Notion Database Reader"
echo "🔄 Copying scripts to target directory"
echo ""
echo "Source: $SOURCE_DIR"
echo "Target: $TARGET_DIR"
echo ""

# Create target directory if not exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "📁 Creating target directory: $TARGET_DIR"
    mkdir -p "$TARGET_DIR"
fi

# List of files to copy
FILES=(
    "notion_database_reader.py"
    "list_all_pages.py"
    "list_dev_tickets.py"
    "list_bug_tickets.py"
    "clawbot_ticket_reader.py"
    "test_notion_connection.py"
    "NOTION_DATABASE_GUIDE.md"
    "README_NOTION_SCRIPTS.md"
    "SUMMARY.md"
    "INDEX.txt"
    "setup_notion_scripts.sh"
)

# Copy files
echo "📦 Copying files..."
for file in "${FILES[@]}"; do
    if [ -f "$SOURCE_DIR/$file" ]; then
        cp "$SOURCE_DIR/$file" "$TARGET_DIR/$file"
        echo "  ✅ $file"
    else
        echo "  ⚠️  $file not found"
    fi
done

# Make shell scripts executable
echo ""
echo "🔧 Making scripts executable..."
chmod +x "$TARGET_DIR/setup_notion_scripts.sh"
chmod +x "$TARGET_DIR"/*.py

echo ""
echo "✅ Copy complete!"
echo ""
echo "Files copied to: $TARGET_DIR"
echo ""
echo "Next steps:"
echo "  1. cd $TARGET_DIR"
echo "  2. export NOTION_TOKEN='your_token_here'"
echo "  3. python3 list_all_pages.py"
echo ""
echo "📚 See NOTION_DATABASE_GUIDE.md for full documentation"
