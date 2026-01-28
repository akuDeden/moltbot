#!/usr/bin/env python3
"""
Auto-sync belanja dari memory file ke Google Sheet
Usage: python3 auto-sync-memory-to-sheet.py [memory_file]
"""
import sys
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Configuration
SHEET_ID = "1Ibt6u5_SK4Sck9uCdLTlvkk4OYPyrjaHo92Zr33pQMc"
WORKSHEET_NAME = "Sheet1"
CREDENTIALS_FILE = "/Users/ahmadfaris/moltbot-workspace/google-credentials.json"
MEMORY_FILE = "/Users/ahmadfaris/moltbot-workspace/memory/2026-01-28.md"

def parse_memory_file(filepath):
    """Parse belanja items from memory file"""
    items = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find Belanja section
    belanja_match = re.search(r'## Belanja\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if not belanja_match:
        return items
    
    belanja_section = belanja_match.group(1)
    
    # Parse each line: - Nama X: Rp Y atau - Nama X kg: Rp Y atau - Nama: Rp Y
    # Support multiple formats:
    # - Telur 10: Rp 2.500
    # - Pete 20 kg: Rp 20.000
    # - Sayur2an: Rp 50.000 (without quantity, assume 1)
    
    for line in belanja_section.split('\n'):
        line = line.strip()
        if not line.startswith('-'):
            continue
        
        # Remove leading dash and strip
        line = line[1:].strip()
        
        # Split by colon to separate name+qty from price
        if ':' not in line:
            continue
        
        parts = line.split(':', 1)
        left_part = parts[0].strip()  # Name and quantity part
        right_part = parts[1].strip()  # Price part (may have comments)
        
        # Extract price from right part (ignore comments in parentheses)
        price_match = re.search(r'Rp\s*([\d.,]+)', right_part)
        if not price_match:
            continue
        
        harga_str = price_match.group(1).replace('.', '').replace(',', '')
        harga = int(harga_str)
        
        # Parse left part for name and quantity
        # Try to find quantity: "Pete 20 kg" or "Telur 10" or just "Sayur2an"
        qty_match = re.search(r'^(.+?)\s+(\d+)\s*(?:kg|g|ml|l|pcs|buah|biji|ekor)?$', left_part)
        
        if qty_match:
            # Has quantity
            nama = qty_match.group(1).strip()
            jumlah = int(qty_match.group(2))
        else:
            # No quantity, assume 1
            nama = left_part
            jumlah = 1
        
        items.append({
            'nama': nama,
            'jumlah': jumlah,
            'harga': harga
        })
    
    return items

def get_existing_items(worksheet):
    """Get existing items from sheet to avoid duplicates"""
    all_values = worksheet.get_all_values()
    if len(all_values) <= 1:  # Only header
        return []
    
    existing = []
    for row in all_values[1:]:  # Skip header
        if len(row) >= 5:
            # Store as tuple: (nama, jumlah, harga)
            try:
                existing.append((row[1], int(row[2]), int(row[3])))
            except:
                pass
    
    return existing

def add_items_to_sheet(items):
    """Add items to Google Sheet"""
    try:
        # Setup credentials
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
        client = gspread.authorize(creds)
        
        # Open the sheet
        sheet = client.open_by_key(SHEET_ID)
        worksheet = sheet.worksheet(WORKSHEET_NAME)
        
        # Get existing items to avoid duplicates
        existing = get_existing_items(worksheet)
        
        added_count = 0
        skipped_count = 0
        
        for item in items:
            # Check if item already exists
            item_tuple = (item['nama'], item['jumlah'], item['harga'])
            
            if item_tuple in existing:
                print(f"⏭️  Skip (already exists): {item['nama']} x{item['jumlah']} @ Rp{item['harga']:,}")
                skipped_count += 1
                continue
            
            # Add to sheet
            tanggal = datetime.now().strftime('%Y-%m-%d %H:%M')
            next_row = len(worksheet.get_all_values()) + 1
            
            row = [
                tanggal,
                item['nama'],
                item['jumlah'],
                item['harga'],
                f"=C{next_row}*D{next_row}"  # Formula for total
            ]
            
            worksheet.append_row(row)
            
            total = item['jumlah'] * item['harga']
            print(f"✅ Added: {item['nama']} x{item['jumlah']} @ Rp{item['harga']:,} = Rp{total:,}")
            
            added_count += 1
            existing.append(item_tuple)
        
        print(f"\n📊 Summary: {added_count} added, {skipped_count} skipped")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    memory_file = sys.argv[1] if len(sys.argv) > 1 else MEMORY_FILE
    
    print(f"📖 Reading from: {memory_file}")
    
    items = parse_memory_file(memory_file)
    
    if not items:
        print("⚠️  No items found in memory file")
        sys.exit(0)
    
    print(f"📝 Found {len(items)} items")
    
    add_items_to_sheet(items)
