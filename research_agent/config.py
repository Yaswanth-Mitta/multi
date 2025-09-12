import os
from typing import Optional

class Config:
    """Configuration class for Research Agent"""
    
    @staticmethod
    def get_google_api_key() -> Optional[str]:
        return os.getenv('GOOGLE_API_KEY')
    
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
    def validate_config() -> bool:
        """Validate that all required configuration is present"""
        google_cse_id = Config.get_google_cse_id()
        
        if not google_cse_id:
            print("Error: GOOGLE_CSE_ID environment variable not set")
            return False
        
        return True