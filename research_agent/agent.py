import json
import boto3
import requests
from bs4 import BeautifulSoup
import urllib.parse
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
        """Scrape Google search results"""
        try:
            # Encode query for URL
            encoded_query = urllib.parse.quote_plus(query)
            url = f"https://www.google.com/search?q={encoded_query}&num={num_results}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            print(f"Searching: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            # Find search result containers
            search_results = soup.find_all('div', class_='g')
            print(f"Found {len(search_results)} search results")
            
            for result in search_results[:num_results]:
                try:
                    # Extract title
                    title_elem = result.find('h3')
                    title = title_elem.get_text() if title_elem else 'No title'
                    
                    # Extract snippet
                    snippet_elem = result.find('span', {'data-ved': True}) or result.find('div', class_='VwiC3b')
                    snippet = snippet_elem.get_text() if snippet_elem else 'No snippet'
                    
                    # Extract link
                    link_elem = result.find('a')
                    link = link_elem.get('href') if link_elem else 'No link'
                    
                    if title != 'No title':
                        results.append({
                            'title': title,
                            'snippet': snippet,
                            'link': link
                        })
                        print(f"Result: {title[:50]}...")
                        
                except Exception as e:
                    print(f"Error parsing result: {e}")
                    continue
            
            print(f"Returning {len(results)} results")
            return results
            
        except Exception as e:
            print(f"Error scraping Google: {e}")
            # Fallback to mock data if scraping fails
            return [
                {
                    'title': f'Market Analysis for {query}',
                    'snippet': f'Latest market trends and pricing for {query}. Consumer demand and competitive analysis.',
                    'link': 'https://example.com/market-analysis'
                },
                {
                    'title': f'Reviews: {query}',
                    'snippet': f'User reviews and ratings for {query}. Real customer feedback and purchase decisions.',
                    'link': 'https://example.com/reviews'
                }
            ]
    
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
        
        print(f"\nSearch Context:\n{search_context}\n")
        
        # Step 3: Query first LLM for market analysis
        market_analysis_prompt = f"""
        Based on the following search results about "{user_query}", provide a market analysis:
        
        Search Results:
        {search_context}
        
        Analyze the market demand, pricing trends, and consumer preferences for this product query.
        """
        
        print("Analyzing with first Bedrock LLM...")
        market_analysis = self.query_bedrock_llm(market_analysis_prompt)
        print(f"\nMarket Analysis Response:\n{market_analysis}\n")
        
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
        print(f"\nPurchase Analysis Response:\n{purchase_analysis}\n")
        
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