@echo off
echo Starting Attendance Management System Backend...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found in PATH. Trying to use local Python installer...
    if exist "python-3.11.6-amd64.exe" (
        echo Please install Python first by running: python-3.11.6-amd64.exe
        echo After installation, restart this script.
        pause
        exit /b 1
    ) else (
        echo Python installer not found. Please install Python 3.11+ and add it to PATH.
        pause
        exit /b 1
    )
)

cd backend

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if MongoDB is running
echo Checking MongoDB connection...
python -c "import pymongo; client = pymongo.MongoClient('mongodb://localhost:27017/'); client.admin.command('ping'); print('MongoDB is running!')" 2>nul
if %errorlevel% neq 0 (
    echo Warning: MongoDB might not be running. Please start MongoDB first.
    echo You can download MongoDB from: https://www.mongodb.com/try/download/community
    echo Or use MongoDB Atlas for cloud database.
)

REM Start the server
echo Starting FastAPI server...
echo Backend will be available at: http://localhost:8080
echo API documentation at: http://localhost:8080/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python run.py

pause
