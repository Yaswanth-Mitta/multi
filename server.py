#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from agent.research_agent.orchestrator import AIOrchestrator
from agent.research_agent.config import Config
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize orchestrator
orchestrator = None

def init_orchestrator():
    global orchestrator
    try:
        orchestrator = AIOrchestrator(
            newsdata_api_key=Config.get_newsdata_api_key(),
            google_cse_id=Config.get_google_cse_id(),
            serp_api_key=Config.get_serp_api_key(),
            aws_access_key=Config.get_aws_access_key(),
            aws_secret_key=Config.get_aws_secret_key(),
            aws_region=Config.get_aws_region()
        )
        print("✅ AI Orchestrator initialized successfully!")
    except Exception as e:
        print(f"Error initializing AI Orchestrator: {e}")

@app.route('/research', methods=['POST'])
def research():
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        if not orchestrator:
            return jsonify({'error': 'Orchestrator not initialized'}), 500
        
        # Process the query
        result = orchestrator.analyze_query(query)
        
        # Format response for frontend
        response = {
            'query': query,
            'marketAnalysis': {
                'summary': result,
                'trends': [],
                'competition': '',
                'marketSize': ''
            },
            'sources': [
                {'title': 'AI Research Analysis', 'url': '#', 'type': 'AI Analysis'},
                {'title': 'Web Research Data', 'url': '#', 'type': 'Web Scraping'},
                {'title': 'Market Intelligence', 'url': '#', 'type': 'Market Data'}
            ]
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def health():
    return jsonify({'status': 'Research Agent API is running'})

if __name__ == '__main__':
    print("🚀 Starting AI Research Agent")
    print("=" * 29)
    
    # Get public IP from environment
    public_ip = os.getenv('PUBLIC_IP', '0.0.0.0')
    print(f"🌐 Public IP: {public_ip}")
    print("🚀 Starting on port 8000...")
    print(f"🌐 Access: http://{public_ip}:8000")
    print("=" * 29)
    
    # Initialize orchestrator
    init_orchestrator()
    
    # Start Flask server
    app.run(host='0.0.0.0', port=8000, debug=False)