#!/bin/bash
# Check Attendance Status
# Shows today's attendance record

STATE_FILE="$HOME/moltbot-workspace/data/attendance-state.json"
TODAY=$(date +%Y-%m-%d)

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Attendance Status Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Date: $TODAY"
echo ""

if [ ! -f "$STATE_FILE" ]; then
    echo "❌ No attendance record found"
    echo ""
    echo "You haven't clocked in today."
    exit 0
fi

# Read state file
STATE_DATE=$(grep -o '"date": "[^"]*' "$STATE_FILE" | cut -d'"' -f4)
CLOCK_IN=$(grep -o '"clockIn": "[^"]*' "$STATE_FILE" | cut -d'"' -f4)
CLOCK_OUT=$(grep -o '"clockOut": "[^"]*' "$STATE_FILE" | cut -d'"' -f4)
STATUS=$(grep -o '"status": "[^"]*' "$STATE_FILE" | cut -d'"' -f4)

# Check if it's today's record
if [ "$STATE_DATE" != "$TODAY" ]; then
    echo "❌ No attendance record for today"
    echo ""
    echo "Last record: $STATE_DATE"
    if [ "$CLOCK_IN" != "null" ]; then
        echo "  Clock In:  $CLOCK_IN"
    fi
    if [ "$CLOCK_OUT" != "null" ]; then
        echo "  Clock Out: $CLOCK_OUT"
    fi
    echo ""
    echo "You haven't clocked in today yet."
    exit 0
fi

# Display today's status
echo "✅ Attendance Record Found"
echo ""

if [ "$CLOCK_IN" != "null" ] && [ -n "$CLOCK_IN" ]; then
    echo "🟢 Clock In:  $CLOCK_IN"
else
    echo "⚪ Clock In:  Not yet"
fi

if [ "$CLOCK_OUT" != "null" ] && [ -n "$CLOCK_OUT" ]; then
    echo "🔴 Clock Out: $CLOCK_OUT"
    
    # Calculate work duration
    if [ "$CLOCK_IN" != "null" ] && [ -n "$CLOCK_IN" ]; then
        IN_EPOCH=$(date -j -f "%Y-%m-%d %H:%M:%S" "$CLOCK_IN" +%s 2>/dev/null)
        OUT_EPOCH=$(date -j -f "%Y-%m-%d %H:%M:%S" "$CLOCK_OUT" +%s 2>/dev/null)
        
        if [ -n "$IN_EPOCH" ] && [ -n "$OUT_EPOCH" ]; then
            DURATION=$((OUT_EPOCH - IN_EPOCH))
            HOURS=$((DURATION / 3600))
            MINUTES=$(((DURATION % 3600) / 60))
            echo ""
            echo "⏱️  Duration: ${HOURS}h ${MINUTES}m"
        fi
    fi
else
    echo "⚪ Clock Out: Not yet"
fi

echo ""
echo "Status: $STATUS"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
