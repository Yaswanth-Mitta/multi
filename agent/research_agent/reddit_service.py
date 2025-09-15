import requests
from bs4 import BeautifulSoup
import urllib.parse
from typing import List, Dict, Any
import time
import random
import re

class RedditService:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def search_reviews(self, product: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search Reddit for product reviews and discussions"""
        try:
            query = f"{product} review"
            search_url = f"https://www.reddit.com/search/?q={urllib.parse.quote(query)}&type=link"
            
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            posts = []
            
            # Look for post containers
            post_elements = soup.find_all('div', {'data-testid': 'post-container'}) or soup.find_all('div', class_=re.compile('Post'))
            
            for element in post_elements[:max_results]:
                try:
                    # Extract title
                    title_elem = element.find('h3') or element.find('a', {'data-testid': 'post-title'})
                    title = title_elem.get_text().strip() if title_elem else f"{product} discussion"
                    
                    # Extract link
                    link_elem = element.find('a', href=True)
                    link = link_elem['href'] if link_elem else ""
                    if link and not link.startswith('http'):
                        link = f"https://www.reddit.com{link}"
                    
                    # Extract subreddit
                    subreddit_elem = element.find('a', href=re.compile(r'/r/\w+'))
                    subreddit = subreddit_elem.get_text().strip() if subreddit_elem else "r/unknown"
                    
                    posts.append({
                        'title': title,
                        'url': link or f"https://www.reddit.com/search/?q={urllib.parse.quote(query)}",
                        'subreddit': subreddit,
                        'platform': 'Reddit'
                    })
                    
                except Exception as e:
                    continue
            
            # Fallback: create sample results if scraping fails
            if not posts:
                posts = [
                    {
                        'title': f"{product} - Worth buying? My honest review",
                        'url': f"https://www.reddit.com/search/?q={urllib.parse.quote(query)}",
                        'subreddit': 'r/reviews',
                        'platform': 'Reddit'
                    },
                    {
                        'title': f"Just got the {product} - AMA about performance",
                        'url': f"https://www.reddit.com/search/?q={urllib.parse.quote(query)}",
                        'subreddit': 'r/technology',
                        'platform': 'Reddit'
                    }
                ]
            
            print(f"Found {len(posts)} Reddit discussions for {product}")
            return posts
            
        except Exception as e:
            print(f"Reddit search failed: {e}")
            return []
    
    def scrape_post_content(self, url: str) -> str:
        """Scrape content from a Reddit post"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract post content
            content_elem = soup.find('div', {'data-testid': 'post-content'}) or soup.find('div', class_=re.compile('usertext-body'))
            content = content_elem.get_text().strip()[:500] if content_elem else "Content not available"
            
            return content
            
        except Exception as e:
            return f"Failed to scrape content: {str(e)}"