@echo off
echo 🚀 Starting setup and installation process...

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.13+ first.
    exit /b 1
)

:: Print Python version
echo 📌 Using Python version:
python --version

:: Create and activate virtual environment
echo 🔧 Creating virtual environment...
if exist venv (
    echo Found existing venv, removing it...
    rmdir /s /q venv
)

python -m venv venv
call venv\Scripts\activate.bat

:: Upgrade pip
echo 🔄 Upgrading pip...
python -m pip install --upgrade pip

:: Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

:: Check for .env file
if not exist .env (
    echo ⚠️ Creating .env file...
    echo OPENAI_API_KEY= > .env
    echo ⚠️ Please edit .env and add your OpenAI API key
)

:: Run the application
echo 🚀 Starting the application...
python -m agent.main

echo ✨ Done! Check the output above for any errors.
pause