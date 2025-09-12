from typing import Dict, List, Any
from .news_service import NewsService
from .search_service import SearchService
from .llm_service import LLMService

class AIOrchestrator:
    def __init__(self, newsdata_api_key: str, google_cse_id: str, aws_access_key: str = None, aws_secret_key: str = None, aws_region: str = 'us-east-1'):
        self.news_service = NewsService(newsdata_api_key)
        self.search_service = SearchService(google_cse_id)
        self.llm_service = LLMService(aws_access_key, aws_secret_key, aws_region)
    
    def classify_query(self, query: str) -> str:
        """Classify query type using LLM"""
        classification_prompt = f"""
        Classify this query into one of these categories:
        1. STOCKS - stock prices, market data, financial news, company earnings, trading
        2. NEWS - current events, breaking news, politics, world events
        3. PRODUCT - product reviews, shopping, specifications, price comparison
        4. GENERAL - other queries
        
        Query: "{query}"
        
        Respond with only: STOCKS, NEWS, PRODUCT, or GENERAL
        """
        
        classification = self.llm_service.query_llm(classification_prompt).strip().upper()
        print(f"\n=== CLASSIFICATION ===")
        print(f"Query: {query}")
        print(f"Classified as: {classification}")
        print(f"=== END CLASSIFICATION ===")
        return classification
    
    def create_optimized_prompt(self, query: str, category: str) -> str:
        """Create optimized search prompt based on category"""
        if category == "STOCKS":
            return f"stock market {query} financial news earnings"
        elif category == "NEWS":
            return f"breaking news {query} latest updates"
        elif category == "PRODUCT":
            return f"product {query} reviews specifications price"
        else:
            return query
    
    def analyze_query(self, user_query: str) -> str:
        """Main orchestration method"""
        print(f"Processing query: {user_query}")
        
        # Step 1: Classify the query
        category = self.classify_query(user_query)
        
        # Step 2: Route to appropriate service
        if category in ["STOCKS", "NEWS"]:
            return self._handle_news_query(user_query, category)
        elif category == "PRODUCT":
            return self._handle_product_query(user_query)
        else:
            return self._handle_general_query(user_query)
    
    def _handle_news_query(self, query: str, category: str) -> str:
        """Handle stocks/news queries with real-time data"""
        optimized_query = self.create_optimized_prompt(query, category)
        news_results = self.news_service.search_news(optimized_query)
        
        if not news_results:
            return "No real-time data found for the query."
        
        news_context = "\n".join([
            f"Title: {article['title']}\nDescription: {article['description']}\nSource: {article['source_id']}\nDate: {article['pubDate']}\n"
            for article in news_results[:3]
        ])
        
        print(f"\n=== NEWS DATA RETRIEVED ===")
        for i, article in enumerate(news_results[:3], 1):
            print(f"\nArticle {i}:")
            print(f"Title: {article['title']}")
            print(f"Description: {article['description'][:200]}...")
            print(f"Source: {article['source_id']}")
            print(f"Date: {article['pubDate']}")
        print(f"\n=== END NEWS DATA ===")
        
        analysis_prompt = f"""
        Based on real-time news data about "{query}", provide analysis:
        
        News Data:
        {news_context}
        
        Provide:
        1. Current market sentiment/trends
        2. Key developments and impact
        3. Risk assessment
        4. Actionable insights
        """
        
        print("Analyzing with real-time news data...")
        analysis = self.llm_service.query_llm(analysis_prompt)
        
        return f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        REAL-TIME NEWS ANALYSIS                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 QUERY: {query}
🏷️  CATEGORY: {category}

📰 REAL-TIME DATA ANALYSIS:
{analysis}

═══════════════════════════════════════════════════════════════════════════════
Based on {len(news_results)} recent articles | NewsData.io + AWS Bedrock
═══════════════════════════════════════════════════════════════════════════════
        """.strip()
    
    def _handle_product_query(self, query: str) -> str:
        """Handle product queries with search data"""
        search_results = self.search_service.search_products(query)
        
        if not search_results:
            return "No product data found for the query."
        
        search_context = "\n".join([
            f"Title: {result['title']}\nSnippet: {result['snippet']}\n"
            for result in search_results
        ])
        
        print(f"\n=== SEARCH DATA RETRIEVED ===")
        for i, result in enumerate(search_results, 1):
            print(f"\nResult {i}:")
            print(f"Title: {result['title']}")
            print(f"Snippet: {result['snippet'][:150]}...")
            print(f"Link: {result['link']}")
        print(f"\n=== END SEARCH DATA ===")
        
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
        
        print("Analyzing product market data...")
        market_analysis = self.llm_service.query_llm(market_analysis_prompt)
        
        print("Generating purchase assessment...")
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
    
    def _handle_general_query(self, query: str) -> str:
        """Handle general queries"""
        general_prompt = f"""
        Provide a comprehensive analysis for: "{query}"
        
        Include relevant insights, recommendations, and actionable information.
        """
        
        print("Processing general query...")
        analysis = self.llm_service.query_llm(general_prompt)
        
        return f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           GENERAL ANALYSIS                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 QUERY: {query}

📝 ANALYSIS:
{analysis}

═══════════════════════════════════════════════════════════════════════════════
General Analysis | AWS Bedrock
═══════════════════════════════════════════════════════════════════════════════
        """.strip()