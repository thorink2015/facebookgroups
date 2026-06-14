@echo off
REM Tank Mix Campaign Dashboard - one-command start (Windows)
cd /d %~dp0

if not exist venv (
  echo First run: setting up (this takes a minute)...
  python -m venv venv
  venv\Scripts\python -m pip install -q --upgrade pip
  venv\Scripts\pip install -q -r requirements.txt
)

venv\Scripts\python seed.py
echo.
echo   Dashboard is starting.
echo   Open this in your browser:  http://127.0.0.1:5000
echo   Press Ctrl+C in this window to stop.
echo.
venv\Scripts\python app.py
