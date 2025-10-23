"""
Main entry point for the AI-powered software assistant application.
Initializes the GUI and backend components and starts the application.
"""

import sys
import asyncio
from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from agent.ai.factory import AIFactory
from agent.cli import main as cli_main
from utils.logger import logger

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
    # Log application startup
    logger.info("Starting AI Software Assistant")
    
    # Determine whether to run in GUI or CLI mode
    # Can be extended to handle command line arguments
    try:
        # Default to GUI mode
        run_gui_mode()
    except ImportError:
        # Fallback to CLI mode if GUI dependencies are not available
        logger.warning("GUI dependencies not found. Falling back to CLI mode...")
        run_cli_mode()