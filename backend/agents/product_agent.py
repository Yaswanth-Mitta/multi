from typing import Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from interfaces import Agent
from services.search_service import SearchService
from services.llm_service import LLMService
from services.enhanced_scraper_service import EnhancedScraperService
from services.youtube_service import YouTubeService
from services.enhanced_ecommerce_service import EnhancedEcommerceService
from services.langchain_service import LangChainService
import time

class ProductAgent(Agent):
    def __init__(self, search_service: SearchService, llm_service: LLMService, serp_api_key: str = None):
        self.search_service = search_service
        self.llm_service = llm_service
        self.scraper = EnhancedScraperService(serp_api_key)
        self.youtube = YouTubeService(serp_api_key)
        self.ecommerce = EnhancedEcommerceService(serp_api_key)
        self.langchain = LangChainService()
        print("✅ ProductAgent initialized with enhanced SERP-powered services")
    
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
        
        # Only get YouTube reviews for specific product review queries
        youtube_reviews = []
        if 'review' in query.lower() or 'unboxing' in query.lower() or 'vs' in query.lower():
            print("\nSearching YouTube for reviews (10 videos)...")
            youtube_reviews = self.youtube.search_reviews(query, max_results=10)
            
            # Extract content from all 10 YouTube videos
            print("\nExtracting content from 10 YouTube videos...")
            for i, video in enumerate(youtube_reviews[:10]):  # Process all 10 videos
                print(f"Processing video {i+1}/10: {video['title'][:60]}...")
                content = self.youtube.get_video_transcript(video['url'])
                video['transcript'] = content
                print(f"Content extracted {i+1}: {len(content)} characters")
                
                # Add small delay to avoid overwhelming requests
                if i < 9:  # Don't delay after last video
                    time.sleep(0.5)
        else:
            print("\nSkipping YouTube search (not a review query)")
        
        # Skip Reddit scraping (service removed)
        
        # Get e-commerce product details
        print("\nGathering e-commerce product details...")
        ecommerce_data = self.ecommerce.get_product_details(query)
        
        # Print e-commerce data
        print(f"\n=== E-COMMERCE PRODUCT DATA ===")
        for platform, data in ecommerce_data.items():
            if platform != 'summary' and data:
                print(f"\n{platform.upper()} Details:")
                print(f"Product: {data.get('product_name', 'N/A')}")
                print(f"Price: {data.get('price', 'N/A')}")
                print(f"Rating: {data.get('rating', 'N/A')} ({data.get('review_count', 'N/A')})")
                print(f"Availability: {data.get('availability', 'N/A')}")
        print(f"\n=== END E-COMMERCE DATA ===")
        
        # Scrape content from SERP API results
        print("\nScraping content from SERP API results...")
        scraped_data = self.scraper.scrape_serp_results(query, max_results=5)
        
        # Find competitors using SERP API
        print("\nFinding competitors...")
        competitors = self.scraper.find_competitors(query)
        
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
            search_results, scraped_data, youtube_reviews, ecommerce_data, competitors
        )
        
        market_analysis_prompt = f"""
        You are a professional product analyst conducting a comprehensive market analysis for "{query}".
        
        You have access to extensive research data from multiple authoritative sources:
        - Professional review websites (TechRadar, PCMag, Tom's Guide, GSMArena)
        - 10 YouTube video reviews from tech experts
        - Official product specifications and pricing
        - User feedback and discussions
        
        COMPREHENSIVE DATA:
        {search_context}
        
        REQUIRED ANALYSIS:
        1. **Product Overview**: Key specifications, features, and positioning
        2. **Performance Analysis**: Based on reviewer testing and benchmarks
        3. **User Experience**: Summarize feedback from YouTube reviews and discussions
        4. **Pros & Cons**: Balanced analysis from multiple reviewer perspectives
        5. **Competitive Positioning**: How it compares to alternatives
        6. **Value Assessment**: Price-to-performance ratio analysis
        
        ANALYSIS GUIDELINES:
        - Treat all provided data as current and factual
        - Reference specific reviewer insights and test results
        - Synthesize information from multiple sources
        - Provide concrete, data-driven conclusions
        - Focus on practical buying considerations
        """
        
        purchase_prompt = f"""
        You are a senior product consultant providing a definitive purchase recommendation for "{query}".
        
        You have analyzed comprehensive review data from:
        - 10 professional YouTube video reviews
        - Multiple expert review websites
        - User feedback and real-world testing
        - Competitive analysis and pricing data
        
        COMPLETE REVIEW DATABASE:
        {search_context}
        
        PURCHASE RECOMMENDATION FRAMEWORK:
        1. **Overall Score** (1-10): Weighted average based on all reviews
        2. **Target Buyers**: Who will benefit most from this product
        3. **Use Case Scenarios**: Best applications and environments
        4. **Potential Concerns**: Issues highlighted by reviewers
        5. **Alternative Options**: Competitive products mentioned in reviews
        6. **Final Recommendation**: Clear buy/wait/skip advice with reasoning
        
        RECOMMENDATION CRITERIA:
        - Synthesize insights from all 10+ review sources
        - Reference specific reviewer conclusions and test results
        - Consider price-performance value from multiple perspectives
        - Provide actionable buying guidance
        - Base recommendations on reviewer consensus and data
        - Assume all provided data represents current, accurate product information
        """
        
        market_analysis = self.llm_service.query_llm(market_analysis_prompt)
        purchase_analysis = self.llm_service.query_llm(purchase_prompt)
        
        # Store research data in memory if available
        if context and 'memory' in context:
            memory = context['memory']
            research_data = {
                'web_content': search_context,
                'youtube_content': str(youtube_reviews),
                'search_results': search_results
            }
            # Extract product name from query for memory storage
            product_name = query.replace('review', '').replace('analysis', '').replace('purchase', '').strip()
            research_data['youtube_videos_analyzed'] = len(youtube_reviews)
            research_data['scraped_sources'] = len(scraped_data)
            memory.start_new_session(product_name, research_data)
        
        return f"""
## 📊 COMPREHENSIVE PRODUCT ANALYSIS

**Query:** {query}  
**Category:** PRODUCT

### 📈 Market Analysis
{market_analysis}

### 🎯 Purchase Assessment
{purchase_analysis}

### 💬 Interactive Mode
✅ **Conversational mode activated** - Ask follow-up questions about:
- Product specifications and features
- Pricing and availability
- Comparisons with competitors
- User reviews and ratings

*Type 'exit' to start fresh research*

---
*Data Sources: SERP API • YouTube Reviews • E-commerce Data • AWS Bedrock AI*
        """.strip()
    
    def get_agent_type(self) -> str:
        return "PRODUCT"