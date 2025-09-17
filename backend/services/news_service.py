import requests
from typing import Dict, List, Any

class NewsService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsdata.io/api/1/news"
    
    def search_news(self, query: str, language: str = "en", size: int = 5) -> List[Dict[str, Any]]:
        """Search for news articles using NewsData.io API"""
        try:
            params = {
                'apikey': self.api_key,
                'q': query,
                'language': language,
                'size': size
            }
            
            print(f"Searching news for: {query}")
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for article in data.get('results', []):
                results.append({
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'content': article.get('content', ''),
                    'link': article.get('link', ''),
                    'pubDate': article.get('pubDate', ''),
                    'source_id': article.get('source_id', '')
                })
            
            print(f"Found {len(results)} news articles")
            return results
            
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []