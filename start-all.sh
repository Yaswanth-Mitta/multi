#!/bin/bash

echo "🚀 Starting AI Research Orchestrator - Full Stack"
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
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "✅ Backend stopped"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "✅ Frontend stopped"
    fi
    echo "👋 Goodbye!"
    exit 0
}

# Set trap to cleanup on exit
trap cleanup SIGINT SIGTERM

# Start backend in background
echo ""
echo "🔄 Starting Backend (Console Mode)..."
python main.py &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"

# Wait a moment for backend to initialize
sleep 2

# Start frontend in background
echo ""
echo "🌐 Starting Frontend (Web Interface)..."
cd frontend
python app.py &
FRONTEND_PID=$!
cd ..
echo "✅ Frontend started (PID: $FRONTEND_PID)"

echo ""
echo "🎉 All services are running!"
echo "=================================================="
echo "🖥️  Console Interface: Check terminal above"
echo "🌐 Web Interface: http://localhost:8000"
echo "📱 Mobile friendly UI available"
echo ""
echo "💡 Usage:"
echo "   • Use console for direct CLI interaction"
echo "   • Use web browser for modern UI experience"
echo "   • Both interfaces share the same backend"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=================================================="

# Wait for user to stop services
wait