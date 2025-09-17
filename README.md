# AI Research Agent

A comprehensive AI-powered research system with Next.js frontend and Python backend featuring multi-agent architecture, SERP API integration, and advanced LLM analysis.

## 🏗️ Architecture

```
Amit/
├── frontend-nextjs/     # Next.js frontend application
│   ├── app/            # Next.js app router
│   ├── components/     # React components
│   └── lib/           # Utilities
├── backend/            # Python Flask backend
│   ├── agents/        # AI agents (News, Product, General, Validator)
│   ├── services/      # Core services (SERP, YouTube, E-commerce, LLM)
│   ├── server.py      # Flask web server
│   └── main.py        # Console interface
└── .env               # Environment configuration
```

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Add your API keys to .env
SERP_API_KEY=your_serp_api_key
NEWSDATA_API_KEY=your_newsdata_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
PUBLIC_IP=your_server_ip
```

### 2. Docker Deployment (Recommended)
```bash
# Build images
./build.sh  # Linux/Mac or build.bat for Windows

# Start services
docker-compose up -d
```

### 3. Kubernetes Deployment
```bash
# Build images
./build.sh

# Deploy to cluster
cd k8s && kubectl apply -f .
```

### 4. Access Application
- **Docker**: Frontend http://localhost:3000, Backend http://localhost:8000
- **Kubernetes**: Frontend http://node-ip:30300, Backend http://node-ip:30800

## 🔧 Features

### Frontend (Next.js + TypeScript)
- **Modern UI**: Clean, responsive design with Tailwind CSS
- **Real-time Analysis**: Live research results display
- **PDF Export**: Download analysis reports
- **Interactive Mode**: Follow-up questions and conversations
- **Markdown Rendering**: Properly formatted analysis results

### Backend (Python + Flask)
- **Multi-Agent System**: Specialized agents for different query types
- **SERP API Integration**: Enhanced search capabilities
- **YouTube Analysis**: Video transcript extraction and analysis
- **E-commerce Scraping**: Product data from Amazon, Flipkart, etc.
- **AWS Bedrock LLM**: Advanced AI analysis and insights
- **Memory Management**: Conversational context retention

## 🤖 AI Agents

1. **Product Agent**: Product reviews, specifications, market analysis
2. **News Agent**: Real-time news analysis and stock market insights
3. **General Agent**: Comprehensive research and analysis
4. **Validator Agent**: Information validation and fact-checking

## 🔌 API Integration

- **SERP API**: Google, YouTube, Shopping, News search
- **NewsData.io**: Real-time news articles
- **Tavily AI**: Advanced AI-powered search
- **AWS Bedrock**: LLM analysis and insights
- **YouTube Transcript API**: Video content extraction

## 📊 Data Sources

- **Web Scraping**: Real content from SERP API results
- **YouTube Reviews**: Video transcripts and analysis
- **E-commerce Data**: Product pricing and reviews
- **News Articles**: Real-time news and market data
- **Stock Data**: Financial metrics and analysis

## 🛠️ Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python server.py
```

### Frontend Development
```bash
cd frontend-nextjs
npm install
npm run dev
```

## 📝 Configuration

### Required API Keys
- **SERP API**: https://serpapi.com/ (100 searches/month free)
- **NewsData.io**: https://newsdata.io/ (200 requests/day free)
- **AWS Bedrock**: AWS account with Bedrock access
- **Tavily AI**: https://tavily.com/ (1000 searches/month free)

### Optional API Keys
- **Google Custom Search**: For fallback search
- **YouTube Data API**: For enhanced video search

## 🚀 Deployment

### Docker (Recommended)
```bash
# Build and run
./build.sh
docker-compose up -d
```

### Kubernetes
```bash
# Deploy to cluster
cd k8s
kubectl apply -f .

# Access via NodePort
# Frontend: http://node-ip:30300
# Backend: http://node-ip:30800
```

### Manual Development
```bash
# Backend
cd backend && python server.py

# Frontend
cd frontend-nextjs && npm run dev
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📈 Usage Examples

- **Product Research**: "iPhone 15 Pro review analysis"
- **Stock Analysis**: "Tesla stock analysis and news"
- **Market Research**: "Electric vehicle market trends"
- **News Analysis**: "Latest AI developments"

## 🔄 System Flow

1. **Query Input**: User enters research query
2. **Agent Selection**: Orchestrator selects appropriate agent
3. **Data Collection**: SERP API, YouTube, E-commerce scraping
4. **AI Analysis**: AWS Bedrock LLM processes data
5. **Result Display**: Formatted analysis with sources
6. **Interactive Mode**: Follow-up questions and conversations

## 🛡️ Error Handling

- **Graceful Degradation**: Works with any combination of API keys
- **Fallback Systems**: Multiple backup data sources
- **Retry Logic**: Automatic retry for failed requests
- **User Feedback**: Clear error messages and status updates