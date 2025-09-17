#!/usr/bin/env python3
"""Test script to validate all imports"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    print("🧪 Testing all imports...")
    
    try:
        print("✅ Testing config...")
        from config import Config
        
        print("✅ Testing interfaces...")
        from interfaces import Agent
        
        print("✅ Testing services...")
        from services.llm_service import LLMService
        from services.news_service import NewsService
        from services.search_service import SearchService
        from services.serp_service import SerpService
        from services.enhanced_search_service import EnhancedSearchService
        from services.enhanced_scraper_service import EnhancedScraperService
        from services.enhanced_ecommerce_service import EnhancedEcommerceService
        from services.youtube_service import YouTubeService
        from services.stock_service import StockService
        from services.memory_service import MemoryService
        from services.langchain_service import LangChainService
        
        print("✅ Testing agents...")
        from agents.news_agent import NewsAgent
        from agents.product_agent import ProductAgent
        from agents.general_agent import GeneralAgent
        from agents.validator_agent import ValidatorAgent
        
        print("✅ Testing factory...")
        from factory import AgentFactory
        
        print("✅ Testing orchestrator...")
        from orchestrator import AIOrchestrator
        
        print("🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)