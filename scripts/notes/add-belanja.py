#!/usr/bin/env python3
"""
Add shopping item to Google Sheet
Usage: python3 add-belanja.py "Nama Barang" Jumlah HargaSatuan [Catatan]
"""
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Configuration
SHEET_ID = "1Ibt6u5_SK4Sck9uCdLTlvkk4OYPyrjaHo92Zr33pQMc"
WORKSHEET_NAME = "Sheet1"
CREDENTIALS_FILE = "/Users/ahmadfaris/moltbot-workspace/google-credentials.json"

def add_item(nama_barang, jumlah, harga_satuan, catatan=""):
    try:
        # Setup credentials
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
        client = gspread.authorize(creds)
        
        # Open the sheet
        sheet = client.open_by_key(SHEET_ID)
        worksheet = sheet.worksheet(WORKSHEET_NAME)
        
        # Get current date
        tanggal = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # Get next row number
        next_row = len(worksheet.get_all_values()) + 1
        
        # Calculate total
        total = int(jumlah) * int(harga_satuan)
        
        # Append row with formula for total and catatan
        row = [tanggal, nama_barang, jumlah, harga_satuan, f"=C{next_row}*D{next_row}", catatan]
        worksheet.append_row(row)
        
        # Format numbers for display
        harga_format = f"{int(harga_satuan):,}".replace(',', '.')
        total_format = f"{total:,}".replace(',', '.')
        catatan_str = f" ({catatan})" if catatan else ""
        print(f"✅ Berhasil tambah: {nama_barang} x{jumlah} @ Rp{harga_format} = Rp{total_format}{catatan_str}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python3 add-belanja.py 'Nama Barang' Jumlah HargaSatuan [Catatan]")
        print("Example: python3 add-belanja.py 'Telur' 10 2500")
        print("Example: python3 add-belanja.py 'Laundry' 1 30000 'kering dan basah'")
        sys.exit(1)
    
    nama_barang = sys.argv[1]
    jumlah = sys.argv[2]
    harga_satuan = sys.argv[3]
    catatan = sys.argv[4] if len(sys.argv) == 5 else ""
    
    add_item(nama_barang, jumlah, harga_satuan, catatan)
