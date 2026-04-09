import datetime
import logging
import time

def update_sheet_with_prices(sheet, products):
    """
    Update Google Sheet with the latest prices using batch updates
    """
    if not sheet:
        logging.error("Sheet is not available")
        return False
        
    try:
        # Clear existing data (except headers)
        sheet.clear()
        
        # Add headers
        headers = ["Product ID", "Product Name", "Price", "Last Updated"]
        sheet.append_row(headers)
        
        # Prepare all rows at once
        all_rows = []
        for product in products:
            row = [
                product['id'],
                product['name'],
                product['price'],
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ]
            all_rows.append(row)
        
        # Use batch update to add all rows at once
        # Split into batches of 100 to avoid size limits
        batch_size = 100
        for i in range(0, len(all_rows), batch_size):
            batch = all_rows[i:i+batch_size]
            sheet.append_rows(batch)
            
            # Add a small delay between batches
            if i + batch_size < len(all_rows):
                time.sleep(5)  # Wait 5 seconds between batches
            
        logging.info(f"Successfully updated sheet with {len(products)} products")
        return True
        
    except Exception as e:
        logging.error(f"Error updating sheet: {e}")
        return False

def check_for_price_changes(sheet, products):
    """
    Compare new prices with existing ones and log changes
    """
    if not sheet:
        logging.error("Sheet is not available")
        return
        
    try:
        # Get existing data
        existing_data = sheet.get_all_records()
        existing_prices = {row['Product ID']: float(row['Price']) for row in existing_data}
        
        # Check for changes
        changes = []
        for product in products:
            product_id = product['id']
            new_price = product['price']
            
            if product_id in existing_prices and existing_prices[product_id] != new_price:
                old_price = existing_prices[product_id]
                change_percent = ((new_price - old_price) / old_price) * 100
                
                changes.append({
                    'id': product_id,
                    'name': product['name'],
                    'old_price': old_price,
                    'new_price': new_price,
                    'change_percent': change_percent
                })
        
        if changes:
            logging.info("Price changes detected:")
            for change in changes:
                direction = "increased" if change['change_percent'] > 0 else "decreased"
                # Fix: Replace Unicode arrow with ASCII text
                logging.info(f"{change['name']} ({change['id']}): ${change['old_price']:.2f} to ${change['new_price']:.2f} ({abs(change['change_percent']):.2f}% {direction})")
        
        return changes
        
    except Exception as e:
        logging.error(f"Error checking for price changes: {e}")
        return []