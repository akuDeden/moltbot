#!/bin/bash

echo "🧪 Testing n8n Webhook..."
echo ""

# Test 1: Natural Language Query
echo "Test 1: Natural Language (AI)"
echo "Command: curl -X POST https://n8n.chronicle.rip/webhook-test/query-tickets -d '{\"query\": \"cari ticket sprint 1 yang in progress\"}'"
echo ""
curl -X POST https://n8n.chronicle.rip/webhook-test/query-tickets \
  -H "Content-Type: application/json" \
  -d '{"query": "cari ticket sprint 1 yang in progress"}' \
  -s | jq '.' 2>/dev/null || echo "Response (raw):"

echo ""
echo "---"
echo ""

# Test 2: Structured Parameters
echo "Test 2: Structured (Direct, no AI)"
echo "Command: curl -X POST https://n8n.chronicle.rip/webhook-test/query-tickets -d '{\"sprint\": \"Sprint 1\", \"status\": \"In progress\"}'"
echo ""
curl -X POST https://n8n.chronicle.rip/webhook-test/query-tickets \
  -H "Content-Type: application/json" \
  -d '{"sprint": "Sprint 1", "status": "In progress"}' \
  -s | jq '.' 2>/dev/null || echo "Response (raw):"

echo ""
echo "---"
echo ""

# Test 3: Simple keyword search
echo "Test 3: Keyword Search"
echo "Command: curl -X POST https://n8n.chronicle.rip/webhook-test/query-tickets -d '{\"keywords\": \"bug\"}'"
echo ""
curl -X POST https://n8n.chronicle.rip/webhook-test/query-tickets \
  -H "Content-Type: application/json" \
  -d '{"keywords": "bug"}' \
  -s | jq '.' 2>/dev/null || echo "Response (raw):"

echo ""
echo "✅ Test completed!"
