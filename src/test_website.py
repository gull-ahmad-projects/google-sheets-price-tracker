import requests
from bs4 import BeautifulSoup

def test_website_access():
    # Replace with a real website you want to scrape
    test_urls = [
        "https://httpbin.org/html",  # Test website that always works
        # "https://actual-supplier-website.com/products",  # Replace with your real supplier URL
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for url in test_urls:
        try:
            print(f"Testing access to: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            print(f"✓ Successfully fetched page from {url}")
            print(f"  Status code: {response.status_code}")
            print(f"  Content length: {len(response.content)} bytes")
            
            # Save a small snippet of the HTML for inspection
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('title')
            if title:
                print(f"  Page title: {title.text}")
            
            # Save HTML to file for inspection
            filename = f"debug_{url.replace('https://', '').replace('/', '_')}.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"  Page HTML saved to {filename}")
            
        except Exception as e:
            print(f"✗ Error accessing {url}: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_website_access()