import schedule
import time
import logging
from datetime import datetime
import sys
import os

# Add project root to Python path to fix import issues
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.auth import authenticate_google_sheets
from src.scraper import scrape_supplier_prices
from src.sheets_updater import update_sheet_with_prices, check_for_price_changes
from config.settings import LOG_FILE

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def job():
    """Main job to scrape prices and update Google Sheet"""
    logging.info("Starting price update job")
    
    # Authenticate with Google Sheets
    sheet = authenticate_google_sheets()
    if not sheet:
        logging.error("Failed to authenticate with Google Sheets")
        return
    
    # Scrape prices from supplier website
    products = scrape_supplier_prices()
    if not products:
        logging.warning("No products found or error in scraping")
        return
    
    # Check for price changes
    check_for_price_changes(sheet, products)
    
    # Update the sheet with new prices using batch updates
    success = update_sheet_with_prices(sheet, products)
    
    if success:
        logging.info("Price update job completed successfully")
    else:
        logging.error("Price update job failed")

def main():
    """Main function to schedule and run the job"""
    logging.info("Starting Supplier Price Tracker")
    
    # Schedule the job to run daily at a specific time (e.g., 9:00 AM)
    schedule.every().day.at("09:00").do(job)
    
    # Run the job immediately on startup
    job()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute if the scheduled job is due

if __name__ == "__main__":
    main()