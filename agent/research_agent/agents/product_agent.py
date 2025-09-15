from typing import Dict, Any
from ..interfaces import Agent
from ..search_service import SearchService
from ..llm_service import LLMService
from ..scraper_service import ScraperService
from ..youtube_service import YouTubeService
from ..reddit_service import RedditService
from ..langchain_service import LangChainService

class ProductAgent(Agent):
    def __init__(self, search_service: SearchService, llm_service: LLMService):
        self.search_service = search_service
        self.llm_service = llm_service
        self.scraper = ScraperService()
        self.youtube = YouTubeService()
        self.reddit = RedditService()
        self.langchain = LangChainService()
    
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
        
        # Get YouTube reviews only for review queries
        youtube_reviews = []
        if 'review' in query.lower():
            print("\nSearching YouTube for reviews...")
            youtube_reviews = self.youtube.search_reviews(query)
            
            # Extract transcripts from YouTube videos
            print("\nExtracting YouTube transcripts...")
            for i, video in enumerate(youtube_reviews[:2]):  # Limit to first 2 videos
                transcript = self.youtube.get_video_transcript(video['url'])
                video['transcript'] = transcript
                print(f"Transcript {i+1}: {len(transcript)} characters")
        else:
            print("\nSkipping YouTube search (not a review query)")
        
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
        
        # Use LangChain to process and structure all data
        print("\nProcessing data with LangChain...")
        search_context = self.langchain.create_comprehensive_context(
            search_results, scraped_data, youtube_reviews, reddit_posts
        )
        
        market_analysis_prompt = f"""
        You are a product analyst reviewing "{query}" based on REAL DATA from multiple sources.
        
        IMPORTANT: The data below is from actual websites, YouTube videos, and user discussions. 
        Treat this as legitimate, current information about the product.
        
        DATA SOURCES:
        {search_context}
        
        ANALYSIS REQUIRED:
        1. Product Overview & Key Features (from scraped data)
        2. User Reviews & Feedback Summary (from YouTube transcripts and discussions)
        3. Pros and Cons Analysis (based on actual user experiences)
        4. Pricing & Value Assessment (from review sites)
        5. Comparison with Competitors (mentioned in reviews)
        6. Purchase Recommendation (based on all data)
        
        INSTRUCTIONS:
        - Use the provided data as factual information
        - Quote specific points from the scraped content
        - Reference YouTube reviewer opinions when available
        - Provide a data-driven analysis, not speculation
        """
        
        purchase_prompt = f"""
        You are providing a purchase recommendation for "{query}" based on REAL REVIEW DATA.
        
        The following data is from actual product reviews, YouTube videos, and user discussions:
        
        COMPREHENSIVE REVIEW DATA:
        {search_context}\n\nNote: This data includes actual scraped content from review websites, YouTube transcripts, and user discussions.
        
        PURCHASE ANALYSIS REQUIRED:
        1. Overall Rating (1-10) - based on reviewer consensus
        2. Best Use Cases - from actual user experiences
        3. Who Should Buy This - target audience from reviews
        4. Who Should Avoid This - common complaints/issues
        5. Best Alternatives - mentioned in comparative reviews
        6. Final Verdict - data-driven recommendation
        
        INSTRUCTIONS:
        - Base your analysis ONLY on the provided review data
        - Quote specific reviewer opinions and experiences
        - Reference price points and value assessments from reviews
        - Provide concrete recommendations based on actual user feedback
        - Do NOT question the existence of the product - analyze the provided data
        """
        
        market_analysis = self.llm_service.query_llm(market_analysis_prompt)
        purchase_analysis = self.llm_service.query_llm(purchase_prompt)
        
        # Store research data in memory if available
        if context and 'memory' in context:
            memory = context['memory']
            research_data = {
                'web_content': search_context,
                'youtube_content': str(youtube_reviews),
                'reddit_content': str(reddit_posts),
                'search_results': search_results
            }
            # Extract product name from query
            product_name = query.replace('review', '').replace('analysis', '').strip()
            memory.start_new_session(product_name, research_data)
        
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

💬 CONVERSATIONAL MODE ACTIVATED
→ Ask follow-up questions about this product (colors, price, specs, etc.)
→ Type 'exit' to start fresh research

═══════════════════════════════════════════════════════════════════════════════
Product Analysis + Conversational Mode | Search Data + AWS Bedrock
═══════════════════════════════════════════════════════════════════════════════
        """.strip()
    
    def get_agent_type(self) -> str:
        return "PRODUCT"