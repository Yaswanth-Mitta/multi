import os
from typing import Optional

class Config:
    @staticmethod
    def get_google_cse_id() -> Optional[str]:
        return os.getenv('GOOGLE_CSE_ID')
    
    @staticmethod
    def get_aws_region() -> str:
        return os.getenv('AWS_REGION', 'us-east-1')
    
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
        
        if not newsdata_key:
            print("Error: NEWSDATA_API_KEY environment variable not set")
            return False
        
        return True