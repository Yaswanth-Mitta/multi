import yfinance as yf
from typing import Dict, Any, List
import pandas as pd

class StockService:
    def __init__(self):
        pass
    
    def get_stock_data(self, symbol: str) -> Dict[str, Any]:
        """Get real-time stock data for a symbol"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            hist = stock.history(period="5d")
            
            if hist.empty:
                return None
            
            current_price = hist['Close'].iloc[-1]
            prev_close = info.get('previousClose', hist['Close'].iloc[-2] if len(hist) > 1 else current_price)
            change = current_price - prev_close
            change_percent = (change / prev_close) * 100 if prev_close else 0
            
            return {
                'symbol': symbol.upper(),
                'name': info.get('longName', symbol),
                'current_price': round(current_price, 2),
                'previous_close': round(prev_close, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'day_high': round(hist['High'].iloc[-1], 2),
                'day_low': round(hist['Low'].iloc[-1], 2),
                '52_week_high': info.get('fiftyTwoWeekHigh', 'N/A'),
                '52_week_low': info.get('fiftyTwoWeekLow', 'N/A')
            }
            
        except Exception as e:
            print(f"Error fetching stock data for {symbol}: {e}")
            return None
    
    def search_stock_symbol(self, query: str) -> List[str]:
        """Search for stock symbols based on company name"""
        # Common stock symbols mapping
        common_stocks = {
            'apple': 'AAPL', 'microsoft': 'MSFT', 'google': 'GOOGL', 'alphabet': 'GOOGL',
            'amazon': 'AMZN', 'tesla': 'TSLA', 'meta': 'META', 'facebook': 'META',
            'netflix': 'NFLX', 'nvidia': 'NVDA', 'intel': 'INTC', 'amd': 'AMD',
            'reliance': 'RELIANCE.NS', 'tcs': 'TCS.NS', 'infosys': 'INFY.NS',
            'hdfc': 'HDFCBANK.NS', 'icici': 'ICICIBANK.NS', 'sbi': 'SBIN.NS'
        }
        
        query_lower = query.lower()
        symbols = []
        
        # Direct symbol match
        if query.upper() in ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NFLX', 'NVDA']:
            symbols.append(query.upper())
        
        # Company name match
        for company, symbol in common_stocks.items():
            if company in query_lower:
                symbols.append(symbol)
        
        return symbols[:3]  # Return top 3 matches
    
    def get_market_summary(self) -> Dict[str, Any]:
        """Get major market indices"""
        try:
            indices = {
                'S&P 500': '^GSPC',
                'Dow Jones': '^DJI',
                'NASDAQ': '^IXIC',
                'Nifty 50': '^NSEI'
            }
            
            summary = {}
            for name, symbol in indices.items():
                data = self.get_stock_data(symbol)
                if data:
                    summary[name] = {
                        'price': data['current_price'],
                        'change': data['change'],
                        'change_percent': data['change_percent']
                    }
            
            return summary
            
        except Exception as e:
            print(f"Error fetching market summary: {e}")
            return {}