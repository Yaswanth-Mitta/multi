@echo off
echo Setting up Multi-Agent LLM System...

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt

REM Copy environment template
copy .env.example .env

echo.
echo Setup complete! 
echo.
echo Next steps:
echo 1. Edit .env file with your API keys
echo 2. Run: venv\Scripts\activate.bat
echo 3. Run: python main.py
echo.
pause