# Research Agent

A Python-based research agent that analyzes product queries using Google Search API and AWS Bedrock LLMs to provide market analysis and purchase likelihood assessments.

## Features

- Fetches real-time data from Google Search API
- Uses two AWS Bedrock LLMs for comprehensive analysis
- Provides market analysis and purchase likelihood assessment
- Interactive console interface

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Set your Google API credentials:
     - `GOOGLE_API_KEY`: Get from Google Cloud Console
     - `GOOGLE_CSE_ID`: Create a Custom Search Engine at https://cse.google.com/
   - Configure AWS credentials (AWS CLI, IAM role, or environment variables)

3. **Run the application:**
   ```bash
   python main.py
   ```

## Usage

Run the main script and enter product queries like:
- "mobile with 8 gb ram, hd camera at 40000k how likely someone will buy this"
- "laptop with 16gb ram under 50000"
- "wireless headphones with noise cancellation"

The agent will:
1. Search Google for relevant market data
2. Analyze market trends using first Bedrock LLM
3. Assess purchase likelihood using second Bedrock LLM
4. Provide refined, actionable insights

## Requirements

- Python 3.7+
- Google Custom Search API key and CSE ID
- AWS account with Bedrock access
- Internet connection for API calls
