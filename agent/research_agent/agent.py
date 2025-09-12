from typing import Dict, List, Any
from .news_service import NewsService
from .llm_service import LLMService

class ResearchAgent:
    def __init__(self, newsdata_api_key: str, aws_access_key: str = None, aws_secret_key: str = None, aws_region: str = 'us-east-1'):
        self.news_service = NewsService(newsdata_api_key)
        self.llm_service = LLMService(aws_access_key, aws_secret_key, aws_region)
    
    def analyze_query(self, user_query: str) -> str:
        """Main method to process user query and return refined output"""
        print(f"Processing query: {user_query}")
        
        # Step 1: Search for real-time news data
        news_results = self.news_service.search_news(user_query)
        
        if not news_results:
            return "No news data found for the query."
        
        # Step 2: Prepare context from news results
        news_context = "\n".join([
            f"Title: {article['title']}\nDescription: {article['description']}\nSource: {article['source_id']}\nDate: {article['pubDate']}\n"
            for article in news_results[:3]
        ])
        
        # Step 3: Market analysis with first LLM
        market_analysis_prompt = f"""
        Based on the following real-time news data about "{user_query}", provide a comprehensive market analysis:
        
        News Data:
        {news_context}
        
        Analyze:
        1. Current market trends and sentiment
        2. Recent developments and news impact
        3. Consumer behavior patterns
        4. Competitive landscape
        5. Market opportunities and risks
        
        Provide detailed market insights.
        """
        
        print("Analyzing market trends with Bedrock LLM...")
        market_analysis = self.llm_service.query_llm(market_analysis_prompt)
        
        # Step 4: Purchase likelihood assessment with second LLM
        purchase_likelihood_prompt = f"""
        Product Query: "{user_query}"
        
        Market Analysis:
        {market_analysis}
        
        Based on real-time news data and market analysis, provide:
        
        1. Purchase Likelihood Score (0-100%)
        2. Key Market Drivers
        3. Consumer Sentiment Analysis
        4. Risk Factors
        5. Investment/Purchase Recommendations
        6. Market Timing Analysis
        
        Provide actionable insights based on current market conditions.
        """
        
        print("Generating purchase likelihood assessment...")
        purchase_analysis = self.llm_service.query_llm(purchase_likelihood_prompt)
        
        # Step 5: Generate final report
        final_report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     REAL-TIME RESEARCH AGENT ANALYSIS                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 QUERY: {user_query}

📰 REAL-TIME NEWS INSIGHTS:
Based on {len(news_results)} recent news articles

📊 MARKET ANALYSIS:
{market_analysis}

🎯 PURCHASE LIKELIHOOD ASSESSMENT:
{purchase_analysis}

═══════════════════════════════════════════════════════════════════════════════
Report Generated with Real-Time Data | NewsData.io + AWS Bedrock
═══════════════════════════════════════════════════════════════════════════════
        """
        
        return final_report.strip()