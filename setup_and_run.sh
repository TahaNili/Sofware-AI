#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting setup and installation process..."

# Check Python installation
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.7+ first."
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

# Install Playwright browser
echo "🌐 Installing Chromium for Playwright..."
python -m playwright install chromium

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️ Creating .env file..."
    echo "OPENAI_API_KEY=" > .env
    echo "⚠️ Please edit .env and add your OpenAI API key"
fi

# Run the application
echo "🚀 Starting the application..."
python -m agent.main

echo "✨ Done! Check the output above for any errors."