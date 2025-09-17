@echo off

echo 🚀 Starting AI Research Agent Backend
echo ====================================

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Start the server
echo 🌐 Starting Flask server...
python server.py

pause