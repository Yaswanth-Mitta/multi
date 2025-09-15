import json
import boto3
import os
from typing import Optional

class LLMService:
    def __init__(self, aws_access_key: str = None, aws_secret_key: str = None, aws_region: str = 'us-east-1'):
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
    
    def query_llm(self, prompt: str, model_id: str = 'anthropic.claude-3-5-sonnet-20240620-v1:0') -> str:
        """Query Bedrock LLM with the given prompt"""
        # List of fallback models to try
        models_to_try = [
            model_id,
            'anthropic.claude-3-sonnet-20240229-v1:0',
            'anthropic.claude-v2:1',
            'anthropic.claude-v2'
        ]
        
        for model in models_to_try:
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
                    modelId=model,
                    accept='application/json',
                    contentType='application/json'
                )
                
                response_body = json.loads(response.get('body').read())
                return response_body['content'][0]['text']
                
            except Exception as e:
                if "security token" in str(e).lower():
                    print(f"AWS credentials invalid. Please check your .env file.")
                    break  # No point trying other models with bad credentials
                print(f"Failed with model {model}: {e}")
                continue
        
        # If all models fail, return fallback response
        print(f"All Bedrock models failed. Using fallback logic.")
        if "classification" in prompt.lower():
            # Simple keyword-based classification fallback
            query_lower = prompt.lower()
            if any(word in query_lower for word in ["mobile", "phone", "laptop", "product", "snapdragon", "camera", "display"]):
                return "PRODUCT"
            elif any(word in query_lower for word in ["stock", "market", "trading"]):
                return "STOCKS"
            elif any(word in query_lower for word in ["news", "breaking"]):
                return "NEWS"
            else:
                return "GENERAL"
        
        # For analysis prompts, return a basic response
        return f"Analysis for query: Based on the information provided, this appears to be a product-related inquiry. The system is currently operating in fallback mode due to LLM service issues."