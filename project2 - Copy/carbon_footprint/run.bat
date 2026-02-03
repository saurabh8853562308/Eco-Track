@echo off
REM Carbon Footprint Calculator Setup Script for Windows
REM This script sets up and runs the Django application

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║     CARBON FOOTPRINT CALCULATOR - SETUP & RUN SCRIPT          ║
echo ║              For Ghaziabad Climate Awareness                  ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo ✓ Python is installed
python --version

REM Navigate to project directory
cd /d "%~dp0"
echo.
echo Current directory: %CD%

REM Check if manage.py exists
if not exist "manage.py" (
    echo ❌ ERROR: manage.py not found. Make sure you're in the correct directory.
    pause
    exit /b 1
)

echo ✓ Project structure verified

REM Install dependencies
echo.
echo 📦 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

REM Run migrations
echo.
echo 🗄️  Running database migrations...
python manage.py migrate
if errorlevel 1 (
    echo ❌ ERROR: Failed to run migrations
    pause
    exit /b 1
)
echo ✓ Database migrations completed

REM Collect static files
echo.
echo 📁 Collecting static files...
python manage.py collectstatic --noinput
if errorlevel 1 (
    echo ⚠️  WARNING: Failed to collect static files (may be okay)
)

REM Start the development server
echo.
echo 🚀 Starting Django development server...
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  Your Carbon Footprint Calculator is starting!               ║
echo ║  Open your browser and go to: http://127.0.0.1:8000          ║
echo ║                                                                ║
echo ║  To stop the server, press: CTRL + BREAK (or CTRL + C)       ║
echo ║                                                                ║
echo ║  Admin Panel: http://127.0.0.1:8000/admin                    ║
echo ║  API Endpoint: http://127.0.0.1:8000/api/calculate/          ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

python manage.py runserver

pause
