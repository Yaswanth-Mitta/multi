from typing import Dict, Any
from ..interfaces import Agent
from ..news_service import NewsService
from ..llm_service import LLMService
from ..stock_service import StockService

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
        # COMMENTED OUT - PAID SERVICE
        # news_results = self.news_service.search_news(query)
        # if not news_results:
        #     return "No real-time data found for the query."
        
        news_context = f"News service disabled (NewsData.io is paid). Query was: {query}"
        
        return f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        NEWS SERVICE DISABLED                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 QUERY: {query}
🏷️  CATEGORY: {category}

📰 NEWS SERVICE STATUS:
NewsData.io service is disabled (paid service)
For stock queries, use stock-specific commands instead.

═══════════════════════════════════════════════════════════════════════════════
News Service Disabled | Use Stock Analysis Instead
═══════════════════════════════════════════════════════════════════════════════
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
┌─────────────────────────────────────────────────────────────┐
│  {data['name']} ({data['symbol']})                          
└─────────────────────────────────────────────────────────────┘

💰 CURRENT TRADING SESSION:
   ├─ Current Price: ${data['current_price']}
   ├─ Change: ${data['change']} ({data['change_percent']:+.2f}%)
   ├─ Today's Open: ${data['today_open']}
   ├─ Day Range: ${data['today_low']} - ${data['today_high']}
   └─ Volume: {data['today_volume']:,}

📈 PREVIOUS SESSION:
   ├─ Yesterday Open: ${data['yesterday_open']}
   ├─ Yesterday Close: ${data['yesterday_close']}
   ├─ Yesterday Range: ${data['yesterday_low']} - ${data['yesterday_high']}
   └─ Yesterday Volume: {data['yesterday_volume']:,}

📊 KEY METRICS:
   ├─ Market Cap: ${data['market_cap']:,}
   ├─ P/E Ratio: {data['pe_ratio']}
   └─ 52-Week Range: ${data['52_week_low']} - ${data['52_week_high']}

"""
        
        # Step 3: Get market summary
        market_summary = self.stock_service.get_market_summary()
        market_context = "\nMarket Indices:\n"
        for index, data in market_summary.items():
            market_context += f"{index}: ${data['price']} ({data['change_percent']:+.2f}%)\n"
        
        # Step 4: Get related news for the company (COMMENTED OUT - PAID SERVICE)
        print("Skipping news fetch (paid service)...")
        news_context = "\n📰 News Analysis: Skipped (NewsData.io is a paid service)\n"
        
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
╔══════════════════════════════════════════════════════════════════════════════╗
║                     COMPREHENSIVE STOCK ANALYSIS                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 QUERY: {query}

📊 REAL-TIME STOCK DATA:
{stock_data_context}
{market_context}

📰 RECENT NEWS & DEVELOPMENTS:
{news_context}

📈 COMPREHENSIVE ANALYSIS:
{analysis}

═══════════════════════════════════════════════════════════════════════════════
Real-time Stock Data + News Analysis | Yahoo Finance + NewsData.io + AWS Bedrock
═══════════════════════════════════════════════════════════════════════════════
        """.strip()
    
    def get_agent_type(self) -> str:
        return "NEWS"