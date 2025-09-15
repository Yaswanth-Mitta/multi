from typing import Dict, Any
from .factory import AgentFactory
from .news_service import NewsService
from .search_service import SearchService
from .llm_service import LLMService

class AIOrchestrator:
    def __init__(self, newsdata_api_key: str, google_cse_id: str, aws_access_key: str = None, aws_secret_key: str = None, aws_region: str = 'us-east-1'):
        # Initialize services
        news_service = NewsService(newsdata_api_key)
        search_service = SearchService(google_cse_id)
        llm_service = LLMService(aws_access_key, aws_secret_key, aws_region)
        
        # Initialize factory with services
        self.factory = AgentFactory(news_service, search_service, llm_service)
        self.llm_service = llm_service
    
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
        
        # Fallback if LLM fails or returns empty
        if not classification or classification not in ["STOCKS", "NEWS", "PRODUCT", "GENERAL"]:
            # Simple keyword-based fallback
            query_lower = query.lower()
            if any(word in query_lower for word in ["mobile", "phone", "laptop", "product", "buy", "price", "camera", "display"]):
                classification = "PRODUCT"
            elif any(word in query_lower for word in ["stock", "market", "trading", "investment"]):
                classification = "STOCKS"
            elif any(word in query_lower for word in ["news", "breaking", "latest"]):
                classification = "NEWS"
            else:
                classification = "GENERAL"
        
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
        
        try:
            # Step 1: Classify the query
            category = self.classify_query(user_query)
            
            # Step 2: Get appropriate agent from factory
            agent = self.factory.get_agent(category)
            
            # Step 3: Process query with agent
            context = {'category': category}
            return agent.process(user_query, context)
            
        except Exception as e:
            print(f"Error in orchestration: {e}")
            return f"Error processing query: {str(e)}"
    
