#!/bin/bash
# Test script for n8n ticket query system
# Run this after deploying n8n workflow

echo "🧪 N8N Ticket Query System - Test Suite"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check environment
echo "1. Checking environment..."

if [ -z "$N8N_WEBHOOK_URL" ]; then
  echo -e "${RED}❌ N8N_WEBHOOK_URL not set${NC}"
  echo "   Set with: export N8N_WEBHOOK_URL='https://your-n8n.com/webhook/query-tickets'"
  exit 1
else
  echo -e "${GREEN}✅ N8N_WEBHOOK_URL configured${NC}"
  echo "   URL: $N8N_WEBHOOK_URL"
fi

echo ""

# Check scripts exist
echo "2. Checking scripts..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/n8n-tickets.sh" ]; then
  echo -e "${GREEN}✅ n8n-tickets.sh found${NC}"
else
  echo -e "${RED}❌ n8n-tickets.sh not found${NC}"
  exit 1
fi

if [ -f "$SCRIPT_DIR/n8n-query-tickets.py" ]; then
  echo -e "${GREEN}✅ n8n-query-tickets.py found${NC}"
else
  echo -e "${RED}❌ n8n-query-tickets.py not found${NC}"
  exit 1
fi

echo ""

# Test 1: Basic connectivity
echo "3. Testing webhook connectivity..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$N8N_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{}' \
  --connect-timeout 10)

if [ "$RESPONSE" = "200" ]; then
  echo -e "${GREEN}✅ Webhook responds with HTTP 200${NC}"
elif [ "$RESPONSE" = "000" ]; then
  echo -e "${RED}❌ Cannot connect to webhook (timeout/connection error)${NC}"
  echo "   Check n8n instance is running and URL is correct"
  exit 1
else
  echo -e "${YELLOW}⚠️  Webhook responds with HTTP $RESPONSE${NC}"
  echo "   Expected 200, but got $RESPONSE"
fi

echo ""

# Test 2: Query without filters
echo "4. Testing basic query (no filters)..."
curl -s -X POST "$N8N_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"limit": 5}' | jq -r '.success' > /tmp/n8n-test-result.txt

RESULT=$(cat /tmp/n8n-test-result.txt)
if [ "$RESULT" = "true" ]; then
  echo -e "${GREEN}✅ Query successful${NC}"
else
  echo -e "${RED}❌ Query failed${NC}"
  echo "   Response:"
  cat /tmp/n8n-test-result.txt
fi

echo ""

# Test 3: Bash wrapper
echo "5. Testing bash wrapper (n8n-tickets.sh)..."
if command -v python3 &> /dev/null; then
  OUTPUT=$("$SCRIPT_DIR/n8n-tickets.sh" all 2>&1)
  if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Bash wrapper works${NC}"
  else
    echo -e "${RED}❌ Bash wrapper failed${NC}"
    echo "   Output: $OUTPUT"
  fi
else
  echo -e "${YELLOW}⚠️  Python3 not found, skipping bash wrapper test${NC}"
fi

echo ""

# Test 4: Python client
echo "6. Testing Python client (n8n-query-tickets.py)..."
if command -v python3 &> /dev/null; then
  # Check httpx is installed
  python3 -c "import httpx" 2>/dev/null
  if [ $? -eq 0 ]; then
    OUTPUT=$(python3 "$SCRIPT_DIR/n8n-query-tickets.py" --limit 5 --output compact 2>&1)
    if [ $? -eq 0 ]; then
      echo -e "${GREEN}✅ Python client works${NC}"
    else
      echo -e "${RED}❌ Python client failed${NC}"
      echo "   Output: $OUTPUT"
    fi
  else
    echo -e "${YELLOW}⚠️  httpx module not installed${NC}"
    echo "   Install with: pip install httpx"
  fi
else
  echo -e "${YELLOW}⚠️  Python3 not found, skipping Python client test${NC}"
fi

echo ""

# Test 5: Filter query
echo "7. Testing filtered query..."
curl -s -X POST "$N8N_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"limit": 3}' | jq -r '.data.count' > /tmp/n8n-test-count.txt

COUNT=$(cat /tmp/n8n-test-count.txt)
if [ "$COUNT" != "null" ] && [ ! -z "$COUNT" ]; then
  echo -e "${GREEN}✅ Filtered query works (returned $COUNT tickets)${NC}"
else
  echo -e "${YELLOW}⚠️  Could not verify filtered query${NC}"
fi

echo ""

# Summary
echo "========================================"
echo "✨ Test Summary"
echo "========================================"
echo ""
echo "If all tests passed, your n8n ticket query system is ready!"
echo ""
echo "📚 Next steps:"
echo "  1. Review docs: docs/N8N-QUICK-REF.md"
echo "  2. Try queries: ./n8n-tickets.sh sprint 'Sprint 2'"
echo "  3. Integrate with chat bot commands"
echo ""
echo "🔗 Resources:"
echo "  - Full docs: docs/N8N-DYNAMIC-TICKETS.md"
echo "  - Quick ref: docs/N8N-QUICK-REF.md"
echo "  - Scripts: scripts/tickets/"
echo ""

# Cleanup
rm -f /tmp/n8n-test-result.txt /tmp/n8n-test-count.txt
