#!/bin/bash

echo "🚀 Starting AI Research Orchestrator - Web Interface"
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    echo "Run: ./setup.sh"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install all dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
pip install -r frontend/requirements.txt

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "✅ Web interface stopped"
    fi
    echo "👋 Goodbye!"
    exit 0
}

# Set trap to cleanup on exit
trap cleanup SIGINT SIGTERM

# Start only the web frontend (it includes the backend functionality)
echo ""
echo "🌐 Starting Web Interface with Backend Integration..."
cd frontend
python app.py &
FRONTEND_PID=$!
cd ..
echo "✅ Web interface started (PID: $FRONTEND_PID)"
echo "    Backend functionality integrated into web server"

echo ""
echo "🎉 All services are running!"
echo "=================================================="
EC2_IP=${EC2_PUBLIC_IP:-"your-ec2-ip"}
echo "🌐 Web Interface Access:"
echo "   • Local: http://localhost:8000"
echo "   • EC2 Public: http://$EC2_IP:8000"
echo "📱 Mobile friendly UI available"
echo "🤖 Full AI agent functionality available"
echo ""
echo "💡 Usage:"
echo "   • Open the web interface in your browser"
echo "   • Use the modern web interface for all features"
echo "   • All agents and memory features included"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=================================================="

# Wait for user to stop services
wait