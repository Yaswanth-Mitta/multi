from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os
from datetime import datetime

# Add parent directory to path to import research agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from agent.research_agent.orchestrator import AIOrchestrator
    from agent.research_agent.config import Config
    AGENT_AVAILABLE = True
    print("✅ Research agent modules imported successfully")
except ImportError as e:
    print(f"❌ Research agent not available: {e}")
    AGENT_AVAILABLE = False

app = Flask(__name__)
CORS(app)

# Global orchestrator instance
orchestrator = None

def generate_demo_response(query):
    """Generate demo response when orchestrator is not available"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['stock', 'tesla', 'nvidia', 'apple']):
        agent_type = 'NEWS'
        result = f"""
╭──────────────────────────────────────────────────────────────────────────────╮
│                     DEMO MODE - STOCK ANALYSIS                            │
╰──────────────────────────────────────────────────────────────────────────────╯

📋 QUERY: {query}

📈 DEMO STOCK ANALYSIS:
This is a demonstration of the stock analysis feature. In full mode, this would show:
• Real-time stock prices from Yahoo Finance
• Market trends and technical analysis
• Investment recommendations
• Risk assessment and price targets

⚠️  To enable full functionality, configure your environment variables and restart the backend.
"""
    elif any(word in query_lower for word in ['pixel', 'iphone', 'samsung', 'review', 'phone']):
        agent_type = 'PRODUCT'
        result = f"""
╭──────────────────────────────────────────────────────────────────────────────╮
│                     DEMO MODE - PRODUCT ANALYSIS                          │
╰──────────────────────────────────────────────────────────────────────────────╯

📋 QUERY: {query}

📈 DEMO PRODUCT ANALYSIS:
This is a demonstration of the product analysis feature. In full mode, this would show:
• Comprehensive web scraping from review sites
• YouTube video analysis (10+ reviews)
• Real-time pricing and availability
• Detailed pros/cons from multiple sources
• Purchase recommendations and alternatives

💬 CONVERSATIONAL MODE:
In full mode, you could ask follow-up questions like:
• "What about the camera quality?"
• "How's the battery life?"
• "What colors are available?"

⚠️  To enable full functionality, configure your environment variables and restart the backend.
"""
    else:
        agent_type = 'GENERAL'
        result = f"""
╭──────────────────────────────────────────────────────────────────────────────╮
│                     DEMO MODE - GENERAL ANALYSIS                          │
╰──────────────────────────────────────────────────────────────────────────────╯

📋 QUERY: {query}

📈 DEMO GENERAL ANALYSIS:
This is a demonstration of the general analysis feature. In full mode, this would provide:
• Comprehensive research and analysis
• Multi-source data aggregation
• AI-powered insights and recommendations
• Contextual information and trends

