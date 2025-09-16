#!/bin/bash

echo "🚀 Quick Start - AI Research Agent"
echo "================================="

# Get public IP manually or use a simple method
PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s ipinfo.io/ip 2>/dev/null || echo "localhost")
echo "🌐 Public IP: $PUBLIC_IP"

# Install net-tools if needed
if ! command -v netstat &> /dev/null; then
    echo "📦 Installing net-tools..."
    sudo apt-get update -qq && sudo apt-get install -y net-tools
fi

# Kill any existing process on port 8000
sudo pkill -f "python.*app.py" 2>/dev/null || true
sudo fuser -k 8000/tcp 2>/dev/null || true

# Start the application
echo ""
echo "🚀 Starting application..."
echo "🌐 Access: http://$PUBLIC_IP:8000"
echo "🏠 Local: http://localhost:8000"
echo ""

cd frontend
python app.py