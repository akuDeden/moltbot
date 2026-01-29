#!/bin/bash
# Download Google Sheet sebagai CSV

SHEET_ID="1Ibt6u5_SK4Sck9uCdLTlvkk4OYPyrjaHo92Zr33pQMc"
OUTPUT_FILE="$HOME/moltbot-workspace/data.csv"

echo "🔄 Downloading Google Sheet..."
curl -L "https://docs.google.com/spreadsheets/d/${SHEET_ID}/export?format=csv" -o "$OUTPUT_FILE" 2>/dev/null

if [ -f "$OUTPUT_FILE" ]; then
    echo "✅ Sheet synced!"
    echo "📊 Data saved to: $OUTPUT_FILE"
    echo ""
    echo "Preview:"
    head -5 "$OUTPUT_FILE"
else
    echo "❌ Error: Download failed"
    exit 1
fi
