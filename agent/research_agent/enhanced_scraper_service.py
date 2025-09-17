import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import time
import random
from .serp_service import SerpService

class EnhancedScraperService:
    def __init__(self, serp_api_key: str = None):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        
        try:
            self.serp_service = SerpService(serp_api_key)
            self.use_serp = True
            print("✅ Enhanced Scraper initialized with SERP API")
        except:
            self.serp_service = None
            self.use_serp = False
            print("⚠️ SERP API not available for enhanced scraping")
    
    def scrape_serp_results(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Get URLs from SERP API and scrape their content"""
        scraped_data = []
        
        if self.use_serp and self.serp_service:
            try:
                # Get search results from SERP API
                search_results = self.serp_service.search_google(query, max_results)
                
                for result in search_results:
                    url = result.get('link', '')
                    if url:
                        scraped_content = self._scrape_single_url(url, result.get('title', ''))
                        if scraped_content:
                            scraped_data.append(scraped_content)
                        
                        # Add delay to avoid overwhelming servers
                        time.sleep(1)
                
                print(f"✅ Scraped content from {len(scraped_data)} SERP results")
                return scraped_data
                
            except Exception as e:
                print(f"SERP scraping failed: {e}")
        
        # Fallback to basic scraping
        return self._fallback_scraping(query, max_results)
    
    def find_competitors(self, product: str) -> List[Dict[str, Any]]:
        """Find competitor products using SERP API"""
        competitors = []
        
        if self.use_serp and self.serp_service:
            try:
                # Search for competitors
                competitor_query = f"{product} vs competitors alternatives"
                results = self.serp_service.search_google(competitor_query, 5)
                
                # Extract competitor mentions from results
                competitor_names = set()
                for result in results:
                    title = result.get('title', '').lower()
                    snippet = result.get('snippet', '').lower()
                    
                    # Look for competitor patterns
                    if 'vs' in title or 'vs' in snippet:
                        # Extract product names around 'vs'
                        text = f"{title} {snippet}"
                        words = text.split()
                        for i, word in enumerate(words):
                            if word == 'vs' and i > 0 and i < len(words) - 1:
                                competitor_names.add(words[i-1].title())
                                competitor_names.add(words[i+1].title())
                
                # Create competitor list
                for name in list(competitor_names)[:5]:
                    if name.lower() not in product.lower():
                        competitors.append({
                            'name': name,
                            'category': 'Direct Competitor',
                            'comparison_url': f"https://www.google.com/search?q={product}+vs+{name}"
                        })
                
                print(f"✅ Found {len(competitors)} competitors via SERP API")
                
            except Exception as e:
                print(f"Competitor search failed: {e}")
        
        # Add fallback competitors if none found
        if not competitors:
            competitors = self._generate_fallback_competitors(product)
        
        return competitors
    
    def _scrape_single_url(self, url: str, title: str = '') -> Dict[str, Any]:
        """Scrape content from a single URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extract main content
            content = ""
            
            # Try to find main content areas
            main_selectors = [
                'main', 'article', '.content', '.main-content', 
                '.post-content', '.entry-content', '#content'
            ]
            
            for selector in main_selectors:
                main_content = soup.select_one(selector)
                if main_content:
                    content = main_content.get_text(strip=True, separator=' ')
                    break
            
            # Fallback to body content
            if not content:
                content = soup.get_text(strip=True, separator=' ')
            
            # Clean and limit content
            content = ' '.join(content.split())[:2000]
            
            return {
                'url': url,
                'title': title or soup.title.string if soup.title else 'No Title',
                'content': content,
                'scraped': True,
                'word_count': len(content.split())
            }
            
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
            return {
                'url': url,
                'title': title,
                'content': f"Failed to scrape content from {url}",
                'scraped': False,
                'word_count': 0
            }
    
    def _fallback_scraping(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Fallback scraping when SERP API unavailable"""
        fallback_urls = [
            f"https://www.techradar.com/search?searchTerm={query.replace(' ', '+')}",
            f"https://www.gsmarena.com/search.php3?sQuickSearch=yes&sName={query.replace(' ', '+')}",
            f"https://www.pcmag.com/search?q={query.replace(' ', '+')}",
        ]
        
        scraped_data = []
        for url in fallback_urls[:max_results]:
            scraped_content = self._scrape_single_url(url, f"{query} - Tech Review")
            if scraped_content:
                scraped_data.append(scraped_content)
        
        return scraped_data
    
    def _generate_fallback_competitors(self, product: str) -> List[Dict[str, Any]]:
        """Generate realistic competitors when SERP search fails"""
        # Extract product type for better competitor matching
        product_lower = product.lower()
        
        if any(word in product_lower for word in ['iphone', 'apple']):
            competitors = ['Samsung Galaxy', 'Google Pixel', 'OnePlus', 'Xiaomi']
        elif any(word in product_lower for word in ['samsung', 'galaxy']):
            competitors = ['iPhone', 'Google Pixel', 'OnePlus', 'Huawei']
        elif any(word in product_lower for word in ['laptop', 'macbook']):
            competitors = ['Dell XPS', 'HP Spectre', 'Lenovo ThinkPad', 'ASUS ZenBook']
        elif any(word in product_lower for word in ['tesla', 'model']):
            competitors = ['BMW i4', 'Mercedes EQS', 'Audi e-tron', 'Lucid Air']
        else:
            competitors = ['Alternative A', 'Alternative B', 'Alternative C', 'Alternative D']
        
        return [
            {
                'name': comp,
                'category': 'Direct Competitor',
                'comparison_url': f"https://www.google.com/search?q={product}+vs+{comp}"
            }
            for comp in competitors[:4]
        ]