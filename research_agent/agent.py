import json
import boto3
import requests
from typing import Dict, List, Any

class ResearchAgent:
    def __init__(self, google_api_key: str, google_cse_id: str, aws_access_key: str = None, aws_secret_key: str = None, aws_region: str = 'us-east-1'):
        self.google_api_key = google_api_key
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
        """Search using Google Custom Search API"""
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': self.google_api_key,
                'cx': self.google_cse_id,
                'q': query,
                'num': num_results
            }
            
            print(f"Searching Google for: {query}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get('items', []):
                results.append({
                    'title': item.get('title', ''),
                    'snippet': item.get('snippet', ''),
                    'link': item.get('link', '')
                })
            
            print(f"Found {len(results)} search results")
            return results
            
        except Exception as e:
            print(f"Error searching Google: {e}")
            return []
    
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
        search_results = self.search_google(user_query)
        
        if not search_results:
            return "No search results found."
        
        # Step 2: Prepare context from search results
        search_context = "\n".join([
            f"Title: {result['title']}\nSnippet: {result['snippet']}\nURL: {result['link']}\n"
            for result in search_results
        ])
        
        # Step 3: Query first LLM for market analysis
        market_analysis_prompt = f"""
        Based on the following Google search results about "{user_query}", provide a comprehensive market analysis:
        
        Search Results:
        {search_context}
        
        Please analyze:
        1. Market demand and trends
        2. Pricing analysis
        3. Consumer preferences
        4. Competitive landscape
        5. Market opportunities
        
        Provide a detailed market analysis report.
        """
        
        print("Analyzing market trends with Bedrock LLM...")
        market_analysis = self.query_bedrock_llm(market_analysis_prompt)
        
        # Step 4: Query second LLM for purchase likelihood
        purchase_likelihood_prompt = f"""
        Product Query: "{user_query}"
        
        Market Analysis:
        {market_analysis}
        
        Based on the above information, provide a detailed purchase likelihood assessment including:
        
        1. Purchase Likelihood Score (0-100%)
        2. Key Buying Factors
        3. Target Customer Profile
        4. Price Sensitivity Analysis
        5. Recommendations for Success
        6. Potential Challenges
        
        Provide actionable insights and recommendations.
        """
        
        print("Generating purchase likelihood assessment...")
        purchase_analysis = self.query_bedrock_llm(purchase_likelihood_prompt)
        
        # Step 5: Generate final report
        final_report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           RESEARCH AGENT ANALYSIS REPORT                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 QUERY: {user_query}

📊 MARKET ANALYSIS:
{market_analysis}

🎯 PURCHASE LIKELIHOOD ASSESSMENT:
{purchase_analysis}

═══════════════════════════════════════════════════════════════════════════════
Report Generated by Research Agent | Powered by AWS Bedrock & Google Search
═══════════════════════════════════════════════════════════════════════════════
        """
        
        return final_report.strip()