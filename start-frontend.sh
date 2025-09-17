#!/bin/bash
pkill -f "npm.*dev" 2>/dev/null
cd frontend-nextjs
npm run dev