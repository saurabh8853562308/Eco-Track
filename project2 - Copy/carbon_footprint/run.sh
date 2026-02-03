#!/bin/bash
# Carbon Footprint Calculator Setup Script for Linux/Mac
# This script sets up and runs the Django application

clear

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     CARBON FOOTPRINT CALCULATOR - SETUP & RUN SCRIPT          ║"
echo "║              For Ghaziabad Climate Awareness                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

echo "✓ Python is installed"
python3 --version

# Navigate to script directory
cd "$(dirname "$0")"
echo ""
echo "Current directory: $(pwd)"

# Check if manage.py exists
if [ ! -f "manage.py" ]; then
    echo "❌ ERROR: manage.py not found. Make sure you're in the correct directory."
    exit 1
fi

echo "✓ Project structure verified"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"

# Run migrations
echo ""
echo "🗄️  Running database migrations..."
python3 manage.py migrate
if [ $? -ne 0 ]; then
    echo "❌ ERROR: Failed to run migrations"
    exit 1
fi
echo "✓ Database migrations completed"

# Collect static files
echo ""
echo "📁 Collecting static files..."
python3 manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo "⚠️  WARNING: Failed to collect static files (may be okay)"
fi

# Start the development server
echo ""
echo "🚀 Starting Django development server..."
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Your Carbon Footprint Calculator is starting!               ║"
echo "║  Open your browser and go to: http://127.0.0.1:8000          ║"
echo "║                                                                ║"
echo "║  To stop the server, press: CTRL + C                          ║"
echo "║                                                                ║"
echo "║  Admin Panel: http://127.0.0.1:8000/admin                    ║"
echo "║  API Endpoint: http://127.0.0.1:8000/api/calculate/          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

python3 manage.py runserver
