import json
import boto3
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