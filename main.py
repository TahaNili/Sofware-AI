"""
Main entry point of the application
"""

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from agent.planner import analyze_user_request
from agent.windows.system import WindowsController

def main():
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Set style
    app.setStyle('Fusion')
    
    # Create and show main window
    agent = WindowsController()
    window = MainWindow(agent=agent)
    window.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()