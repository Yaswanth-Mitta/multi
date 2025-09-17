# AI Research Agent Backend

Python Flask backend for the AI Research Agent system with multi-agent architecture.

## Features

- **Multi-Agent System**: News, Product, General, and Validator agents
- **SERP API Integration**: Enhanced search capabilities
- **YouTube Analysis**: Video transcript extraction and analysis
- **E-commerce Scraping**: Product data from multiple platforms
- **AWS Bedrock LLM**: Advanced AI analysis
- **Memory Management**: Conversational context retention

## Quick Start

### Windows
```bash
start.bat
```

### Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

### Manual Setup
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
python server.py
```

## Configuration

Create `.env` file in the root directory:

```env
# Required APIs
SERP_API_KEY=your_serp_api_key
NEWSDATA_API_KEY=your_newsdata_api_key
TAVILY_API_KEY=your_tavily_api_key

# AWS Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1

# Optional
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_cse_id
PUBLIC_IP=your_server_ip
```

## API Endpoints

- `GET /` - Health check
- `POST /research` - Process research query

## Architecture

```
backend/
├── agents/           # AI agents
├── services/         # Core services
├── main.py          # Console interface
├── server.py        # Flask web server
├── orchestrator.py  # Main orchestrator
├── factory.py       # Agent factory
└── config.py        # Configuration
```

## Services

- **SERP Service**: Google, YouTube, Shopping, News search
- **YouTube Service**: Video transcript extraction
- **E-commerce Service**: Product data scraping
- **LLM Service**: AWS Bedrock integration
- **News Service**: Real-time news data
- **Stock Service**: Financial data analysis