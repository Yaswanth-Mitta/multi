#!/bin/bash
pkill -f "python.*server.py" 2>/dev/null
source .env
python server.py