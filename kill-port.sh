#!/bin/bash

echo "🔍 Checking for processes on port 8000..."

# Find process using port 8000
PID=$(lsof -ti:8000 2>/dev/null)

if [ -n "$PID" ]; then
    echo "📍 Found process $PID using port 8000"
    echo "🔫 Killing process..."
    kill -9 $PID
    sleep 1
    echo "✅ Process killed"
else
    echo "✅ Port 8000 is free"
fi

echo "🚀 Port 8000 is now available"