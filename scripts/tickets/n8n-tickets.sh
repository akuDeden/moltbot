#!/bin/bash
# Quick wrapper for n8n ticket queries from chat commands
# Usage: ./n8n-tickets.sh sprint "Sprint 2"
#        ./n8n-tickets.sh status "In Progress"
#        ./n8n-tickets.sh search "sales"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/n8n-query-tickets.py"

case "$1" in
  sprint)
    python3 "$PYTHON_SCRIPT" --sprint "$2" --output compact
    ;;
  
  status)
    python3 "$PYTHON_SCRIPT" --status "$2" --output compact
    ;;
  
  search|find)
    python3 "$PYTHON_SCRIPT" --keywords "$2" --output compact
    ;;
  
  assignee|assigned)
    python3 "$PYTHON_SCRIPT" --assignee "$2" --output compact
    ;;
  
  all)
    python3 "$PYTHON_SCRIPT" --all --output compact
    ;;
  
  *)
    echo "Usage: $0 {sprint|status|search|assignee|all} [value]"
    echo ""
    echo "Examples:"
    echo "  $0 sprint 'Sprint 2'"
    echo "  $0 status 'In Progress'"
    echo "  $0 search 'sales'"
    echo "  $0 assignee 'Ahmad'"
    echo "  $0 all"
    exit 1
    ;;
esac
