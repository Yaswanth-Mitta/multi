from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import urllib.parse
from typing import List, Dict, Any
import time

class SeleniumService:
    def __init__(self):
        self.driver = None
        self._setup_driver()
    
    def _setup_driver(self):
        """Setup Chrome driver with options"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ Selenium Chrome driver initialized")
        except Exception as e:
            print(f"❌ Failed to initialize Selenium: {e}")
            self.driver = None
    
    def search_google(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search Google using Selenium"""
        if not self.driver:
            print("Selenium not available, using fallback")
            return self._get_fallback_results(query)
        
        try:
            print(f"🔍 Searching Google with Selenium: {query}")
            
            # Navigate to Google
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            self.driver.get(search_url)
            
            # Wait for results to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.g"))
            )
            
            # Get page source and parse with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            results = []
            
            # Find search result containers
            search_results = soup.find_all('div', class_='g')[:max_results]
            
            for result in search_results:
                try:
                    # Extract title
                    title_elem = result.find('h3')
                    title = title_elem.get_text().strip() if title_elem else ""
                    
                    # Extract link
                    link_elem = result.find('a', href=True)
                    link = link_elem['href'] if link_elem else ""
                    
                    # Extract snippet
                    snippet_elem = result.find('span', {'data-ved': True}) or result.find('div', class_='VwiC3b')
                    snippet = snippet_elem.get_text().strip() if snippet_elem else ""
                    
                    if title and link:
                        results.append({
                            'title': title,
                            'snippet': snippet,
                            'link': link
                        })
                        
                except Exception as e:
                    continue
            
            print(f"✅ Found {len(results)} Google results")
            return results
            
        except Exception as e:
            print(f"❌ Google search failed: {e}")
            return self._get_fallback_results(query)
    
    def search_official_websites(self, product: str) -> List[Dict[str, Any]]:
        """Search official product websites"""
        if not self.driver:
            return []
        
        try:
            official_sites = []
            
            # Common official website patterns
            brand_sites = {
                'pixel': 'https://store.google.com/product/pixel_9',
                'iphone': 'https://www.apple.com/iphone/',
                'samsung': 'https://www.samsung.com/us/smartphones/',
                'oneplus': 'https://www.oneplus.com/',
                'xiaomi': 'https://www.mi.com/'
            }
            
            product_lower = product.lower()
            for brand, url in brand_sites.items():
                if brand in product_lower:
                    try:
                        print(f"🏢 Checking official site: {url}")
                        self.driver.get(url)
                        time.sleep(3)
                        
                        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                        title = soup.find('title')
                        title_text = title.get_text().strip() if title else f"{brand.title()} Official Site"
                        
                        # Extract key content
                        content_selectors = ['main', '.product-info', '.specs', '.features']
                        content = ""
                        for selector in content_selectors:
                            elem = soup.select_one(selector)
                            if elem:
                                content = elem.get_text()[:500]
                                break
                        
                        official_sites.append({
                            'title': title_text,
                            'snippet': f"Official {brand} website with product specifications and details",
                            'link': url,
                            'content': content,
                            'type': 'official'
                        })
                        break
                        
                    except Exception as e:
                        print(f"Failed to scrape {url}: {e}")
                        continue
            
            return official_sites
            
        except Exception as e:
            print(f"Official website search failed: {e}")
            return []
    
    def _get_fallback_results(self, query: str) -> List[Dict[str, Any]]:
        """Fallback results when Selenium fails"""
        return [
            {
                'title': f'{query} - Product Reviews and Specifications',
                'snippet': f'Comprehensive review and analysis of {query}',
                'link': f'https://www.gsmarena.com/search.php3?sQuickSearch=yes&sName={urllib.parse.quote(query)}'
            },
            {
                'title': f'{query} - Price and Availability',
                'snippet': f'Latest pricing and availability information for {query}',
                'link': f'https://www.amazon.com/s?k={urllib.parse.quote(query)}'
            }
        ]
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("🔒 Selenium driver closed")