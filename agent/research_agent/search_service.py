import requests
import urllib.parse
import os
from typing import Dict, List, Any
from .enhanced_search_service import EnhancedSearchService

class SearchService:
    def __init__(self, google_cse_id: str):
        self.google_cse_id = google_cse_id
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        self.enhanced_search = EnhancedSearchService()
    
    def search_products(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Search for product information using Google Custom Search"""
        try:
            print(f"Searching products for: {query}")
            
            if not self.google_api_key:
                print("Google API key not found, using enhanced multi-source search")
                search_results = self.enhanced_search.search_multiple_sources(query, num_results)
                
                # Also get official website results
                official_results = self.enhanced_search.search_official_websites(query)
                
                # Combine results
                all_results = search_results + official_results
                return all_results[:num_results]
            
            params = {
                'key': self.google_api_key,
                'cx': self.google_cse_id,
                'q': f"{query} specifications reviews price",
                'num': min(num_results, 10)
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get('items', []):
                results.append({
                    'title': item.get('title', ''),
                    'snippet': item.get('snippet', ''),
                    'link': item.get('link', '')
                })
            
            print(f"Found {len(results)} search results")
            return results
            
        except Exception as e:
            print(f"Error in Google search: {e}, falling back to enhanced search")
            search_results = self.enhanced_search.search_multiple_sources(query, num_results)
            return search_results if search_results else self._get_fallback_results(query)
    
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