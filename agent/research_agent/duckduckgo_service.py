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
                    if '/l/?uddg=' in link:
                        # Extract actual URL from DuckDuckGo redirect
                        try:
                            # Parse the redirect URL
                            if '&uddg=' in link:
                                actual_url = link.split('&uddg=')[1].split('&')[0]
                            elif '?uddg=' in link:
                                actual_url = link.split('?uddg=')[1].split('&')[0]
                            else:
                                actual_url = link
                            
                            # URL decode the extracted URL
                            link = urllib.parse.unquote(actual_url)
                            print(f"Extracted URL: {link}")
                        except Exception as e:
                            print(f"Failed to extract URL from {link}: {e}")
                    
                    # Ensure URL has scheme
                    if link.startswith('//'):
                        link = 'https:' + link
                    elif not link.startswith('http') and not link.startswith('//'):
                        link = 'https://' + link
                    
                    snippet = snippet_elem.get_text().strip() if snippet_elem else ""
                    
                    results.append({
                        'title': title,
                        'snippet': snippet,
                        'link': link
                    })
            
            print(f"Found {len(results)} DuckDuckGo results")
            for i, result in enumerate(results):
                print(f"Result {i+1} URL: {result['link']}")
            return results
            
        except Exception as e:
            print(f"DuckDuckGo search failed: {e}")
            return []