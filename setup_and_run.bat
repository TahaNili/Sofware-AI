@echo off
setlocal enabledelayedexpansion

:: Parse command line arguments
set WITH_BROWSER=0
for %%a in (%*) do (
    if "%%a"=="--with-browser" set WITH_BROWSER=1
)

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

::: Check for .env file and copy from .env.example if needed
if not exist .env (
    echo ⚠️ .env file not found. Creating from .env.example...
    copy .env.example .env
) else (
    :: Check if .env is empty
    for %%I in (.env) do if %%~zI==0 (
        echo ⚠️ .env file is empty. Copying contents from .env.example...
        copy .env.example .env
    )
)

:: Run the application
echo 🚀 Starting the modern GUI application...
python main.py

:: Setup browser-use environment if requested
if !WITH_BROWSER!==1 (
    echo 🌐 Setting up browser-use environment...
    if exist .venv-browser (
        echo Found existing .venv-browser, removing it...
        rmdir /s /q .venv-browser
    )
    python -m venv .venv-browser
    call .venv-browser\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements-browser.txt
    echo ✨ browser-use environment is ready
    :: Return to main venv
    call venv\Scripts\activate.bat
)

echo ✨ Done! Check the output above for any errors.
if !WITH_BROWSER!==1 (
    echo 🔍 Browser automation is available in .venv-browser
)
pause