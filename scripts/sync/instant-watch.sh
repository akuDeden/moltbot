#!/bin/bash
# Watch memory file and auto-sync INSTANTLY when changed

MEMORY_FILE="/Users/ahmadfaris/moltbot-workspace/memory/$(date +%Y-%m-%d).md"
SYNC_SCRIPT="/Users/ahmadfaris/moltbot-workspace/scripts/auto-sync-memory-to-sheet.py"
export PATH="/opt/homebrew/bin:/Users/ahmadfaris/.pyenv/shims:$PATH"

echo "👀 Watching: $MEMORY_FILE"
echo "🔄 Will auto-sync instantly on changes..."
echo ""

# Use fswatch if available, otherwise fallback to sleep loop
if command -v fswatch &> /dev/null; then
    echo "✅ Using fswatch for instant detection"
    fswatch -0 "$MEMORY_FILE" | while read -d "" event; do
        echo "[$(date '+%H:%M:%S')] 🔔 File changed! Syncing..."
        python3 "$SYNC_SCRIPT"
        echo ""
    done
else
    echo "⚠️  fswatch not found. Install with: brew install fswatch"
    echo "📝 Falling back to 10-second polling..."
    
    LAST_MOD=""
    while true; do
        if [ -f "$MEMORY_FILE" ]; then
            CURRENT_MOD=$(stat -f "%m" "$MEMORY_FILE" 2>/dev/null)
            
            if [ "$CURRENT_MOD" != "$LAST_MOD" ]; then
                if [ ! -z "$LAST_MOD" ]; then
                    echo "[$(date '+%H:%M:%S')] 🔔 File changed! Syncing..."
                    python3 "$SYNC_SCRIPT"
                    echo ""
                fi
                LAST_MOD="$CURRENT_MOD"
            fi
        fi
        
        sleep 10
    done
fi
