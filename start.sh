#!/bin/bash
pkill -f "python.*main.py" 2>/dev/null
pkill -f "npm.*dev" 2>/dev/null
cd "$(dirname "$0")"
./setup-env.sh
source .env
python main.py &
sleep 2
cd frontend-nextjs && npm run dev &
echo "Backend: http://${PUBLIC_IP}:8000"
echo "Frontend: http://${PUBLIC_IP}:3000"
wait