@echo off
REM Setup script for CineStream Pro - Windows

echo.
echo ========================================
echo CineStream Pro - Setup Script
echo ========================================
echo.

REM Backend Setup
echo [1/5] Setting up Python Backend...
cd backend

REM Create virtual environment
if not exist venv (
  echo Creating virtual environment...
  python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Deactivate virtual environment
deactivate

REM Frontend Setup
echo.
echo [2/5] Setting up React Frontend...
cd ..\frontend

REM Install npm dependencies
echo Installing npm dependencies...
call npm install

REM Return to root
cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo.
echo 1. Backend (Terminal 1):
echo    cd backend
echo    venv\Scripts\activate
echo    python app.py
echo.
echo 2. Frontend (Terminal 2):
echo    cd frontend
echo    npm start
echo.
echo Backend will run on: http://localhost:5000
echo Frontend will run on: http://localhost:3000
echo.
echo ========================================
echo.

pause
