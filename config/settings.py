# Google Sheet settings
GOOGLE_SHEET_NAME = "Product Data"

# Supplier website settings
# For testing, we'll use a demo e-commerce site
SUPPLIER_URL = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
REQUEST_DELAY = 2  # Seconds to wait between requests

# API rate limiting
API_BATCH_SIZE = 100  # Number of rows to update in a single API call
API_DELAY_SECONDS = 5  # Seconds to wait between batch API calls
# Logging
LOG_FILE = "logs/price_tracker.log"