#!/bin/bash

echo "🚀 Starting AI Research Agent"
echo "============================="

# Use your EC2 IP
PUBLIC_IP="34.224.101.80"
echo "🌐 Public IP: $PUBLIC_IP"

# Kill existing processes
pkill -f "python.*app.py" 2>/dev/null || true

# Start application
echo "🚀 Starting on port 8000..."
echo "🌐 Access: http://$PUBLIC_IP:8000"
echo "============================="

cd frontend
python app.py