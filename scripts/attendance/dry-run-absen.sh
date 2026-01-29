#!/bin/bash
# Dry Run Test - Show what would be executed without actually running

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Load credentials from .env
if [ -f "$WORKSPACE_ROOT/.env" ]; then
    export $(grep -v '^#' "$WORKSPACE_ROOT/.env" | grep -E '^(HR_URL|HR_EMAIL|HR_PASSWORD)=' | xargs)
fi

ACTION=${1:-in}
HR_URL="${HR_URL}"
EMAIL="${HR_EMAIL}"
PASSWORD="${HR_PASSWORD}"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 DRY RUN: Attendance Automation Test"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Action: $ACTION"
echo "Target: $HR_URL"
echo "User: $EMAIL"
echo ""

# Random delay simulation
if [ "$ACTION" = "in" ]; then
    RANDOM_DELAY=$((RANDOM % 1800))
    MINUTES=$((RANDOM_DELAY / 60))
    SECONDS=$((RANDOM_DELAY % 60))
    echo "⏰ Random delay: ${MINUTES}m ${SECONDS}s (0-30 min window)"
    MESSAGE="Go to $HR_URL. If you see a login page, enter email: $EMAIL and password: $PASSWORD then submit. After login, find and click the clock-in button, then take a screenshot to confirm success."
else
    RANDOM_DELAY=$((RANDOM % 3600))
    MINUTES=$((RANDOM_DELAY / 60))
    SECONDS=$((RANDOM_DELAY % 60))
    echo "⏰ Random delay: ${MINUTES}m ${SECONDS}s (0-60 min window)"
    MESSAGE="Go to $HR_URL. If you see a login page, enter email: $EMAIL and password: $PASSWORD then submit. After login, find and click the clock-out button, then take a screenshot to confirm success."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 Command that would be executed:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "moltbot agent --message \"$MESSAGE\" --thinking low --agent main"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Dry run completed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "To run for real, use: ./auto-absen.sh $ACTION"