⚠️  To enable full functionality, configure your environment variables and restart the backend.
"""
    
    return {
        'result': result,
        'agent': agent_type,
        'timestamp': datetime.now().isoformat(),
        'session': None,
        'query': query,
        'demo_mode': True
    }

def initialize_orchestrator():
    """Initialize the AI orchestrator"""
    global orchestrator
    
    print(f"🔄 Initializing orchestrator...")
    print(f"📝 Agent available: {AGENT_AVAILABLE}")
    
    if not AGENT_AVAILABLE:
        print("❌ Agent not available")
        return False
    
    try:
        print("🔍 Validating configuration...")
        if not Config.validate_config():
            print("❌ Configuration validation failed")
            return False
        
        print("🏭 Creating orchestrator instance...")
        orchestrator = AIOrchestrator(
            newsdata_api_key=Config.get_newsdata_api_key(),
            google_cse_id=Config.get_google_cse_id(),
            aws_access_key=Config.get_aws_access_key(),
            aws_secret_key=Config.get_aws_secret_key(),
            aws_region=Config.get_aws_region()
        )
        print("✅ AI Orchestrator initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize orchestrator: {e}")
        import traceback
        traceback.print_exc()
        return False

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

@app.route('/status', methods=['GET'])
def get_status():
    """Get system status"""
    if not orchestrator:
        return jsonify({
            'aws': False,
            'google': False,
            'news': False,
            'message': 'Orchestrator not initialized'
        })
    
    try:
        # Check if services are available
        aws_status = True  # Assume AWS is available if orchestrator initialized
        google_status = bool(Config.get_google_cse_id())
        news_status = False  # News service is disabled
        
        return jsonify({
            'aws': aws_status,
            'google': google_status,
            'news': news_status,
            'message': 'System operational'
        })
    except Exception as e:
        return jsonify({
            'aws': False,
            'google': False,
            'news': False,
            'message': f'Status check failed: {str(e)}'
        }), 500

@app.route('/analyze', methods=['POST'])
def analyze_query():
    """Analyze user query"""
    try:
        print(f"📥 Received analyze request")
        data = request.get_json()
        query = data.get('query', '').strip()
        print(f"📝 Query: {query}")
        
        if not query:
            print("❌ Empty query received")
            return jsonify({'error': 'Query is required'}), 400
        
        if not orchestrator:
            print("⚠️  Orchestrator not initialized, using demo mode")
            # Generate demo response
            demo_result = generate_demo_response(query)
            return jsonify(demo_result)
        
        print(f"🔄 Processing query with orchestrator...")
        # Process the query
        result = orchestrator.analyze_query(query)
        print(f"✅ Got result, length: {len(result)}")
        
        # Get memory status
        memory_status = orchestrator.get_memory_status()
        session_info = None
        
        if "Active session" in memory_status:
            session_info = {
                'active': True,
                'product': memory_status.split(': ')[1].split(' (')[0]
            }
        
        # Determine agent type based on result content
        agent_type = 'GENERAL'
        if 'PRODUCT MARKET ANALYSIS' in result:
            agent_type = 'PRODUCT'
        elif 'STOCK ANALYSIS' in result:
            agent_type = 'NEWS'
        elif 'GENERAL ANALYSIS' in result:
            agent_type = 'GENERAL'
        
        response_data = {
            'result': result,
            'agent': agent_type,
            'timestamp': datetime.now().isoformat(),
            'session': session_info,
            'query': query
        }
        print(f"📤 Sending response: agent={agent_type}, session={session_info}")
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Error processing query: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/clear-memory', methods=['POST'])
def clear_memory():
    """Clear conversation memory"""
    try:
        if orchestrator:
            orchestrator.clear_memory()
            return jsonify({'message': 'Memory cleared successfully'})
        else:
            return jsonify({'message': 'Orchestrator not available'})
    except Exception as e:
        return jsonify({'error': f'Failed to clear memory: {str(e)}'}), 500

@app.route('/memory-status', methods=['GET'])
def get_memory_status():
    """Get current memory status"""
    try:
        if orchestrator:
            status = orchestrator.get_memory_status()
            return jsonify({'status': status})
        else:
            return jsonify({'status': 'No active session'})
    except Exception as e:
        return jsonify({'error': f'Failed to get memory status: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Starting Research Agent Web Interface...")
    print("=" * 50)
    
    # Initialize orchestrator
    orchestrator_ready = initialize_orchestrator()
    if orchestrator_ready:
        print("✅ Backend services ready - Full functionality available")
    else:
        print("⚠️  Running in demo mode - Limited functionality")
        print("    • Mock responses will be generated")
        print("    • No real API calls will be made")
    
    ec2_ip = os.getenv('EC2_PUBLIC_IP', 'your-ec2-ip')
    print("\n🌐 Will try ports: 8000, 8001, 8002, 8003, 8080")
    print(f"🌍 EC2 Public IP: http://{ec2_ip}:PORT")
    print("🏠 Local access: http://localhost:PORT")
    print("📱 Mobile friendly interface available")
    print("🔄 Auto-refresh for real-time updates")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    # Try different ports if 8000 is in use
    ports_to_try = [8000, 8001, 8002, 8003, 8080]
    
    for port in ports_to_try:
        try:
            print(f"🔄 Trying to start server on port {port}...")
            ec2_ip = os.getenv('EC2_PUBLIC_IP', 'your-ec2-ip')
            print(f"🌐 Backend API will be available at: http://0.0.0.0:{port}")
            print(f"🌐 Local access: http://localhost:{port}")
            print(f"🌐 EC2 access: http://{ec2_ip}:{port}")
            print("=" * 50)
            app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
            break
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"⚠️  Port {port} is in use, trying next port...")
                continue
            else:
                print(f"❌ Failed to start server on port {port}: {e}")
                break
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            break
    else:
        print("❌ All ports are in use. Please kill existing processes or use different ports.")
        print("Run: ./kill-port.sh to free up port 8000")