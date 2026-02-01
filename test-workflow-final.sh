#!/bin/bash
set -e

echo "🧪 Testing N8N Workflow - Notion Tickets dengan AI Parser"
echo "=========================================================="
echo ""

# Test URL (sesuaikan dengan mode test/production)
WEBHOOK_URL="https://n8n.chronicle.rip/webhook-test/query-tickets"
# WEBHOOK_URL="https://n8n.chronicle.rip/webhook/query-tickets"  # Uncomment untuk production

echo "📍 Webhook URL: $WEBHOOK_URL"
echo ""

# Test 1: Natural Language Query dengan Mistral AI
echo "Test 1: Natural Language Query (AI Parser)"
echo "Query: 'carikan tiket sprint 2 dengan status code review'"
echo "---"
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"query": "carikan tiket sprint 2 dengan status code review"}' \
  -s -w "\nHTTP Status: %{http_code}\nTime: %{time_total}s\n" | jq '.' 2>/dev/null || cat

echo ""
echo "=================================================="
echo ""

# Test 2: Structured Query (No AI)
echo "Test 2: Structured Query (Direct Parsing)"
echo "Params: Sprint 2, Code review"
echo "---"
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"sprint": "Sprint 2", "status": "Code review"}' \
  -s -w "\nHTTP Status: %{http_code}\nTime: %{time_total}s\n" | jq '.' 2>/dev/null || cat

echo ""
echo "=================================================="
echo ""

# Test 3: Keyword Search
echo "Test 3: Keyword Search"
echo "Keywords: 'review'"
echo "---"
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"keywords": "review"}' \
  -s -w "\nHTTP Status: %{http_code}\nTime: %{time_total}s\n" | jq '.' 2>/dev/null || cat

echo ""
echo "✅ Test completed!"
