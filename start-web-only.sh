#!/bin/bash

echo "🌐 Starting AI Research Orchestrator - Web Interface Only"
echo "========================================================"

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
echo "🌐 Starting Web Interface..."
echo "========================================================"

# Start frontend only
cd frontend
python app.py

echo ""
echo "👋 Web interface stopped."