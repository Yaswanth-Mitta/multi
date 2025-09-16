#!/bin/bash

echo "🚀 EC2 Setup for AI Research Agent"
echo "=================================="

# Get EC2 public IP automatically
export EC2_PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null)

if [ -z "$EC2_PUBLIC_IP" ]; then
    echo "❌ Could not detect EC2 public IP. Please set manually:"
    echo "export EC2_PUBLIC_IP=your-actual-ip"
    exit 1
fi

echo "✅ Detected EC2 Public IP: $EC2_PUBLIC_IP"

# Check if port 8000 is available
if netstat -tuln | grep -q ":8000 "; then
    echo "⚠️  Port 8000 is in use. Killing existing processes..."
    sudo pkill -f "python.*app.py" 2>/dev/null || true
    sudo fuser -k 8000/tcp 2>/dev/null || true
    sleep 2
fi

# Start the application
echo ""
echo "🚀 Starting AI Research Agent..."
echo "Frontend + Backend: http://$EC2_PUBLIC_IP:8000"
echo ""

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  No virtual environment found. Using system Python."
fi

# Install requirements
pip install -r requirements.txt >/dev/null 2>&1
pip install -r frontend/requirements.txt >/dev/null 2>&1

# Start the web application
cd frontend
echo "🌐 Server starting on http://0.0.0.0:8000"
echo "🌍 Access from browser: http://$EC2_PUBLIC_IP:8000"
echo ""
echo "Press Ctrl+C to stop"
echo "=================================="

python app.py