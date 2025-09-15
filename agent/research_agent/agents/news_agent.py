from typing import Dict, Any
from ..interfaces import Agent
from ..news_service import NewsService
from ..llm_service import LLMService

class NewsAgent(Agent):
    def __init__(self, news_service: NewsService, llm_service: LLMService):
        self.news_service = news_service
        self.llm_service = llm_service
    
    def process(self, query: str, context: Dict[str, Any] = None) -> str:
        category = context.get('category', 'NEWS') if context else 'NEWS'
        
        # Get news data
        news_results = self.news_service.search_news(query)
        if not news_results:
            return "No real-time data found for the query."
        
        news_context = "\n".join([
            f"Title: {article['title']}\nDescription: {article['description']}\nSource: {article['source_id']}\nDate: {article['pubDate']}\n"
            for article in news_results[:3]
        ])
        
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
    
    def get_agent_type(self) -> str:
        return "NEWS"