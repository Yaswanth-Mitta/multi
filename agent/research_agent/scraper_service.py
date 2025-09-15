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
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "No title"
            
            # Extract main content
            content_selectors = [
                'article', 'main', '.content', '.post-content', 
                '.entry-content', '.article-body', 'p'
            ]
            
            content_text = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content_text = ' '.join([elem.get_text().strip() for elem in elements])
                    break
            
            # Fallback to all text
            if not content_text:
                content_text = soup.get_text()
            
            # Clean and truncate content
            content_text = ' '.join(content_text.split())[:max_length]
            
            return {
                'url': url,
                'title': title_text[:200],
                'content': content_text,
                'scraped': True
            }
            
        except Exception as e:
            return {
                'url': url,
                'title': f"Failed to scrape: {str(e)}",
                'content': "",
                'scraped': False
            }