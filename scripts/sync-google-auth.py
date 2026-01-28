#!/usr/bin/env python3
"""
Sync Google Sheet to CSV using Service Account authentication
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv

# Configuration
SHEET_ID = "1Ibt6u5_SK4Sck9uCdLTlvkk4OYPyrjaHo92Zr33pQMc"
WORKSHEET_NAME = "Sheet1"  # Change if your worksheet has a different name
OUTPUT_FILE = "/Users/ahmadfaris/moltbot-workspace/data.csv"
CREDENTIALS_FILE = "/Users/ahmadfaris/moltbot-workspace/google-credentials.json"

def sync_sheet():
    try:
        # Setup credentials
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
        client = gspread.authorize(creds)
        
        # Open the sheet
        sheet = client.open_by_key(SHEET_ID)
        worksheet = sheet.worksheet(WORKSHEET_NAME)
        
        # Get all values
        data = worksheet.get_all_values()
        
        # Write to CSV
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        
        print(f"✅ Successfully synced {len(data)} rows to {OUTPUT_FILE}")
        return True
        
    except Exception as e:
        print(f"❌ Error syncing sheet: {str(e)}")
        return False

if __name__ == "__main__":
    sync_sheet()
