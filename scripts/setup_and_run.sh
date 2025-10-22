#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting setup and installation process..."

# Check Python installation
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.13+ first."
    exit 1
fi

# Print Python version
echo "📌 Using Python version:"
python --version

# Create and activate virtual environment
echo "🔧 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Found existing venv, removing it..."
    rm -rf venv
fi

python -m venv venv

# Activate virtual environment in Git Bash
source venv/Scripts/activate

# Upgrade pip
echo "🔄 Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check for .env file and copy from .env.example if needed
if [ ! -f ".env" ]; then
    echo "⚠️ .env file not found. Creating from .env.example..."
    cp .env.example .env
else
    # Check if .env is empty
    if [ ! -s ".env" ]; then
        echo "⚠️ .env file is empty. Copying contents from .env.example..."
        cp .env.example .env
    fi
fi

# Run the application
echo "🚀 Starting the modern GUI application..."
python main.py

echo "✨ Done! Check the output above for any errors."