#!/bin/bash
# Simple scheduler - runs every minute via cron

SCRIPT_DIR="/Users/ahmadfaris/moltbot-workspace"
SYNC_SCRIPT="$SCRIPT_DIR/scripts/auto-sync-memory-to-sheet.py"
LOG_FILE="$SCRIPT_DIR/cron-sync.log"

# Set Python path
export PATH="/Users/ahmadfaris/.pyenv/shims:$PATH"

# Run sync
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Syncing..." >> "$LOG_FILE"
python3 "$SYNC_SCRIPT" >> "$LOG_FILE" 2>&1
echo "" >> "$LOG_FILE"
