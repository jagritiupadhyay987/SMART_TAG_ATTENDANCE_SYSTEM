@echo off
echo Seeding Attendance Management System Database...
echo.

cd backend

REM Check if virtual environment exists
if not exist ".venv" (
    echo Virtual environment not found. Please run start_backend.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Seed the database
echo Seeding database with sample data...
python -c "
import requests
import json

try:
    response = requests.post('http://localhost:8080/seed_data')
    if response.status_code == 200:
        print('Database seeded successfully!')
        print('Sample users created:')
        print('- student@demo.com / password123')
        print('- hod@demo.com / password123')
    else:
        print('Error seeding database:', response.text)
except requests.exceptions.ConnectionError:
    print('Cannot connect to backend server. Please make sure the backend is running.')
    print('Run start_backend.bat first.')
except Exception as e:
    print('Error:', str(e))
"

pause
