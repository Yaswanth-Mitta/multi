from typing import Dict, Any
from .factory import AgentFactory
from .news_service import NewsService
from .search_service import SearchService
from .llm_service import LLMService
from .memory_service import MemoryService

class AIOrchestrator:
    def __init__(self, newsdata_api_key: str, google_cse_id: str, aws_access_key: str = None, aws_secret_key: str = None, aws_region: str = 'us-east-1'):
        # Initialize services
        news_service = NewsService(newsdata_api_key)
        search_service = SearchService(google_cse_id)
        llm_service = LLMService(aws_access_key, aws_secret_key, aws_region)
        
        # Initialize factory with services
        self.factory = AgentFactory(news_service, search_service, llm_service)
        self.llm_service = llm_service
        self.memory = MemoryService()
    
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
            if any(word in query_lower for word in ["mobile", "phone", "laptop", "product", "buy", "price", "camera", "display", "snapdragon", "review", "iphone", "samsung", "unboxing"]):
                classification = "PRODUCT"
            elif any(word in query_lower for word in ["stock", "market", "trading", "investment", "share", "apple", "tesla", "microsoft", "google", "amazon", "reliance", "tcs", "infosys", "aapl", "tsla", "msft"]):
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
    
    def get_memory_status(self) -> str:
        """Get current memory status"""
        if self.memory.has_active_session():
            session = self.memory.get_session_info()
            return f"Active session: {session['product']} ({len(self.memory.conversation_history)} exchanges)"
        return "No active session"
    
    def analyze_query(self, user_query: str) -> str:
        """Main orchestration method with conversational memory"""
        print(f"Processing query: {user_query}")
        
        try:
            # Check if this is a follow-up question to existing research
            if self.memory.has_active_session() and not self._is_new_research_query(user_query):
                print(f"🔄 Detected follow-up question about {self.memory.current_session['product']}")
                return self._handle_followup_query(user_query)
            
            # Clear memory if starting new research
            if self.memory.has_active_session():
                print(f"🔄 Starting new research, clearing previous session")
                self.memory.clear_session()
            
            # Step 1: Classify the query for new research
            category = self.classify_query(user_query)
            print(f"🏭 Getting agent for category: {category}")
            
            # Step 2: Get appropriate agent from factory
            agent = self.factory.get_agent(category)
            print(f"🤖 Got agent: {type(agent).__name__}")
            
            # Step 3: Process query with agent (full research)
            context = {'category': category, 'memory': self.memory}
            print(f"📤 Calling agent.process with context: {context}")
            result = agent.process(user_query, context)
            print(f"📥 Agent returned result length: {len(result)}")
            
            return result
            
        except Exception as e:
            print(f"Error in orchestration: {e}")
            import traceback
            traceback.print_exc()
            return f"Error processing query: {str(e)}"
    
    def _is_new_research_query(self, query: str) -> bool:
        """Determine if this is a new research query or follow-up"""
        query_lower = query.lower()
        
        # Keywords that clearly indicate follow-up questions
        followup_keywords = ['camera', 'battery', 'price', 'color', 'colors', 'screen', 'display', 
                           'performance', 'storage', 'memory', 'size', 'weight', 'features',
                           'what', 'how', 'when', 'where', 'why', 'is it', 'does it', 'can it',
                           'details', 'detail', 'about', 'specs', 'specification']
        
        # If it's clearly a follow-up question
        if any(keyword in query_lower for keyword in followup_keywords):
            return False
        
        # Keywords that indicate new research
        new_research_keywords = ['review of', 'analysis of', 'compare with']
        
        # If query contains completely different product names
        if self.memory.current_session:
            current_product = self.memory.current_session['product'].lower()
            different_products = ['iphone', 'samsung', 'oneplus', 'xiaomi', 'huawei', 'sony', 'lg']
            if any(product in query_lower for product in different_products) and not any(word in current_product for word in query_lower.split()):
                return True
        
        # If it contains explicit new research keywords
        return any(keyword in query_lower for keyword in new_research_keywords)
    
    def _handle_followup_query(self, query: str) -> str:
        """Handle follow-up questions using cached research data"""
        print(f"💬 Conversational Mode: Answering follow-up about {self.memory.current_session['product']}")
        
        # Get research context from memory
        research_context = self.memory.get_research_context()
        
        # Create focused prompt for follow-up
        followup_prompt = f"""
        You are answering a follow-up question about {self.memory.current_session['product']} using previously researched data.
        
        QUESTION: {query}
        
        RESEARCH DATA:
        {research_context}
        
        INSTRUCTIONS:
        - Answer the specific question using the research data
        - Be concise and direct
        - Reference specific details from the research when relevant
        - If the question can't be answered from the data, say so
        """
        
        response = self.llm_service.query_llm(followup_prompt)
        
        # Add to conversation history
        self.memory.add_conversation(query, response)
        
        return f"""
💬 FOLLOW-UP RESPONSE ({self.memory.current_session['product']})

{response}

💡 Ask more questions about this product, or type 'exit' to start fresh research.
        """.strip()
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear_session()
    
