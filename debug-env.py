#!/usr/bin/env python3

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("=== Environment Variables Debug ===")
print()

# Check all relevant environment variables
env_vars = [
    'GOOGLE_CSE_ID',
    'GOOGLE_API_KEY', 
    'NEWSDATA_API_KEY',
    'AWS_ACCESS_KEY_ID',
    'AWS_SECRET_ACCESS_KEY',
    'AWS_REGION',
    'EC2_PUBLIC_IP'
]

for var in env_vars:
    value = os.getenv(var)
    if value:
        # Mask sensitive values
        if 'KEY' in var or 'SECRET' in var:
            masked = value[:4] + '*' * (len(value) - 8) + value[-4:] if len(value) > 8 else '*' * len(value)
            print(f"✅ {var}: {masked}")
        else:
            print(f"✅ {var}: {value}")
    else:
        print(f"❌ {var}: Not set")

print()
print("=== Configuration Validation ===")

# Test config validation
try:
    from agent.research_agent.config import Config
    
    print(f"Google CSE ID: {'Set' if Config.get_google_cse_id() else 'Missing'}")
    print(f"NewsData API Key: {'Set' if Config.get_newsdata_api_key() else 'Missing'}")
    print(f"AWS Access Key: {'Set' if Config.get_aws_access_key() else 'Missing'}")
    print(f"AWS Secret Key: {'Set' if Config.get_aws_secret_key() else 'Missing'}")
    print(f"AWS Region: {Config.get_aws_region()}")
    
    print()
    validation_result = Config.validate_config()
    print(f"Config Validation: {'✅ PASSED' if validation_result else '❌ FAILED'}")
    
except Exception as e:
    print(f"❌ Config validation error: {e}")

print()
print("=== YouTube Transcript API Test ===")

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    print("✅ YouTube Transcript API imported successfully")
    
    # Test if get_transcript method exists
    if hasattr(YouTubeTranscriptApi, 'get_transcript'):
        print("✅ get_transcript method available")
    else:
        print("❌ get_transcript method not found")
        
except ImportError as e:
    print(f"❌ YouTube Transcript API not installed: {e}")
except Exception as e:
    print(f"❌ YouTube Transcript API error: {e}")