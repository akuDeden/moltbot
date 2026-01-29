#!/bin/bash
# Auto Attendance Script for Chronicle HR
# Usage: ./auto-absen.sh [in|out]

set -e

ACTION=${1:-in}
HR_URL="https://hr.chronicle.rip"
EMAIL="faris@chronicle.rip"
PASSWORD="AbuTel09!"

# Random delay for clock in (08:30-09:00) = 30 minutes window
# Random delay for clock out (17:00-18:00) = 60 minutes window
if [ "$ACTION" = "in" ]; then
    RANDOM_DELAY=$((RANDOM % 1800)) # 0-1800 seconds (0-30 minutes)
    echo "Clock In scheduled with ${RANDOM_DELAY}s delay"
else
    RANDOM_DELAY=$((RANDOM % 3600)) # 0-3600 seconds (0-60 minutes)
    echo "Clock Out scheduled with ${RANDOM_DELAY}s delay"
fi

sleep $RANDOM_DELAY

# Execute browser automation via moltbot
if [ "$ACTION" = "in" ]; then
    MESSAGE="Go to $HR_URL. If you see a login page, enter email: $EMAIL and password: $PASSWORD then submit. After login, find and click the clock-in button, then take a screenshot to confirm success."
else
    MESSAGE="Go to $HR_URL. If you see a login page, enter email: $EMAIL and password: $PASSWORD then submit. After login, find and click the clock-out button, then take a screenshot to confirm success."
fi

echo "Executing: Browser automation for attendance"
moltbot agent --message "$MESSAGE" --thinking low

# Update attendance state
STATE_FILE="$HOME/moltbot-workspace/data/attendance-state.json"
TODAY=$(date +%Y-%m-%d)
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

mkdir -p "$(dirname "$STATE_FILE")"

if [ "$ACTION" = "in" ]; then
    cat > "$STATE_FILE" << EOF
{
  "date": "$TODAY",
  "clockIn": "$TIMESTAMP",
  "clockOut": null,
  "status": "clocked-in"
}
EOF
    echo "✅ Clock In completed at $TIMESTAMP"
else
    # Read existing state
    if [ -f "$STATE_FILE" ]; then
        CLOCK_IN=$(grep -o '"clockIn": "[^"]*' "$STATE_FILE" | cut -d'"' -f4)
        cat > "$STATE_FILE" << EOF
{
  "date": "$TODAY",
  "clockIn": "$CLOCK_IN",
  "clockOut": "$TIMESTAMP",
  "status": "clocked-out"
}
EOF
        echo "✅ Clock Out completed at $TIMESTAMP"
    else
        cat > "$STATE_FILE" << EOF
{
  "date": "$TODAY",
  "clockIn": null,
  "clockOut": "$TIMESTAMP",
  "status": "clocked-out"
}
EOF
        echo "⚠️  Clock Out completed but no Clock In record found"
    fi
fi

echo ""
echo "State saved to: $STATE_FILE"
