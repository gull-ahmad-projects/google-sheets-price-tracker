import requests
from bs4 import BeautifulSoup
import time
import logging
from config.settings import SUPPLIER_URL, REQUEST_DELAY

def scrape_supplier_prices():
    """
    Scrape product prices from supplier website
    Returns a list of dictionaries with product information
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        logging.info(f"Fetching data from {SUPPLIER_URL}")
        response = requests.get(SUPPLIER_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Save HTML to file for inspection
        with open('debug_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        logging.info("Saved page HTML to debug_page.html for inspection")
        
        products = []
        
        # For the test website, products are in divs with class 'thumbnail'
        product_elements = soup.find_all('div', class_='thumbnail')
        
        if not product_elements:
            logging.warning("No product elements found with the current selector.")
            return []
        
        for element in product_elements:
            try:
                # Extract product details based on the test website structure
                product_name = element.find('a', class_='title').text.strip()
                price = element.find('h4', class_='price').text.strip()
                
                # Generate a simple ID from the product name
                product_id = product_name.replace(' ', '-').lower()[:20]
                
                # Clean price text (remove currency symbols, etc.)
                price = price.replace('$', '').replace(',', '')
                
                products.append({
                    'id': product_id,
                    'name': product_name,
                    'price': float(price)
                })
                
                # Be respectful to the server
                time.sleep(REQUEST_DELAY)
                
            except (AttributeError, ValueError) as e:
                logging.warning(f"Error parsing product: {e}")
                continue
                
        logging.info(f"Successfully scraped {len(products)} products")
        return products
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching supplier website: {e}")
        return []