#!/bin/bash
# Setup cron jobs for automatic attendance
# This will add cron jobs for automatic clock in/out

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ABSEN_SCRIPT="$SCRIPT_DIR/auto-absen.sh"

echo "Setting up attendance cron jobs..."

# Make sure the script is executable
chmod +x "$ABSEN_SCRIPT"

# Add cron jobs
# Clock in: Every weekday at 08:30
# Clock out: Every weekday at 17:00

(crontab -l 2>/dev/null | grep -v "auto-absen.sh"; cat <<EOF
# Auto Attendance - Clock In (Mon-Fri at 08:30)
30 8 * * 1-5 $ABSEN_SCRIPT in >> /tmp/auto-absen.log 2>&1

# Auto Attendance - Clock Out (Mon-Fri at 17:00)
0 17 * * 1-5 $ABSEN_SCRIPT out >> /tmp/auto-absen.log 2>&1
EOF
) | crontab -

echo "✓ Cron jobs installed successfully!"
echo ""
echo "Scheduled:"
echo "  - Clock In:  08:30 (Mon-Fri) with random 0-30min delay"
echo "  - Clock Out: 17:00 (Mon-Fri) with random 0-60min delay"
echo ""
echo "View logs: tail -f /tmp/auto-absen.log"
echo "List jobs: crontab -l"
echo "Remove jobs: crontab -e (then delete the lines)"
