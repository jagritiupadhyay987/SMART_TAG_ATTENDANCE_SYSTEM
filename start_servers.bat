@echo off
echo Starting Attendance System Servers...

echo.
echo Starting Backend Server (Port 8000)...
start "Backend Server" cmd /k "cd /d \"c:\project\attandance management system\backend\" && \"c:\project\attandance management system\backend\.venv\Scripts\python.exe\" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

ping -n 4 127.0.0.1 > nul

echo.
echo Starting Frontend Server (Port 3000)...
start "Frontend Server" cmd /k "cd /d \"c:\project\attandance management system\attendance management-portal\" && npm run dev"

echo.
echo Both servers are starting...
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:3000
echo.
echo Press any key to close this window...
pause > nul