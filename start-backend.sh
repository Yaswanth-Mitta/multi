#!/bin/bash
pkill -f "python.*main.py" 2>/dev/null
source .env
python main.py