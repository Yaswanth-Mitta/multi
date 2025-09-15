import requests
from bs4 import BeautifulSoup
import urllib.parse
from typing import List, Dict, Any
import time
import random

class DuckDuckGoService:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Search using DuckDuckGo (no API key required)"""
        try:
            print(f"Searching DuckDuckGo for: {query}")
            
            # DuckDuckGo search URL
            search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            # Parse DuckDuckGo results
            for result_div in soup.find_all('div', class_='result')[:num_results]:
                title_elem = result_div.find('a', class_='result__a')
                snippet_elem = result_div.find('a', class_='result__snippet')
                
                if title_elem:
                    title = title_elem.get_text().strip()
                    link = title_elem.get('href', '')
                    
                    # Fix DuckDuckGo redirect URLs
                    if link.startswith('/l/?uddg='):
                        # Extract actual URL from DuckDuckGo redirect
                        import urllib.parse
                        parsed = urllib.parse.parse_qs(link.split('?', 1)[1])
                        if 'uddg' in parsed:
                            link = urllib.parse.unquote(parsed['uddg'][0])
                    
                    # Ensure URL has scheme
                    if link.startswith('//'):
                        link = 'https:' + link
                    elif not link.startswith('http'):
                        link = 'https://' + link
                    
                    snippet = snippet_elem.get_text().strip() if snippet_elem else ""
                    
                    results.append({
                        'title': title,
                        'snippet': snippet,
                        'link': link
                    })
            
            print(f"Found {len(results)} DuckDuckGo results")
            return results
            
        except Exception as e:
            print(f"DuckDuckGo search failed: {e}")
            return []