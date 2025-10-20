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

:: Install dependencies one by one to ensure proper installation
echo 📦 Installing dependencies...
pip install openai==2.5.0
pip install python-dotenv==1.1.1
pip install PySide6==6.10.0
pip install darkdetect==0.8.0
pip install pywin32==311
pip install psutil==7.1.1
pip install pandas==2.1.1
pip install numpy==1.26.0
pip install aiohttp==3.9.1
pip install tqdm==4.66.1
pip install colorama==0.4.6

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