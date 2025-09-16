import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import time
import random

class ScraperService:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_content(self, urls: List[str], max_content_length: int = 1000) -> List[Dict[str, Any]]:
        """Scrape content from multiple URLs with enhanced fallback"""
        scraped_data = []
        
        for url in urls[:5]:  # Process up to 5 URLs
            try:
                print(f"Attempting to scrape: {url}")
                content = self._scrape_single_url(url, max_content_length)
                if content:
                    scraped_data.append(content)
                    print(f"Successfully scraped content from {url}")
                else:
                    print(f"No content extracted from {url}, skipping")
                    continue
                
                # Add delay to be respectful
                time.sleep(random.uniform(0.3, 0.8))
                
            except Exception as e:
                print(f"Scraping failed for {url}: {e}")
                continue
        
        return scraped_data
    
    def _scrape_single_url(self, url: str, max_length: int) -> Dict[str, Any]:
        """Scrape content from a single URL with better encoding handling"""
        try:
            print(f"Scraping: {url}")
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            # Handle encoding issues
            response.encoding = response.apparent_encoding or 'utf-8'
            
            # Check if content is readable
            if self._is_garbled_content(response.text):
                print(f"Detected garbled content from {url}, using fallback")
                raise Exception("Garbled content detected")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
                element.decompose()
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "No title"
            
            # Extract main content with improved selectors
            content_selectors = [
                'article', 'main', '[role="main"]',
                '.content', '.post-content', '.entry-content', 
                '.article-body', '.product-description',
                '.review-content', '.specs', '.features',
                '.product-info', '.description',
                'h1', 'h2', 'h3', 'p'
            ]
            
            content_text = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    texts = []
                    for elem in elements[:10]:  # Check more elements
                        text = elem.get_text().strip()
                        # Filter out navigation and short text
                        if len(text) > 30 and not self._is_navigation_text(text):
                            texts.append(text)
                    
                    if texts:
                        content_text = ' '.join(texts)
                        break
            
            # Fallback: extract readable paragraphs
            if not content_text or len(content_text) < 100:
                paragraphs = soup.find_all('p')
                readable_paragraphs = []
                for p in paragraphs[:20]:
                    text = p.get_text().strip()
                    if len(text) > 50 and self._is_readable_text(text):
                        readable_paragraphs.append(text)
                
                if readable_paragraphs:
                    content_text = ' '.join(readable_paragraphs)
                else:
                    # Last resort: use fallback content
                    raise Exception("No readable content found")
            
            # Clean and validate content
            content_text = self._clean_text(content_text)
            
            if len(content_text) < 50 or not self._is_readable_text(content_text):
                raise Exception("Content too short or unreadable")
            
            content_text = content_text[:max_length]
            
            print(f"Successfully scraped {len(content_text)} characters from {url}")
            
            return {
                'url': url,
                'title': title_text[:200],
                'content': content_text,
                'scraped': True
            }
            
        except Exception as e:
            print(f"Failed to scrape {url}: {str(e)}")
            return None
    

    
    def _is_garbled_content(self, text: str) -> bool:
        """Check if content appears to be garbled or encoded incorrectly"""
        if not text:
            return True
        
        # Check for high ratio of non-ASCII characters
        non_ascii_count = sum(1 for char in text if ord(char) > 127)
        if len(text) > 0 and (non_ascii_count / len(text)) > 0.3:
            return True
        
        # Check for replacement character
        return '\ufffd' in text
    
    def _is_navigation_text(self, text: str) -> bool:
        """Check if text appears to be navigation or UI elements"""
        nav_keywords = ['menu', 'navigation', 'skip to', 'search', 'login', 'sign in', 
                       'cart', 'checkout', 'home', 'about us', 'contact', 'privacy',
                       'subscribe', 'newsletter', 'follow us', 'social media']
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in nav_keywords) and len(text) < 100
    
    def _is_readable_text(self, text: str) -> bool:
        """Check if text is readable and meaningful"""
        if not text or len(text) < 20:
            return False
        
        # Check for reasonable ratio of letters to total characters
        letter_count = sum(1 for char in text if char.isalpha())
        if len(text) > 0 and (letter_count / len(text)) < 0.5:
            return False
        
        # Check for meaningful words
        words = text.split()
        if len(words) < 5:
            return False
        
        return True
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        import re
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove control characters
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
        
        # Remove repeated punctuation
        text = re.sub(r'[.]{3,}', '...', text)
        text = re.sub(r'[-]{3,}', '---', text)
        
        # Remove HTML entities
        text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        text = text.replace('&quot;', '"').replace('&#39;', "'")
        
        return text.strip()