#!/bin/bash

echo "🖥️ Starting AI Research Orchestrator - Console Interface"
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

echo ""
echo "🖥️ Starting Console Interface..."
echo "========================================================"

# Start console interface
python main.py

echo ""
echo "👋 Console interface stopped."