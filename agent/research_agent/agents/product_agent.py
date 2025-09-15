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
        
        # Print search results
        print(f"\n=== SEARCH DATA RETRIEVED ===")
        for i, result in enumerate(search_results, 1):
            print(f"\nResult {i}:")
            print(f"Title: {result['title']}")
            print(f"Snippet: {result['snippet']}")
            print(f"Link: {result['link']}")
        print(f"\n=== END SEARCH DATA ===")
        
        # Get YouTube reviews
        print("\nSearching YouTube for reviews...")
        youtube_reviews = self.youtube.search_reviews(query)
        
        # Get Reddit discussions
        print("\nSearching Reddit for discussions...")
        reddit_posts = self.reddit.search_reviews(query)
        
        # Scrape actual content from URLs
        print("\nScraping content from search results...")
        urls = [result['link'] for result in search_results if result.get('link')]
        scraped_data = self.scraper.scrape_content(urls)
        
        # Print scraped data
        print(f"\n=== SCRAPED CONTENT ===")
        for i, data in enumerate(scraped_data):
            print(f"\nScraped from URL {i+1}: {data['url']}")
            print(f"Title: {data['title']}")
            print(f"Content Preview: {data['content'][:200]}...")
            print(f"Scraping Success: {data['scraped']}")
        print(f"\n=== END SCRAPED CONTENT ===")
        
        # Combine all sources
        enhanced_context = "\n=== SEARCH RESULTS & SCRAPED CONTENT ===\n"
        for i, result in enumerate(search_results):
            enhanced_context += f"Source {i+1}:\n"
            enhanced_context += f"Title: {result['title']}\n"
            enhanced_context += f"Snippet: {result['snippet']}\n"
            enhanced_context += f"URL: {result['link']}\n"
            
            # Add scraped content if available
            if i < len(scraped_data) and scraped_data[i]['scraped']:
                enhanced_context += f"Scraped Content: {scraped_data[i]['content'][:500]}\n"
            else:
                enhanced_context += "Scraped Content: Not available\n"
            enhanced_context += "\n"
        
        enhanced_context += "\n=== YOUTUBE REVIEWS ===\n"
        for i, video in enumerate(youtube_reviews, 1):
            enhanced_context += f"{i}. 📺 {video['title']}\n"
            enhanced_context += f"   Views: {video['views']}\n"
            enhanced_context += f"   URL: {video['url']}\n\n"
        
        enhanced_context += "\n=== REDDIT DISCUSSIONS ===\n"
        for i, post in enumerate(reddit_posts, 1):
            enhanced_context += f"{i}. 💬 {post['title']}\n"
            enhanced_context += f"   Subreddit: {post['subreddit']}\n"
            enhanced_context += f"   URL: {post['url']}\n\n"
        
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