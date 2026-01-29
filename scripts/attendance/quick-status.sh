#!/bin/bash
# Quick Status Check - Returns simple status for AI to read

STATE_FILE="$HOME/moltbot-workspace/data/attendance-state.json"
TODAY=$(date +%Y-%m-%d)

if [ ! -f "$STATE_FILE" ]; then
    echo "Belum absen hari ini"
    exit 0
fi

STATE_DATE=$(grep -o '"date": "[^"]*' "$STATE_FILE" | cut -d'"' -f4)
CLOCK_IN=$(grep -o '"clockIn": "[^"]*' "$STATE_FILE" | cut -d'"' -f4)
CLOCK_OUT=$(grep -o '"clockOut": "[^"]*' "$STATE_FILE" | cut -d'"' -f4)

if [ "$STATE_DATE" != "$TODAY" ]; then
    echo "Belum absen hari ini (last record: $STATE_DATE)"
    exit 0
fi

if [ "$CLOCK_IN" != "null" ] && [ -n "$CLOCK_IN" ] && [ "$CLOCK_OUT" != "null" ] && [ -n "$CLOCK_OUT" ]; then
    IN_EPOCH=$(date -j -f "%Y-%m-%d %H:%M:%S" "$CLOCK_IN" +%s 2>/dev/null)
    OUT_EPOCH=$(date -j -f "%Y-%m-%d %H:%M:%S" "$CLOCK_OUT" +%s 2>/dev/null)
    if [ -n "$IN_EPOCH" ] && [ -n "$OUT_EPOCH" ]; then
        DURATION=$((OUT_EPOCH - IN_EPOCH))
        HOURS=$((DURATION / 3600))
        MINUTES=$(((DURATION % 3600) / 60))
        IN_TIME=$(date -j -f "%Y-%m-%d %H:%M:%S" "$CLOCK_IN" +"%H:%M" 2>/dev/null)
        OUT_TIME=$(date -j -f "%Y-%m-%d %H:%M:%S" "$CLOCK_OUT" +"%H:%M" 2>/dev/null)
        echo "Sudah clock in jam $IN_TIME dan clock out jam $OUT_TIME (kerja ${HOURS}h ${MINUTES}m)"
    else
        echo "Sudah clock in dan clock out hari ini"
    fi
elif [ "$CLOCK_IN" != "null" ] && [ -n "$CLOCK_IN" ]; then
    IN_TIME=$(date -j -f "%Y-%m-%d %H:%M:%S" "$CLOCK_IN" +"%H:%M" 2>/dev/null)
    echo "Sudah clock in jam $IN_TIME, belum clock out"
else
    echo "Belum absen hari ini"
fi
