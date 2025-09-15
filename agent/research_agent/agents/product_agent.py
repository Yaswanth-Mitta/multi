from typing import Dict, Any
from ..interfaces import Agent
from ..search_service import SearchService
from ..llm_service import LLMService
from ..scraper_service import ScraperService

class ProductAgent(Agent):
    def __init__(self, search_service: SearchService, llm_service: LLMService):
        self.search_service = search_service
        self.llm_service = llm_service
        self.scraper = ScraperService()
    
    def process(self, query: str, context: Dict[str, Any] = None) -> str:
        # Get product search data
        search_results = self.search_service.search_products(query)
        if not search_results:
            return "No product data found for the query."
        
        # Scrape actual content from URLs
        print("Scraping content from search results...")
        urls = [result['link'] for result in search_results if result.get('link')]
        scraped_data = self.scraper.scrape_content(urls)
        
        # Combine search results with scraped content
        enhanced_context = ""
        for i, result in enumerate(search_results):
            enhanced_context += f"Title: {result['title']}\nSnippet: {result['snippet']}\n"
            
            # Add scraped content if available
            if i < len(scraped_data) and scraped_data[i]['scraped']:
                enhanced_context += f"Content: {scraped_data[i]['content'][:500]}...\n"
            enhanced_context += "\n"
        
        search_context = enhanced_context
        
        market_analysis_prompt = f"""
        Based on product search data for "{query}":
        
        Search Results:
        {search_context}
        
        Provide market analysis:
        1. Product demand and trends
        2. Pricing analysis
        3. Consumer preferences
        4. Market opportunities
        """
        
        purchase_prompt = f"""
        Product: "{query}"
        
        Provide purchase assessment:
        1. Purchase likelihood (0-100%)
        2. Key buying factors
        3. Target audience
        4. Recommendations
        """
        
        market_analysis = self.llm_service.query_llm(market_analysis_prompt)
        purchase_analysis = self.llm_service.query_llm(purchase_prompt)
        
        return f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        PRODUCT MARKET ANALYSIS                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 QUERY: {query}
🏷️  CATEGORY: PRODUCT

📊 MARKET ANALYSIS:
{market_analysis}

🎯 PURCHASE ASSESSMENT:
{purchase_analysis}

═══════════════════════════════════════════════════════════════════════════════
Product Analysis | Search Data + AWS Bedrock
═══════════════════════════════════════════════════════════════════════════════
        """.strip()
    
    def get_agent_type(self) -> str:
        return "PRODUCT"