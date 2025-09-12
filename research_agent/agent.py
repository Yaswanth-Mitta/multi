import json
import boto3
import requests
from typing import Dict, List, Any

class ResearchAgent:
    def __init__(self, google_cse_id: str, aws_access_key: str = None, aws_secret_key: str = None, aws_region: str = 'us-east-1'):
        self.google_cse_id = google_cse_id
        
        # Configure boto3 client with credentials if provided
        if aws_access_key and aws_secret_key:
            self.bedrock_client = boto3.client(
                'bedrock-runtime',
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=aws_region
            )
        else:
            self.bedrock_client = boto3.client('bedrock-runtime', region_name=aws_region)
        
    def search_google(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Simulate search results for the query"""
        # Since you mentioned no API key needed, using mock data
        # Replace this with your actual search implementation
        mock_results = [
            {
                'title': f'Market Analysis for {query}',
                'snippet': f'Latest market trends and pricing information for {query}. Consumer demand analysis and competitive landscape.',
                'link': 'https://example.com/market-analysis'
            },
            {
                'title': f'Consumer Reviews: {query}',
                'snippet': f'User reviews and ratings for {query}. Purchase decisions and satisfaction ratings from real customers.',
                'link': 'https://example.com/reviews'
            },
            {
                'title': f'Price Comparison: {query}',
                'snippet': f'Compare prices for {query} across different retailers. Best deals and offers available.',
                'link': 'https://example.com/price-comparison'
            }
        ]
        return mock_results[:num_results]
    
    def query_bedrock_llm(self, prompt: str, model_id: str = 'anthropic.claude-3-5-sonnet-20240620-v1:0') -> str:
        """Query Bedrock LLM with the given prompt"""
        try:
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
            
            response = self.bedrock_client.invoke_model(
                body=body,
                modelId=model_id,
                accept='application/json',
                contentType='application/json'
            )
            
            response_body = json.loads(response.get('body').read())
            return response_body['content'][0]['text']
        except Exception as e:
            print(f"Error querying Bedrock LLM: {e}")
            return ""
    
    def analyze_query(self, user_query: str) -> str:
        """Main method to process user query and return refined output"""
        print(f"Processing query: {user_query}")
        
        # Step 1: Search Google for relevant information
        print("Fetching data from Google Search...")
        search_results = self.search_google(user_query)
        
        if not search_results:
            return "No search results found."
        
        # Step 2: Prepare context from search results
        search_context = "\n".join([
            f"Title: {result['title']}\nSnippet: {result['snippet']}\n"
            for result in search_results[:3]  # Use top 3 results
        ])
        
        # Step 3: Query first LLM for market analysis
        market_analysis_prompt = f"""
        Based on the following search results about "{user_query}", provide a market analysis:
        
        Search Results:
        {search_context}
        
        Analyze the market demand, pricing trends, and consumer preferences for this product query.
        """
        
        print("Analyzing with first Bedrock LLM...")
        market_analysis = self.query_bedrock_llm(market_analysis_prompt)
        
        # Step 4: Query second LLM for purchase likelihood
        purchase_likelihood_prompt = f"""
        Given this product query: "{user_query}"
        And this market analysis: {market_analysis}
        
        Provide a detailed assessment of how likely someone would buy this product, including:
        1. Purchase likelihood percentage
        2. Key factors influencing the decision
        3. Target audience analysis
        4. Recommendations for improvement
        
        Keep the response concise and actionable.
        """
        
        print("Getting purchase likelihood analysis from second Bedrock LLM...")
        purchase_analysis = self.query_bedrock_llm(purchase_likelihood_prompt)
        
        # Step 5: Combine and refine the output
        final_output = f"""
=== RESEARCH AGENT ANALYSIS ===

Query: {user_query}

MARKET ANALYSIS:
{market_analysis}

PURCHASE LIKELIHOOD ASSESSMENT:
{purchase_analysis}

=== END ANALYSIS ===
        """
        
        return final_output.strip()