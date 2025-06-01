import os
import glob
import time
import pandas as pd
from typing import List, Dict
from browser_use import Browser
from pathlib import Path

class ScraperError(Exception):
    pass

def extract_asin(url: str) -> str:
    """Extract ASIN from Amazon URL."""
    import re
    patterns = [
        r'/dp/([A-Z0-9]{10})',  # Standard product URL
        r'/gp/product/([A-Z0-9]{10})',  # Alternative product URL
        r'/product/([A-Z0-9]{10})',  # Another common pattern
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # If URL is just the ASIN
    if re.match(r'^[A-Z0-9]{10}$', url):
        return url
        
    raise ScraperError("Could not extract ASIN from URL")

def fetch_history(asin: str, download_dir: str = "/app/downloads") -> List[Dict[str, any]]:
    """Fetch price history for a given ASIN from camelcamelcamel.com."""
    browser = Browser()
    try:
        # Navigate to the product page
        url = f"https://camelcamelcamel.com/product/{asin}"
        browser.get(url)
        
        # Wait for the download button and click it
        download_button = browser.find_element("a.download-csv")
        if not download_button:
            raise ScraperError("Download button not found")
            
        download_button.click()
        
        # Wait for download to complete (max 10 seconds)
        max_wait = 10
        start_time = time.time()
        while time.time() - start_time < max_wait:
            csv_files = glob.glob(os.path.join(download_dir, "*.csv"))
            if csv_files:
                # Get the most recent CSV file
                latest_file = max(csv_files, key=os.path.getctime)
                
                # Read and parse the CSV
                df = pd.read_csv(latest_file)
                
                # Convert to required format
                history = []
                for _, row in df.iterrows():
                    history.append({
                        "date": row['Date'],
                        "price": float(row['Price'])
                    })
                
                # Clean up the downloaded file
                os.remove(latest_file)
                return history
                
            time.sleep(0.5)
            
        raise ScraperError("Timeout waiting for CSV download")
        
    except Exception as e:
        raise ScraperError(f"Failed to fetch price history: {str(e)}")
    finally:
        browser.quit()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve-worker", action="store_true")
    args = parser.parse_args()
    
    if args.serve_worker:
        # Worker mode - keep running and process jobs
        while True:
            time.sleep(1) 