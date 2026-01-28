#!/bin/bash
# Wrapper script untuk query sprint tickets dari Notion
# Usage: ./query-sprint-tickets.sh [sprint_number]

SPRINT_NUM="${1:-2}"

echo "🔍 Querying Sprint ${SPRINT_NUM} tickets from Notion..."
echo ""

python3 /Users/ahmadfaris/moltbot-workspace/scripts/get-tickets-sprint.py "${SPRINT_NUM}"
