import os
from typing import Optional

class Config:
    @staticmethod
    def get_google_cse_id() -> Optional[str]:
        return os.getenv('GOOGLE_CSE_ID')
    
    @staticmethod
    def get_aws_region() -> str:
        return os.getenv('AWS_REGION') or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    
    @staticmethod
    def get_aws_access_key() -> Optional[str]:
        return os.getenv('AWS_ACCESS_KEY_ID')
    
    @staticmethod
    def get_aws_secret_key() -> Optional[str]:
        return os.getenv('AWS_SECRET_ACCESS_KEY')
    
    @staticmethod
    def get_newsdata_api_key() -> Optional[str]:
        return os.getenv('NEWSDATA_API_KEY')
    
    @staticmethod
    def validate_config() -> bool:
        """Validate that all required configuration is present"""
        newsdata_key = Config.get_newsdata_api_key()
        google_cse_id = Config.get_google_cse_id()
        
        # NewsData API is optional (paid service, currently disabled)
        if not newsdata_key:
            print("Info: NEWSDATA_API_KEY not set (news service will be disabled)")
        
        # Google API is optional (enhanced search service provides fallback)
        if not google_cse_id:
            print("Info: GOOGLE_CSE_ID not set (using enhanced search fallback)")
        
        # Always return True - system works without external APIs
        return True