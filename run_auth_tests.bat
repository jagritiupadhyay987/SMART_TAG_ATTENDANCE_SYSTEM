@echo off
set BASE=http://localhost:8000

echo Checking backend health...
curl -s %BASE%/health || (
  echo Backend not reachable at %BASE% & exit /b 1
)

echo Seeding data...
curl -s -X POST %BASE%/seed_data > nul

echo Running Python tests...
python "%~dp0test_authentication_flow.py"

start "" "%~dp0test_frontend_auth.html"