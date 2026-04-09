import gspread
from oauth2client.service_account import ServiceAccountCredentials

def setup_sheet():
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('config/credentials.json', scope)
        client = gspread.authorize(creds)
        
        # Open the sheet
        spreadsheet = client.open("Product Data")
        worksheet = spreadsheet.get_worksheet(0)
        
        # Get all values in the worksheet
        all_values = worksheet.get_all_values()
        
        # Check if the sheet is truly empty
        is_empty = len(all_values) == 0 or (len(all_values) == 1 and all(len(row) == 0 for row in all_values))
        
        if is_empty:
            headers = ["Product ID", "Product Name", "Price", "Last Updated"]
            worksheet.append_row(headers)
            print("Headers added to the sheet")
            
            # Verify headers were added
            updated_values = worksheet.get_all_values()
            print(f"Sheet now has {len(updated_values)} rows")
        else:
            print(f"Sheet already has {len(all_values)} rows with data")
            # Print first row to see what's there
            if all_values:
                print(f"First row: {all_values[0]}")
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    setup_sheet()