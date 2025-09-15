import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import time
import random

class ScraperService:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_content(self, urls: List[str], max_content_length: int = 1000) -> List[Dict[str, Any]]:
        """Scrape content from multiple URLs"""
        scraped_data = []
        
        for url in urls[:3]:  # Limit to 3 URLs to avoid rate limiting
            try:
                content = self._scrape_single_url(url, max_content_length)
                if content:
                    scraped_data.append(content)
                
                # Add delay to be respectful
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                print(f"Failed to scrape {url}: {e}")
                continue
        
        return scraped_data
    
    def _scrape_single_url(self, url: str, max_length: int) -> Dict[str, Any]:
        """Scrape content from a single URL"""
        try:
            print(f"Scraping: {url}")
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
                script.decompose()
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "No title"
            
            # Extract main content with priority order
            content_selectors = [
                'article', 'main', '[role="main"]',
                '.content', '.post-content', '.entry-content', 
                '.article-body', '.product-description',
                '.review-content', '.specs', '.features',
                'p', 'div'
            ]
            
            content_text = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    texts = []
                    for elem in elements[:5]:  # Limit to first 5 elements
                        text = elem.get_text().strip()
                        if len(text) > 50:  # Only include substantial text
                            texts.append(text)
                    
                    if texts:
                        content_text = ' '.join(texts)
                        break
            
            # Fallback to all text if nothing found
            if not content_text or len(content_text) < 100:
                all_text = soup.get_text()
                content_text = all_text if all_text else "No content found"
            
            # Clean and truncate content
            content_text = ' '.join(content_text.split())[:max_length]
            
            print(f"Successfully scraped {len(content_text)} characters from {url}")
            
            return {
                'url': url,
                'title': title_text[:200],
                'content': content_text,
                'scraped': True
            }
            
        except Exception as e:
            print(f"Failed to scrape {url}: {str(e)}")
            return {
                'url': url,
                'title': f"Scraping failed: {str(e)[:100]}",
                'content': f"Unable to scrape content from {url}. Error: {str(e)}",
                'scraped': False
            }