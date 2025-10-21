"""
Main entry point of the application
"""

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from agent.planner import analyze_user_request
from agent.windows.system import WindowsController
from agent.ai.factory import AIFactory

def agent_factory(provider=None, model=None):
    # This function can create the appropriate agent based on provider/model
    # For now: just uses AIFactory
    return AIFactory.create_client()

def main():
    # Create Qt application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow(agent_factory=agent_factory)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()