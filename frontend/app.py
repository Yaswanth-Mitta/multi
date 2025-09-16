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
except ImportError as e:
    print(f"Research agent not available: {e}")
    AGENT_AVAILABLE = False

app = Flask(__name__)
CORS(app)

# Global orchestrator instance
orchestrator = None

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
            print("❌ Orchestrator not initialized")
            return jsonify({'error': 'Orchestrator not initialized'}), 500
        
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
    if initialize_orchestrator():
        print("✅ Backend services ready")
    else:
        print("⚠️  Running in limited mode (some features may not work)")
    
    print("\n🌐 Web Interface: http://localhost:8000")
    print("📱 Mobile friendly interface available")
    print("🔄 Auto-refresh for real-time updates")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=8000, debug=True)