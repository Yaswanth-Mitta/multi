import requests
import urllib.parse
import os
from typing import Dict, List, Any
from .enhanced_search_service import EnhancedSearchService
from .serp_service import SerpService

try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
except ImportError:
    TavilyClient = None
    TAVILY_AVAILABLE = False

class SearchService:
    def __init__(self, google_cse_id: str = None, serp_api_key: str = None):
        self.google_cse_id = google_cse_id
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.tavily_api_key = os.getenv('TAVILY_API_KEY')
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        self.enhanced_search = EnhancedSearchService()
        
        # Initialize SERP API service
        try:
            self.serp_service = SerpService(serp_api_key)
            self.use_serp = True
            print("✅ Search Service initialized with SERP API")
        except:
            self.serp_service = None
            self.use_serp = False
            print("⚠️ SERP API not available, using enhanced search fallback")
        
        # Initialize Tavily client if available
        if TAVILY_AVAILABLE and self.tavily_api_key:
            self.tavily_client = TavilyClient(api_key=self.tavily_api_key)
        else:
            self.tavily_client = None
    
    def search_products(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Search for product information using SERP API, Tavily, or enhanced search"""
        print(f"Searching products for: {query}")
        
        # Try SERP API first
        if self.use_serp and self.serp_service:
            try:
                search_query = f"{query} review specifications price"
                results = self.serp_service.search_google(search_query, num_results)
                if results:
                    print(f"✅ SERP API returned {len(results)} product results")
                    return results
            except Exception as e:
                print(f"SERP API failed: {e}")
        
        # Try Tavily if available
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
    
    def search_general(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """General search using SERP API or enhanced search"""
        if self.use_serp and self.serp_service:
            try:
                results = self.serp_service.search_google(query, num_results)
                if results:
                    print(f"✅ SERP API returned {len(results)} general results")
                    return results
            except Exception as e:
                print(f"SERP API failed: {e}")
        
        # Fallback to enhanced search
        return self.enhanced_search.search_multiple_sources(query, num_results)
    
    def search_news(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Search for news articles using SERP API or enhanced search"""
        if self.use_serp and self.serp_service:
            try:
                # Use SERP's dedicated news search
                results = self.serp_service.search_news(query, num_results)
                if results:
                    print(f"✅ SERP API returned {len(results)} news results")
                    # Convert to expected format
                    formatted_results = []
                    for result in results:
                        formatted_results.append({
                            'title': result.get('title', ''),
                            'snippet': result.get('snippet', ''),
                            'link': result.get('link', ''),
                            'source': result.get('source', ''),
                            'date': result.get('date', '')
                        })
                    return formatted_results
            except Exception as e:
                print(f"SERP News API failed: {e}")
        
        # Fallback to enhanced search
        search_query = f"{query} news latest"
        return self.enhanced_search.search_multiple_sources(search_query, num_results)
    
    def search_stocks(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Search for stock information using SERP API or enhanced search"""
        if self.use_serp and self.serp_service:
            try:
                search_query = f"{query} stock price market analysis financial news"
                results = self.serp_service.search_google(search_query, num_results)
                if results:
                    print(f"✅ SERP API returned {len(results)} stock results")
                    return results
            except Exception as e:
                print(f"SERP API failed: {e}")
        
        # Fallback to enhanced search
        search_query = f"{query} stock price market analysis"
        return self.enhanced_search.search_multiple_sources(search_query, num_results)
    
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