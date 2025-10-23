"""
Main entry point of the application
"""

import sys
from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from agent.windows.system import WindowsController
from agent.ai.factory import AIFactory

# Load environment variables from .env early so factory and clients see them
load_dotenv()

def main():
    # Create Qt application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow(agent_factory=AIFactory)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()