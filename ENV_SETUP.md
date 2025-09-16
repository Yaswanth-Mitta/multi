# Environment Setup Guide

## Required API Keys

### 1. NewsData.io API Key
- **Website**: https://newsdata.io/
- **Free Tier**: 200 requests/day
- **Steps**:
  1. Sign up for free account
  2. Get API key from dashboard
  3. Add to `.env` as `NEWSDATA_API_KEY`

### 2. Google Custom Search Engine
- **API Console**: https://console.cloud.google.com/
- **CSE Setup**: https://cse.google.com/
- **Steps**:
  1. Create Google Cloud project
  2. Enable Custom Search API
  3. Create API key
  4. Create Custom Search Engine
  5. Add both to `.env`

### 3. AWS Bedrock Access
- **Console**: https://console.aws.amazon.com/
- **Requirements**: AWS account with Bedrock access
- **Options**:
  
  **Option A - IAM Credentials:**
  ```bash
  AWS_ACCESS_KEY_ID=your_key
  AWS_SECRET_ACCESS_KEY=your_secret
  ```
  
  **Option B - AWS CLI:**
  ```bash
  aws configure
  # Leave AWS credentials empty in .env
  ```

## Quick Setup

1. **Copy template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit with your keys:**
   ```bash
   nano .env
   ```

3. **Test configuration:**
   ```bash
   python -c "from agent.research_agent.config import Config; print('✅ Config valid' if Config.validate_config() else '❌ Config invalid')"
   ```