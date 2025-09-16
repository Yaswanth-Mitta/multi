#!/bin/bash

echo "🔧 Starting Backend API Server Only"
echo "=================================="

# Kill any existing process on port 8000
./kill-port.sh

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    echo "Run: ./setup.sh"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
pip install -r frontend/requirements.txt

echo ""
EC2_IP=${EC2_PUBLIC_IP:-"your-ec2-ip"}
echo "🚀 Starting Backend API Server..."
echo "Local: http://localhost:8000"
echo "EC2 Public: http://$EC2_IP:8000"
echo "=================================="

# Start backend API server
cd frontend
python app.py