import gspread
from oauth2client.service_account import ServiceAccountCredentials

def test_connection():
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('config/credentials.json', scope)
        client = gspread.authorize(creds)
        
        # List all spreadsheets
        spreadsheets = client.openall()
        print("Available spreadsheets:")
        for sheet in spreadsheets:
            print(f"- {sheet.title}")
        
        # Try to open the specific sheet
        spreadsheet = client.open("Product Data")
        
        # Get the first worksheet
        worksheet = spreadsheet.get_worksheet(0)  # 0 is the index of the first worksheet
        
        # Now use get_all_records on the worksheet, not the spreadsheet
        records = worksheet.get_all_records()
        print(f"\nSuccessfully opened '{spreadsheet.title}' with {len(records)} rows")
        
        # Print first few records to verify
        if records:
            print("First record:", records[0])
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_connection()