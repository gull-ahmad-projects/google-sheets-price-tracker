import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config.settings import GOOGLE_SHEET_NAME

def authenticate_google_sheets():
    """Authenticate with Google Sheets API using service account credentials"""
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('config/credentials.json', scope)
    client = gspread.authorize(creds)
    
    # Open the spreadsheet by name
    try:
        sheet = client.open(GOOGLE_SHEET_NAME).sheet1
        return sheet
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Spreadsheet named '{GOOGLE_SHEET_NAME}' not found.")
        return None