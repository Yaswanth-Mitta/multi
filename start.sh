#!/bin/bash
pkill -f "python.*main.py" 2>/dev/null
pkill -f "npm.*dev" 2>/dev/null
cd "$(dirname "$0")"
python main.py &
sleep 2
cd frontend-nextjs && npm run dev &
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
wait