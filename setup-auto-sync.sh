#!/bin/bash
# Setup auto-sync Google Sheet setiap 10 menit

CRON_JOB="*/10 * * * * ~/moltbot-workspace/sync-sheets.sh >> ~/moltbot-workspace/sync.log 2>&1"

echo "Setting up auto-sync untuk Google Sheet..."
echo "Akan sync setiap 10 menit"

# Add to crontab
(crontab -l 2>/dev/null | grep -v "sync-sheets.sh"; echo "$CRON_JOB") | crontab -

echo "✅ Auto-sync enabled!"
echo "Cek log: tail -f ~/moltbot-workspace/sync.log"
