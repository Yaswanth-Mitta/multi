from typing import Dict, Any
from ..interfaces import Agent
from ..search_service import SearchService
from ..llm_service import LLMService
from ..scraper_service import ScraperService
from ..youtube_service import YouTubeService
from ..reddit_service import RedditService

class ProductAgent(Agent):
    def __init__(self, search_service: SearchService, llm_service: LLMService):
        self.search_service = search_service
        self.llm_service = llm_service
        self.scraper = ScraperService()
        self.youtube = YouTubeService()
        self.reddit = RedditService()
    
    def process(self, query: str, context: Dict[str, Any] = None) -> str:
        # Get product search data
        search_results = self.search_service.search_products(query)
        if not search_results:
            return "No product data found for the query."
        
        # Get YouTube reviews
        print("Searching YouTube for reviews...")
        youtube_reviews = self.youtube.search_reviews(query)
        
        # Get Reddit discussions
        print("Searching Reddit for discussions...")
        reddit_posts = self.reddit.search_reviews(query)
        
        # Scrape actual content from URLs
        print("Scraping content from search results...")
        urls = [result['link'] for result in search_results if result.get('link')]
        scraped_data = self.scraper.scrape_content(urls)
        
        # Combine all sources
        enhanced_context = "\n=== SEARCH RESULTS ===\n"
        for i, result in enumerate(search_results):
            enhanced_context += f"Title: {result['title']}\nSnippet: {result['snippet']}\n"
            if i < len(scraped_data) and scraped_data[i]['scraped']:
                enhanced_context += f"Content: {scraped_data[i]['content'][:300]}...\n"
            enhanced_context += "\n"
        
        enhanced_context += "\n=== YOUTUBE REVIEWS ===\n"
        for video in youtube_reviews:
            enhanced_context += f"📺 {video['title']}\n   Views: {video['views']}\n   URL: {video['url']}\n\n"
        
        enhanced_context += "\n=== REDDIT DISCUSSIONS ===\n"
        for post in reddit_posts:
            enhanced_context += f"💬 {post['title']}\n   Subreddit: {post['subreddit']}\n   URL: {post['url']}\n\n"
        
        search_context = enhanced_context
        
        market_analysis_prompt = f"""
        Based on comprehensive product data for "{query}":
        
        {search_context}
        
        Provide detailed product analysis:
        1. Product Overview & Key Features
        2. User Reviews & Feedback Summary
        3. Pros and Cons Analysis
        4. Pricing & Value Assessment
        5. Comparison with Competitors
        6. Purchase Recommendation
        
        Use the YouTube reviews and Reddit discussions to provide authentic user perspectives.
        """
        
        purchase_prompt = f"""
        Based on the comprehensive data including YouTube reviews and Reddit discussions for "{query}":
        
        Provide purchase decision analysis:
        1. Overall Rating (1-10)
        2. Best Use Cases
        3. Who Should Buy This
        4. Who Should Avoid This
        5. Best Alternatives
        6. Final Verdict
        
        Consider real user experiences from YouTube and Reddit in your analysis.
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