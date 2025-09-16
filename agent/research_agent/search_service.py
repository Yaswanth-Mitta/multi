import requests
import urllib.parse
import os
from typing import Dict, List, Any
from .enhanced_search_service import EnhancedSearchService

try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
except ImportError:
    TavilyClient = None
    TAVILY_AVAILABLE = False

class SearchService:
    def __init__(self, google_cse_id: str):
        self.google_cse_id = google_cse_id
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.tavily_api_key = os.getenv('TAVILY_API_KEY')
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        self.enhanced_search = EnhancedSearchService()
        
        # Initialize Tavily client if available
        if TAVILY_AVAILABLE and self.tavily_api_key:
            self.tavily_client = TavilyClient(api_key=self.tavily_api_key)
        else:
            self.tavily_client = None
    
    def search_products(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Search for product information using Tavily or enhanced search"""
        print(f"Searching products for: {query}")
        
        # Try Tavily first if available
        if self.tavily_client:
            print("Using Tavily AI search")
            try:
                response = self.tavily_client.search(
                    query=f"{query} review specifications price",
                    search_depth="advanced",
                    max_results=num_results,
                    include_domains=["techradar.com", "pcmag.com", "gsmarena.com", "flipkart.com", "amazon.in"]
                )
                
                results = []
                for result in response.get('results', []):
                    results.append({
                        'title': result.get('title', ''),
                        'snippet': result.get('content', '')[:200] + '...',
                        'link': result.get('url', ''),
                        'source': 'Tavily'
                    })
                
                if results:
                    return results
                    
            except Exception as e:
                print(f"Tavily search failed: {e}")
        
        print("Using enhanced multi-source search (fallback)")
        # Fallback to enhanced search
        search_results = self.enhanced_search.search_multiple_sources(query, num_results)
        official_results = self.enhanced_search.search_official_websites(query)
        all_results = search_results + official_results
        return all_results[:num_results]
    
    def _get_fallback_results(self, query: str) -> List[Dict[str, Any]]:
        """Fallback search results when all methods fail"""
        return [
            {
                'title': f'{query} - Product Reviews and Specifications',
                'snippet': f'Detailed product analysis of {query} including specifications, user reviews, pricing, and availability.',
                'link': f'https://www.gsmarena.com/search.php3?sQuickSearch=yes&sName={urllib.parse.quote(query)}'
            },
            {
                'title': f'{query} - Price Comparison and Reviews',
                'snippet': f'Compare prices for {query} from multiple vendors and read user reviews.',
                'link': f'https://www.amazon.com/s?k={urllib.parse.quote(query)}'
            },
            {
                'title': f'{query} - Technical Specifications',
                'snippet': f'Technical specifications and detailed features of {query}.',
                'link': f'https://www.techradar.com/search?searchTerm={urllib.parse.quote(query)}'
            },
            {
                'title': f'{query} - Expert Reviews',
                'snippet': f'Professional reviews and analysis of {query} from tech experts.',
                'link': f'https://www.pcmag.com/search?q={urllib.parse.quote(query)}'
            }
        ]
    
    def close(self):
        """Close search service"""
        pass  # No browser to close