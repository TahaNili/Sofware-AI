"""
Main entry point for the AI-powered software assistant application.
Initializes the GUI and backend components and starts the application.
"""

import sys
import os
import asyncio
from PySide6.QtWidgets import QApplication
from dotenv import load_dotenv

from ui.main_window import MainWindow
from agent.ai.factory import AIFactory
from agent.cli import main as cli_main
from utils.logger import logger

def check_environment():
    """Check if environment variables are properly loaded"""
    # Try to load .env from the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(current_dir, '.env')
    
    logger.info(f"Checking .env file at: {env_path}")
    if os.path.exists(env_path):
        try:
            # Check if file is readable
            with open(env_path, 'r', encoding='utf-8') as f:
                content = f.read()
                logger.info(f".env file found and readable, size: {len(content)} bytes")
                if "GOOGLE_API_KEY" not in content and "OPENAI_API_KEY" not in content:
                    logger.warning("Warning: .env file exists but does not contain API key definitions")
        except Exception as e:
            logger.error(f"Error reading .env file: {str(e)}")
        
        # Try to load the environment variables
        load_dotenv(env_path)
    else:
        logger.warning(f"No .env file found at {env_path}")
        # Try parent directory as fallback
        parent_env = os.path.join(os.path.dirname(current_dir), '.env')
        if os.path.exists(parent_env):
            logger.info(f"Found .env in parent directory: {parent_env}")
            load_dotenv(parent_env)
    
    # Check environment variables
    google_key = os.getenv('GOOGLE_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    logger.info("----- Environment Check -----")
    logger.info(f"GOOGLE_API_KEY: {'Present' if google_key else 'Missing'}")
    if google_key:
        logger.info(f"GOOGLE_API_KEY length: {len(google_key)} chars")
    logger.info(f"OPENAI_API_KEY: {'Present' if openai_key else 'Missing'}")
    if openai_key:
        logger.info(f"OPENAI_API_KEY length: {len(openai_key)} chars")
    logger.info("---------------------------")

def run_gui_mode():
    """Start the application in GUI mode with the modern chat interface"""
    try:
        # Initialize Qt application
        app = QApplication(sys.argv)
        
        # Create AI factory for handling requests
        agent_factory = AIFactory
        
        # Create and show the main window
        window = MainWindow(agent_factory)
        window.show()
        
        # Start the Qt event loop
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Error starting GUI mode: {str(e)}")
        sys.exit(1)

def run_cli_mode():
    """Start the application in command-line interface mode"""
    try:
        # Run the CLI main function
        asyncio.run(cli_main())
    except Exception as e:
        logger.error(f"Error starting CLI mode: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Log application startup and check environment
    logger.info("Starting AI Software Assistant")
    check_environment()
    
    # Determine whether to run in GUI or CLI mode
    # Can be extended to handle command line arguments
    try:
        # Try to force reload of environment variables
        load_dotenv(override=True)
        
        # Default to GUI mode
        run_gui_mode()
    except ImportError:
        # Fallback to CLI mode if GUI dependencies are not available
        logger.warning("GUI dependencies not found. Falling back to CLI mode...")
        run_cli_mode()