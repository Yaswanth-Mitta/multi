from typing import Dict, Any
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from interfaces import Agent
from services.news_service import NewsService
from services.llm_service import LLMService
from services.stock_service import StockService

class NewsAgent(Agent):
    def __init__(self, news_service: NewsService, llm_service: LLMService):
        self.news_service = news_service
        self.llm_service = llm_service
        self.stock_service = StockService()
    
    def process(self, query: str, context: Dict[str, Any] = None) -> str:
        category = context.get('category', 'NEWS') if context else 'NEWS'
        print(f"📊 NewsAgent processing: category={category}")
        
        # Handle stock queries with real-time data
        if category == 'STOCKS':
            print("🎯 Routing to stock handler")
            return self._handle_stock_query(query)
        
        # Handle regular news queries
        print("📰 Routing to news handler")
        return self._handle_news_query(query, category)
    
    def _handle_news_query(self, query: str, category: str) -> str:
        """Handle regular news queries"""
        news_results = self.news_service.search_news(query)
        if not news_results:
            return "No real-time news data found for the query."
        
        # Create news context from results
        news_context = "\n=== LATEST NEWS ARTICLES ===\n"
        for i, article in enumerate(news_results, 1):
            news_context += f"\n{i}. {article['title']}\n"
            news_context += f"   Source: {article['source_id']}\n"
            news_context += f"   Published: {article['pubDate']}\n"
            news_context += f"   Summary: {article['description']}\n"
            if article['content']:
                news_context += f"   Content: {article['content'][:300]}...\n"
            news_context += f"   URL: {article['link']}\n"
        
        # Analyze news with LLM
        analysis_prompt = f"""
        Analyze the following news articles about "{query}" and provide comprehensive insights:
        
        {news_context}
        
        Provide:
        1. Key Developments Summary
        2. Impact Analysis
        3. Trend Identification
        4. Future Implications
        5. Stakeholder Effects
        
        Focus on factual analysis based on the provided news content.
        """
        
        analysis = self.llm_service.query_llm(analysis_prompt)
        
        return f"""
## 📰 COMPREHENSIVE NEWS ANALYSIS

**Query:** {query}  
**Category:** {category}

### 📅 Latest News Coverage
{news_context}

### 📊 Analysis & Insights
{analysis}

---
*Data Sources: NewsData.io • AWS Bedrock AI*
        """.strip()
    
    def _handle_stock_query(self, query: str) -> str:
        """Handle stock-specific queries with real-time data and news"""
        print("🔍 ENTERING STOCK HANDLER")
        print("Fetching real-time stock data...")
        
        # Step 1: Search for stock symbols
        symbols = self.stock_service.search_stock_symbol(query)
        print(f"Found symbols: {symbols}")
        
        if not symbols:
            return "No stock symbols found for the query. Please use specific company names or stock symbols."
        
        # Step 2: Get real-time stock data
        stock_data_context = ""
        company_names = []
        
        for symbol in symbols:
            data = self.stock_service.get_stock_data(symbol)
            print(f"Stock data for {symbol}: {data}")
            if data:
                company_names.append(data['name'])
                stock_data_context += f"""
**{data['name']} ({data['symbol']})**

**Current Trading:**
- Price: ${data['current_price']}
- Change: ${data['change']} ({data['change_percent']:+.2f}%)
- Day Range: ${data['today_low']} - ${data['today_high']}
- Volume: {data['today_volume']:,}

**Key Metrics:**
- Market Cap: ${data['market_cap']:,}
- P/E Ratio: {data['pe_ratio']}
- 52-Week Range: ${data['52_week_low']} - ${data['52_week_high']}

"""
        
        # Step 3: Get market summary
        market_summary = self.stock_service.get_market_summary()
        market_context = "**Market Overview:**\n"
        for index, data in market_summary.items():
            market_context += f"- {index}: ${data['price']} ({data['change_percent']:+.2f}%)\n"
        
        # Step 4: Get related news for the company
        print("Fetching company news...")
        company_query = " OR ".join(company_names) if company_names else query
        news_results = self.news_service.search_news(company_query, size=3)
        
        news_context = "\n📰 RECENT NEWS & DEVELOPMENTS:\n"
        if news_results:
            for article in news_results:
                news_context += f"• {article['title']} ({article['source_id']})\n"
                news_context += f"  {article['description']}\n\n"
        else:
            news_context += "No recent news found for the queried companies.\n"
        
        # Step 5: Combine all data and send to LLM
        print("Analyzing with LLM...")
        
        analysis_prompt = f"""
        Provide comprehensive stock market analysis for: "{query}"
        
        REAL-TIME STOCK DATA:
        {stock_data_context}
        
        MARKET CONTEXT:
        {market_context}
        
        Based on the real-time stock data, provide:
        1. Current Stock Performance Analysis
        2. Technical Analysis (price trends, volume)
        3. Market Position & Valuation
        4. Investment Recommendation (Buy/Hold/Sell)
        5. Risk Factors & Opportunities
        6. Price Target & Timeline
        
        Make your analysis data-driven using the provided real-time information.
        """
        
        analysis = self.llm_service.query_llm(analysis_prompt)
        
        return f"""
## 📈 COMPREHENSIVE STOCK ANALYSIS

**Query:** {query}

### 📊 Real-Time Market Data
{stock_data_context}

### 🌍 Market Overview
{market_context}

### 📰 Latest News & Developments
{news_context}

### 🎯 Investment Analysis
{analysis}

---
*Data Sources: Yahoo Finance • NewsData.io • AWS Bedrock AI*
        """.strip()
    
    def get_agent_type(self) -> str:
        return "NEWS"