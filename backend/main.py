#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from orchestrator import AIOrchestrator
from config import Config

# Load environment variables from .env file
load_dotenv()

def main():
    """Main function to run the Research Agent"""
    print("=== AI Research Orchestrator ===")
    print("Clean Architecture Multi-Agent LLM System:")
    print("📰 News/Stocks Agent → Real-time NewsData.io API")
    print("🛍️  Product Agent → Google Search + Market Analysis")
    print("🤖 General Agent → Comprehensive Analysis")
    print("✅ Validator Agent → Information Validation")
    print("🏭 Factory Pattern → Dynamic Agent Creation")
    print("🎯 Orchestrator → Centralized Workflow Control")
    print()
    
    # Validate configuration
    if not Config.validate_config():
        print("\nConfiguration check completed.")
        print("System will work with available services.")
        print("\nOptional enhancements:")
        print("- NEWSDATA_API_KEY: For real news data (currently using fallback)")
        print("- GOOGLE_CSE_ID: For Google search (currently using enhanced search)")
        print("- AWS credentials: For LLM analysis (configure if needed)")
    
    # Initialize the AI orchestrator
    try:
        orchestrator = AIOrchestrator(
            newsdata_api_key=Config.get_newsdata_api_key(),
            google_cse_id=Config.get_google_cse_id(),
            serp_api_key=Config.get_serp_api_key(),
            aws_access_key=Config.get_aws_access_key(),
            aws_secret_key=Config.get_aws_secret_key(),
            aws_region=Config.get_aws_region()
        )
        print("✅ AI Orchestrator initialized successfully!")
        print("🔄 All services ready - enhanced search, YouTube analysis, web scraping")
        print()
    except Exception as e:
        print(f"Error initializing AI Orchestrator: {e}")
        return
    
    # Main interaction loop
    while True:
        try:
            print("-" * 50)
            
            # Show memory status
            memory_status = orchestrator.get_memory_status()
            if "Active session" in memory_status:
                print(f"💭 {memory_status}")
                user_input = input("Ask follow-up question or 'exit' to start fresh: ").strip()
                
                if user_input.lower() == 'exit':
                    orchestrator.clear_memory()
                    print("🔄 Memory cleared. Starting fresh research.")
                    continue
            else:
                user_input = input("Enter your product/market query (or 'quit' to exit): ").strip()
            
            if user_input.lower() in ['quit', 'q']:
                print("Goodbye!")
                break
            
            if not user_input:
                print("Please enter a valid query.")
                continue
            
            print()
            # Process the query
            result = orchestrator.analyze_query(user_input)
            print(result)
            print()
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error processing query: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()