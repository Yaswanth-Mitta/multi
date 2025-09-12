#!/usr/bin/env python3

from dotenv import load_dotenv
from research_agent.agent import ResearchAgent
from research_agent.config import Config

# Load environment variables from .env file
load_dotenv()

def main():
    """Main function to run the Research Agent"""
    print("=== Research Agent ===")
    print("This agent will analyze product queries using Google Search and AWS Bedrock LLMs")
    print()
    
    # Validate configuration
    if not Config.validate_config():
        print("\nPlease set the required environment variables:")
        print("- GOOGLE_API_KEY: Your Google Custom Search API key")
        print("- GOOGLE_CSE_ID: Your Google Custom Search Engine ID")
        print("- AWS credentials should be configured (AWS CLI, IAM role, or environment variables)")
        print("\nGet Google API key from: https://console.cloud.google.com/")
        print("Enable Custom Search API and create credentials")
        return
    
    # Initialize the research agent
    try:
        agent = ResearchAgent(
            google_api_key=Config.get_google_api_key(),
            google_cse_id=Config.get_google_cse_id(),
            aws_access_key=Config.get_aws_access_key(),
            aws_secret_key=Config.get_aws_secret_key(),
            aws_region=Config.get_aws_region()
        )
        print("Research Agent initialized successfully!")
        print()
    except Exception as e:
        print(f"Error initializing Research Agent: {e}")
        return
    
    # Main interaction loop
    while True:
        try:
            print("-" * 50)
            user_input = input("Enter your product query (or 'quit' to exit): ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not user_input:
                print("Please enter a valid query.")
                continue
            
            print()
            # Process the query
            result = agent.analyze_query(user_input)
            print()
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