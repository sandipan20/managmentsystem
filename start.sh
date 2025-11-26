#!/bin/bash
# Quick Start Script for Hostel Manager
# This script sets up and runs the Hostel Manager application

set -e  # Exit on any error

echo "🏨 Hostel Manager - Quick Start"
echo "================================"
echo ""

# Check if Python is installed
echo "✓ Checking Python installation..."
python3 --version

# Check if we're in the right directory
if [ ! -f "run.py" ]; then
    echo "❌ Error: run.py not found!"
    echo "Please navigate to the hostelmanagment directory first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "✓ Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo ""
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Default PORT (can be overridden by environment variable)
PORT=${PORT:-5000}
export PORT

# Install dependencies
echo ""
echo "✓ Installing dependencies..."
pip install -r requirements.txt > /dev/null

echo ""
echo "================================"
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting Hostel Manager..."
echo ""
echo "📍 Open your browser and go to: http://localhost:${PORT}"
echo "⚠️  Press Ctrl+C to stop the server"
echo ""
echo "================================"
echo ""

# Run the application (uses HOST/PORT env vars if set)
python3 run.py
