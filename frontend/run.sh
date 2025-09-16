#!/bin/bash

echo "Starting Research Agent Web Interface..."
echo

# Check if virtual environment exists
if [ ! -d "../venv" ]; then
    echo "Virtual environment not found. Please run setup first."
    echo "Run: ../setup.sh"
    exit 1
fi

# Activate virtual environment
source ../venv/bin/activate

# Install frontend dependencies
echo "Installing frontend dependencies..."
pip install -r requirements.txt

# Start the web server
echo
echo "Starting web server on http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo
python app.py