import os
import requests
from typing import List, Dict, Any
from serpapi import GoogleSearch

class SerpService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('SERP_API_KEY')
        if not self.api_key:
            raise ValueError("SERP API key is required")
    
    def search_google(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """Search Google using SERP API"""
        try:
            params = {
                "engine": "google",
                "q": query,
                "api_key": self.api_key,
                "num": num_results,
                "hl": "en",
                "gl": "us"
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            formatted_results = []
            for result in results.get("organic_results", []):
                formatted_results.append({
                    'title': result.get('title', ''),
                    'snippet': result.get('snippet', ''),
                    'link': result.get('link', ''),
                    'source': result.get('source', ''),
                    'position': result.get('position', 0)
                })
            
            print(f"SERP API found {len(formatted_results)} results for: {query}")
            return formatted_results
            
        except Exception as e:
            print(f"SERP API search failed: {e}")
            return []
    
    def search_youtube(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search YouTube using SERP API"""
        try:
            params = {
                "engine": "youtube",
                "search_query": query,
                "api_key": self.api_key,
                "hl": "en",
                "gl": "us"
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            videos = []
            for video in results.get("video_results", [])[:max_results]:
                video_id = self._extract_video_id(video.get('link', ''))
                videos.append({
                    'title': video.get('title', ''),
                    'url': video.get('link', ''),
                    'video_id': video_id,
                    'channel': video.get('channel', {}).get('name', ''),
                    'views': video.get('views', ''),
                    'duration': video.get('length', ''),
                    'published': video.get('published_date', ''),
                    'thumbnail': video.get('thumbnail', ''),
                    'platform': 'YouTube'
                })
            
            print(f"SERP API found {len(videos)} YouTube videos for: {query}")
            return videos
            
        except Exception as e:
            print(f"SERP YouTube search failed: {e}")
            return []
    
    def search_shopping(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search Google Shopping using SERP API"""
        try:
            params = {
                "engine": "google_shopping",
                "q": query,
                "api_key": self.api_key,
                "hl": "en",
                "gl": "us"
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            products = []
            for product in results.get("shopping_results", [])[:max_results]:
                products.append({
                    'title': product.get('title', ''),
                    'price': product.get('price', ''),
                    'source': product.get('source', ''),
                    'link': product.get('link', ''),
                    'rating': product.get('rating', ''),
                    'reviews': product.get('reviews', ''),
                    'thumbnail': product.get('thumbnail', ''),
                    'delivery': product.get('delivery', '')
                })
            
            print(f"SERP API found {len(products)} shopping results for: {query}")
            return products
            
        except Exception as e:
            print(f"SERP Shopping search failed: {e}")
            return []
    
    def search_news(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search Google News using SERP API"""
        try:
            params = {
                "engine": "google_news",
                "q": query,
                "api_key": self.api_key,
                "hl": "en",
                "gl": "us"
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            news_articles = []
            for article in results.get("news_results", [])[:max_results]:
                news_articles.append({
                    'title': article.get('title', ''),
                    'snippet': article.get('snippet', ''),
                    'link': article.get('link', ''),
                    'source': article.get('source', ''),
                    'date': article.get('date', ''),
                    'thumbnail': article.get('thumbnail', '')
                })
            
            print(f"SERP API found {len(news_articles)} news results for: {query}")
            return news_articles
            
        except Exception as e:
            print(f"SERP News search failed: {e}")
            return []
    
    def _extract_video_id(self, url: str) -> str:
        """Extract YouTube video ID from URL"""
        if not url:
            return ""
        
        # Handle different YouTube URL formats
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/v/([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            import re
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return ""