#!/bin/bash
# Auto-sync memory to Google Sheet every 2 minutes
# Run in background: ./watch-and-sync.sh

SCRIPT_DIR="/Users/ahmadfaris/moltbot-workspace"
SCRIPTS_DIR="$SCRIPT_DIR/scripts"
MEMORY_FILE="$SCRIPT_DIR/memory/2026-01-28.md"
LOG_FILE="$SCRIPT_DIR/sync.log"

# Use pyenv Python
export PATH="/Users/ahmadfaris/.pyenv/shims:$PATH"
PYTHON_CMD="python3"

echo "🔄 Starting auto-sync watcher..." | tee -a "$LOG_FILE"
echo "📁 Watching: $MEMORY_FILE" | tee -a "$LOG_FILE"
echo "🐍 Python: $($PYTHON_CMD --version)" | tee -a "$LOG_FILE"
echo "Press Ctrl+C to stop" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

while true; do
    # Get current date for memory file
    TODAY=$(date +%Y-%m-%d)
    CURRENT_MEMORY="$SCRIPT_DIR/memory/$TODAY.md"
    
    if [ -f "$CURRENT_MEMORY" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Syncing..." | tee -a "$LOG_FILE"
        
        # Run sync script
        $PYTHON_CMD "$SCRIPTS_DIR/auto-sync-memory-to-sheet.py" "$CURRENT_MEMORY" 2>&1 | tee -a "$LOG_FILE"
        
        echo "" | tee -a "$LOG_FILE"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Memory file not found: $CURRENT_MEMORY" | tee -a "$LOG_FILE"
    fi
    
    # Wait 2 minutes
    sleep 120
done
