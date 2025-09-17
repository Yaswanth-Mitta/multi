#!/bin/bash

echo "🚀 Starting AI Research Agent (Manual Mode)"
echo "==========================================="

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

# Start backend in background
echo "📦 Starting backend..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    if command -v python3 &> /dev/null; then
        python3 -m venv venv
    else
        python -m venv venv
    fi
fi

# Activate virtual environment and start backend
source venv/bin/activate
pip install -r requirements.txt

# Test imports before starting server
echo "🧪 Testing imports..."
if command -v python3 &> /dev/null; then
    python3 test_imports.py
else
    python test_imports.py
fi

if [ $? -eq 0 ]; then
    echo "🚀 Starting backend server..."
    if command -v python3 &> /dev/null; then
        python3 server.py &
    else
        python server.py &
    fi
else
    echo "❌ Import test failed. Please check dependencies."
    exit 1
fi
BACKEND_PID=$!

cd ..

# Start frontend
echo "🌐 Starting frontend..."
cd frontend-nextjs
npm install
npm run dev &
FRONTEND_PID=$!

cd ..

# Get PUBLIC_IP from .env
PUBLIC_IP=$(grep PUBLIC_IP .env | cut -d '=' -f2)
if [ -z "$PUBLIC_IP" ]; then
    PUBLIC_IP="localhost"
fi

echo "✅ Services started!"
echo "📋 Access URLs:"
echo "Frontend: http://$PUBLIC_IP:3000"
echo "Backend:  http://$PUBLIC_IP:8000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait