@echo off

echo 🚀 Starting AI Research Agent (Manual Mode)
echo ===========================================

REM Check if .env exists
if not exist ".env" (
    echo ❌ .env file not found. Please copy .env.example to .env and configure it.
    pause
    exit /b 1
)

REM Start backend
echo 📦 Starting backend...
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install dependencies
call venv\Scripts\activate.bat
pip install -r requirements.txt

REM Start backend in new window
start "Backend Server" cmd /k "venv\Scripts\activate.bat && python server.py"

cd ..

REM Start frontend
echo 🌐 Starting frontend...
cd frontend-nextjs
call npm install

REM Start frontend in new window
start "Frontend Server" cmd /k "npm run dev"

cd ..

echo ✅ Services started!
echo 📋 Access URLs:
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo.
echo Both services are running in separate windows.
echo Close the windows to stop the services.

pause